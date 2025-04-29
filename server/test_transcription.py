
import os
import warnings
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Suppress deprecation warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r".*app",
)

from app import app, get_phonetic_transcription, insert_syllable_breaks


# ---------- Fixtures -------------------------------------------- #
@pytest.fixture
def client():
    """Provides a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_audio_dir():
    """Ensure server/test_audio folder exists."""
    test_audio_path = os.path.join(os.path.dirname(__file__), "test_audio")
    os.makedirs(test_audio_path, exist_ok=True)
    yield


@pytest.fixture
def mock_polly(monkeypatch, mock_audio_dir):
    """Mock the AWS Polly client."""
    mock_audio_stream = MagicMock()
    mock_audio_stream.read.return_value = b""

    mock_client = MagicMock()
    mock_client.synthesize_speech.return_value = {"AudioStream": mock_audio_stream}

    monkeypatch.setattr("boto3.client", lambda *args, **kwargs: mock_client)
    return mock_client


# ---------- Helper Function Tests ------------------------------- #
def test_insert_syllable_breaks_inserts_correctly():
    """Test correct insertion of syllable breaks into IPA."""
    test_cases = [
        ("kæləb", "kælə / b"),
        ("hello", "he / llo"),
        ("nəməste", "nə / mə / ste"),
        ("tə.ɡe.ðɚ", "tə / ɡe / ðɚ"),
    ]
    for ipa_input, expected in test_cases:
        result = insert_syllable_breaks(ipa_input)
        assert result == expected, f"Expected: {expected}, Got: {result}"


def test_insert_syllable_breaks_returns_string():
    """Test that insert_syllable_breaks returns a string type."""
    ipa_input = "testing"
    result = insert_syllable_breaks(ipa_input)
    expected = str
    assert isinstance(result, expected), f"Expected type: {expected}, Got: {type(result)}"


# ---------- API Endpoint Tests ---------------------------------- #
def test_transcription_endpoint_single_input(client, mock_polly):
    """Test /transcription endpoint with single valid input."""
    test_data = {"First": "太郎", "Last": "山田", "Country": "japan"}

    response = client.post("/transcription", json=test_data)
    result = response.status_code
    expected = 200
    assert result == expected, f"Expected status code: {expected}, Got: {result}"

    payload = response.json()[0]
    assert isinstance(payload["Translation"], list), "Expected 'Translation' to be a list."
    assert mock_polly.synthesize_speech.called, "Expected Polly synthesize_speech to be called."


def test_batch_transcription_endpoint_multiple_inputs(client, mock_polly):
    """Test /batch-transcription endpoint with a CSV of two entries."""
    csv_data = "First,Last,Country\n太郎,山田,Japan\n花子,田中,Japan\n"

    response = client.post(
        "/batch-transcription",
        files={"file": ("sample.csv", csv_data, "text/csv")},
    )
    result = response.status_code
    expected = 200
    assert result == expected, f"Expected status code: {expected}, Got: {result}"

    data = response.json()
    assert len(data) == 2, f"Expected 2 results, Got: {len(data)}"
    assert "First" in data[0], "Expected 'First' field in result."
    assert "Country" in data[1], "Expected 'Country' field in result."
    assert mock_polly.synthesize_speech.call_count == 2, f"Expected 2 Polly calls, Got: {mock_polly.synthesize_speech.call_count}"


# ---------- Error Handling Tests -------------------------------- #
def test_get_phonetic_transcription_invalid_language(mock_polly):
    """Test get_phonetic_transcription handles invalid language codes."""
    result = get_phonetic_transcription("Test", "invalid-code")
    expected_phrase = "phonetic_transcription"

    assert isinstance(result, dict), f"Expected dict, Got: {type(result)}"
    assert expected_phrase in result, f"Expected key '{expected_phrase}' in result."
    assert isinstance(result["phonetic_transcription"], str), "Expected phonetic_transcription to be a string."
    assert not mock_polly.synthesize_speech.called, "Polly should NOT be called for invalid languages."


def test_get_phonetic_transcription_empty_country(mock_polly):
    """Test get_phonetic_transcription handles empty country input."""
    result = get_phonetic_transcription("Test", "")
    expected = "Country not provided"

    assert isinstance(result, dict), f"Expected dict, Got: {type(result)}"
    assert result.get("phonetic_transcription") == expected, f"Expected: {expected}, Got: {result.get('phonetic_transcription')}"
    assert not mock_polly.synthesize_speech.called, "Polly should NOT be called for empty country."
