import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd

from app import app

client = TestClient(app)

# Mock "get_phonetic_transcription" so we don't rely on its real functionality.
# This way, you can focus on testing only your endpoint and file handling logic.
@patch("app.get_phonetic_transcription", side_effect=lambda name, country: f"Mocked-{name}-{country}")
def test_batch_transcription_csv(mock_get_phonetic_transcription):
    """
    Test the /batch-transcription endpoint with a CSV file containing valid columns.
    """
    # Create a CSV in-memory
    csv_content = """Name,Country
Quan Bai,China
Midori Sugie,Japan
"""
    # We pass the CSV content as if it was uploaded by the client
    files = {
        "file": ("test.csv", csv_content, "text/csv")
    }

    response = client.post("/batch-transcription", files=files)

    assert response.status_code == 200, "Expected 200 OK for valid CSV input"

    # The endpoint returns a CSV file, so let's read it from response.text
    output_csv = response.text
    output_df = pd.read_csv(io.StringIO(output_csv))

    # Check that the output CSV has the expected columns and data
    assert "Name" in output_df.columns
    assert "Country" in output_df.columns
    assert "Translation" in output_df.columns

    # Verify the mock transcription in the output
    assert output_df.loc[0, "Translation"] == "Mocked-Quan Bai-China"
    assert output_df.loc[1, "Translation"] == "Mocked-Midori Sugie-Japan"


def test_batch_transcription_missing_columns():
    """
    Test that the endpoint returns an error if required columns are missing.
    """
    csv_content = """Username,Location
Quan Bai,China
Midori Sugie,Japan
"""
    files = {
        "file": ("test.csv", csv_content, "text/csv")
    }

    response = client.post("/batch-transcription", files=files)

    # This should fail because "Name" and "Country" columns are missing
    assert response.status_code == 200  # The endpoint itself may return 200 with an error dict
    json_data = response.json()
    assert "error" in json_data
    assert "File must contain 'Name' and 'Country' columns." in json_data["error"]

def test_batch_transcription_invalid_format():
    """
    Test that an unsupported file format returns an appropriate error.
    """
    # Provide a file that isn't csv or xlsx
    invalid_content = "Just some text"
    files = {
        "file": ("test.txt", invalid_content, "text/plain")
    }

    response = client.post("/batch-transcription", files=files)

    json_data = response.json()
    assert "error" in json_data
    assert "Unsupported file format" in json_data["error"]