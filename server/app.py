import datetime
import os
import sys
import uuid
import epitran
import pykakasi
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
from gtts import gTTS
import nltk
from nltk.corpus import cmudict
import pandas as pd
from pydantic import BaseModel
import pyopenjtalk


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Downloading CMU Pronouncing Dictionary 
nltk.download("cmudict")
pron_dict = cmudict.dict()
epitran.download.cedict()

# Creating the audio directory if it doesn't exist
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Country to Language Mapping 
COUNTRY_LANGUAGE_MAP = {
    "australia": "english",
    "usa": "english",
    "uk": "english",
    "canada": "english",
    "india": "hindi",
    "nepal": "nepali",
    "france": "french",
    "germany": "german",
    "spain": "spanish",
    "portugal": "portuguese",
    "italy": "italian",
    "china": "chinese",
    "japan": "japanese",
    "korea": "korean",
    "turkey": "turkish",
    "russia": "russian",
    "vietnam": "vietnamese",
    "thailand": "thai",
    "ethiopia": "amharic",
    "iraq": "sorani",
    "egypt": "arabic",
    "sudan": "arabic",
    "somalia": "somali",
    "kenya": "swahili",
    "south africa": "zulu",
    "nigeria": "yoruba",
    "ghana": "akan",
    "senegal": "wolof",
    "tanzania": "swahili",
    "uganda": "luganda",
    "rwanda": "kinyarwanda",
    "burundi": "rundi",
    "cambodia": "khmer",
    "laos": "lao",
    "myanmar": "burmese",
    "philippines": "tagalog",
    "indonesia": "indonesian",
    "malaysia": "malay",
    "pakistan": "urdu",
    "bangladesh": "bengali",
    "sri lanka": "sinhala",
    "kazakhstan": "kazakh",
    "uzbekistan": "uzbek",
    "tajikistan": "tajik",
    "kyrgyzstan": "kyrgyz",
    "turkmenistan": "turkmen",
    "afghanistan": "pashto",
    "mongolia": "mongolian",
    "brazil": "portuguese",
    "argentina": "spanish",
    "mexico": "spanish",
    "colombia": "spanish",
    "peru": "quechua",
    "ecuador": "quechua",
    "bolivia": "quechua",
    "chile": "spanish",
    "venezuela": "spanish",
    "cuba": "spanish",
    "dominican republic": "spanish",
    "puerto rico": "spanish",
    "jamaica": "jamaican",
    "haiti": "haitian creole",
    "morocco": "arabic",
    "algeria": "arabic",
    "tunisia": "arabic",
    "libya": "arabic",
    "mauritania": "arabic",
    "mali": "bambara",
    "niger": "hausa",
    "chad": "arabic",
    "cameroon": "french",
    "congo": "french",
    "angola": "portuguese",
    "mozambique": "portuguese",
    "zimbabwe": "shona",
    "zambia": "bemba",
    "botswana": "tswana",
    "namibia": "afrikaans",
    "lesotho": "sesotho",
    "swaziland": "swati",
    "madagascar": "malagasy",
    "mauritius": "creole",
    "seychelles": "creole",
    "comoros": "comorian",
    "djibouti": "afar",
    "eritrea": "tigrinya",
    "somaliland": "somali",
    "yemen": "arabic",
    "oman": "arabic",
    "uae": "arabic",
    "qatar": "arabic",
    "kuwait": "arabic",
    "bahrain": "arabic",
    "israel": "hebrew",
    "jordan": "arabic",
    "lebanon": "arabic",
    "syria": "arabic",
    "palestine": "arabic",
    "cyprus": "greek",
    "greece": "greek",
    "albania": "albanian",
    "bulgaria": "bulgarian",
    "serbia": "serbian",
    "croatia": "croatian",
    "bosnia": "bosnian",
    "montenegro": "montenegrin",
    "macedonia": "macedonian",
    "slovenia": "slovene",
    "slovakia": "slovak",
    "czech republic": "czech",
    "poland": "polish",
    "hungary": "hungarian",
    "romania": "romanian",
    "moldova": "romanian",
    "ukraine": "ukrainian",
    "belarus": "belarusian",
    "lithuania": "lithuanian",
    "latvia": "latvian",
    "estonia": "estonian",
    "finland": "finnish",
    "sweden": "swedish",
    "norway": "norwegian",
    "denmark": "danish",
    "iceland": "icelandic",
    "ireland": "irish",
    "netherlands": "dutch",
    "belgium": "dutch",
    "luxembourg": "luxembourgish",
    "switzerland": "german",
    "austria": "german",
    "liechtenstein": "german",
    "monaco": "french",
    "andorra": "catalan",
    "san marino": "italian",
    "vatican city": "italian",
    "malta": "maltese",
    "georgia": "georgian",
    "armenia": "armenian",
    "azerbaijan": "azerbaijani",
    "iran": "farsi",
    "saudi arabia": "arabic",
    "bhutan": "dzongkha",
    "singapore": "malay",
    "brunei": "malay",
    "east timor": "tetum",
    "papua new guinea": "tok pisin",
    "fiji": "fijian",
    "samoa": "samoan",
    "tonga": "tongan",
    "vanuatu": "bislama",
    "solomon islands": "pijin",
    "kiribati": "gilbertese",
    "marshall islands": "marshallese",
    "palau": "palauan",
    "nauru": "nauruan",
    "tuvalu": "tuvaluan",
    "micronesia": "chamorro",
    "new zealand": "maori",
}

# Language Mapping
LANGUAGE_MAP = {
    "afar": "aar-Latn",
    "assyrian neo-aramaic": "aii-Syrc",
    "amharic": "amh-Ethi",
    "arabic": "ara-Arab",
    "avaric": "ava-Cyrl",
    "azerbaijani": "aze-Latn",
    "bengali": "ben-Beng",
    "bukusu": "bxk-Latn",
    "catalan": "cat-Latn",
    "cebuano": "ceb-Latn",
    "czech": "ces-Latn",
    "jin": "cjy-Latn",
    "chinese": "cmn-Latn",
    "sorani": "ckb-Arab",
    "kashubian": "csb-Latn",
    "german": "deu-Latn",
    "english": "eng-Latn",
    "esperanto": "epo-Latn",
    "farsi": "fas-Arab",
    "french": "fra-Latn",
    "fulah": "ful-Latn",
    "gan": "gan-Latn",
    "gothic": "got-Latn",
    "hakka": "hak-Latn",
    "hausa": "hau-Latn",
    "hindi": "hin-Deva",
    "hmong": "hmn-Latn",
    "croatian": "hrv-Latn",
    "hungarian": "hun-Latn",
    "ilocano": "ilo-Latn",
    "indonesian": "ind-Latn",
    "italian": "ita-Latn",
    "jamaican": "jam-Latn",
    "japanese": "jpn-Hrgn",
    "javanese": "jav-Latn",
    "kazakh": "kaz-Latn",
    "kabardian": "kbd-Cyrl",
    "khmer": "khm-Khmr",
    "kinyarwanda": "kin-Latn",
    "kyrgyz": "kir-Latn",
    "kurmanji": "kmr-Latn",
    "korean": "kor-Hang",
    "lao": "lao-Laoo",
    "ligurian": "lij-Latn",
    "saamia": "lsm-Latn",
    "malayalam": "mal-Mlym",
    "marathi": "mar-Deva",
    "maltese": "mlt-Latn",
    "mongolian": "mon-Cyrl-bab",
    "maori": "mri-Latn",
    "malay": "msa-Latn",
    "burmese": "mya-Mymr",
    "hokkien": "nan-Latn",
    "dutch": "nld-Latn",
    "chichewa": "nya-Latn",
    "tohono o'odham": "ood-Latn-sax",
    "odia": "ori-Orya",
    "oromo": "orm-Latn",
    "punjabi": "pan-Guru",
    "polish": "pol-Latn",
    "portuguese": "por-Latn",
    "quechua": "quy-Latn",
    "romanian": "ron-Latn",
    "rundi": "run-Latn",
    "russian": "rus-Cyrl",
    "sango": "sag-Latn",
    "sinhala": "sin-Sinh",
    "shona": "sna-Latn",
    "somali": "som-Latn",
    "spanish": "spa-Latn",
    "albanian": "sqi-Latn",
    "serbian": "srp-Latn",
    "swahili": "swa-Latn",
    "swedish": "swe-Latn",
    "tamil": "tam-Taml",
    "telugu": "tel-Telu",
    "tajik": "tgk-Cyrl",
    "tagalog": "tgl-Latn",
    "thai": "tha-Thai",
    "tigrinya": "tir-Ethi",
    "tok pisin": "tpi-Latn",
    "turkmen": "tuk-Latn",
    "turkish": "tur-Latn",
    "ukrainian": "ukr-Cyrl",
    "urdu": "urd-Arab",
    "uyghur": "uig-Arab",
    "uzbek": "uzb-Latn",
    "vietnamese": "vie-Latn",
    "xhosa": "xho-Latn",
    "yoruba": "yor-Latn",
    "zulu": "zul-Latn",
}

# TTS Language Mapping 
TTS_LANGUAGE_MAP = {
    "english": "en",
    "nepali": "ne",
    "hindi": "hi",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "portuguese": "pt",
    "italian": "it",
    "russian": "ru",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "arabic": "ar",
    "turkish": "tr",
    "urdu": "ur",
    "persian": "fa",
    "amharic": "am",
    "bengali": "bn",
    "czech": "cs",
    "dutch": "nl",
    "finnish": "fi",
    "greek": "el",
    "hebrew": "he",
    "hungarian": "hu",
    "indonesian": "id",
    "khmer": "km",
    "malay": "ms",
    "polish": "pl",
    "swahili": "sw",
    "thai": "th",
    "vietnamese": "vi",
    "yoruba": "yo",
    "zulu": "zu",
}

class NameRequest(BaseModel):
    name: str
    country: str

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/supported-countries")
def get_supported_countries():
    """Returns a list of supported countries."""
    return list(COUNTRY_LANGUAGE_MAP.keys())

def get_english_phonetic(name: str) -> str:
    """Get phonetic transcription for English using CMU Pronouncing Dictionary."""
    if name.lower() in pron_dict:
        return " ".join(pron_dict[name.lower()][0])
    return "Phonetic transcription not found in CMU dictionary."


def get_japanese_phonetic(name: str) -> str:
    """Get phonetic transcription for Japanese using kakasi transliteration then epitran."""
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "H")  # Hiragana
    kakasi.setMode("K", "H")  # Katakana to Hiragana
    kakasi.setMode("J", "H")  # Kanji to Hiragana
    kakasi.setMode("r", "Hepburn")  # Use Hepburn romaji if needed

    converter = kakasi.getConverter()
    hira = converter.do(name)
    return get_epitran_phonetic(hira, 'jpn-Hrgn')

def get_hindi_phonetic(name: str) -> str:
    """Get phonetic transcription for hindi using transliteration then epitran"""
    devanagari = transliterate(name, ITRANS, DEVANAGARI)
    return get_epitran_phonetic(devanagari, 'hin-Deva')

def get_epitran_phonetic(name: str, language_code: str) -> str:
    """Get phonetic transcription using epitran for the given language code."""
    try:
        epi = epitran.Epitran(language_code)
        return epi.transliterate(name)
    except FileNotFoundError:
        return (
            f"Phonetic transcription not supported for language code: {language_code}."
        )


def get_phonetic_transcription(name: str, country: str) -> str:
    """Returns phonetic transcription and generates audio file."""
    country = country.lower()

    if country not in COUNTRY_LANGUAGE_MAP:
        return {"error": "Country not supported!"}

    language = COUNTRY_LANGUAGE_MAP[country]

    # Generating a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Current timestamp
    unique_id = uuid.uuid4().hex[:6]  # Random unique identifier
    audio_filename = f"{name}{country}{timestamp}_{unique_id}.mp3"
    audio_file = f"{AUDIO_DIR}/{audio_filename}"

    # Language-specific handlers
    language_handlers = {
        "english": get_english_phonetic,
        "japanese": get_japanese_phonetic,
        "hindi": get_hindi_phonetic,
    }

    # Get phonetic transcription
    if language in language_handlers:
        phonetic = language_handlers[language](name)
    elif language in LANGUAGE_MAP:
        phonetic = get_epitran_phonetic(name, LANGUAGE_MAP[language])
    else:
        phonetic = f"Language not supported: {language}."

    # Generate audio
    tts_lang = TTS_LANGUAGE_MAP.get(language, "en")  # Default to English if not found
    tts = gTTS(text=name, lang=tts_lang)
    tts.save(audio_file)

    return phonetic

@app.post("/transcription")
def transcription(request: NameRequest):
    return get_phonetic_transcription(request.name, request.country)

@app.post("/batch-transcription")
async def batch_transcription(file: UploadFile = File(...)):
    """Processes a batch file and returns transcriptions with audio."""
    try:
        # Read file
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Unsupported file format. Use CSV or Excel."}

        if "Name" not in df.columns or "Country" not in df.columns:
            return {"error": "File must contain 'Name' and 'Country' columns."}

        # Process each row
        results = []
        for _, row in df.iterrows():
            result = {"Name":row["Name"], "Country":row["Country"], "Translation":get_phonetic_transcription(row["Name"], row["Country"])}
            results.append(result)

        output_df = pd.DataFrame(results)
        csv_buffer = StringIO()
        output_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        return StreamingResponse(
            csv_buffer,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=transcription_output.csv"},
            )

    except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as e:
        return {"error": str(e)}