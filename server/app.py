import datetime
import os
import sys
import uuid
import epitran
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from gtts import gTTS
import nltk
from nltk.corpus import cmudict
from pydantic import BaseModel
import pyopenjtalk


app = FastAPI()

# Downloading CMU Pronouncing Dictionary 
nltk.download("cmudict")
pron_dict = cmudict.dict()
epitran.download.cedict()

# Creating the audio directory if it doesn't exist
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Country to Language Mapping 
COUNTRY_LANGUAGE_MAP = {
    "australia": "english", "usa": "english", "uk": "english", "canada": "english", "jamaica": "english",
    "india": "hindi", "nepal": "nepali", "pakistan": "urdu", "bangladesh": "bengali", "sri lanka": "sinhala",
    "france": "french", "germany": "german", "spain": "spanish", "portugal": "portuguese",
    "italy": "italian", "russia": "russian", "china": "chinese", "japan": "japanese",
    "south korea": "korean", "north korea": "korean", "saudi arabia": "arabic", "uae": "arabic",
    "turkey": "turkish", "iran": "persian", "egypt": "arabic", "nigeria": "english",
    "brazil": "portuguese", "argentina": "spanish", "colombia": "spanish", "mexico": "spanish",
    "peru": "spanish", "chile": "spanish", "venezuela": "spanish", "cuba": "spanish",
    "netherlands": "dutch", "belgium": "dutch", "sweden": "swedish", "norway": "norwegian",
    "denmark": "danish", "finland": "finnish", "poland": "polish", "czech republic": "czech",
    "slovakia": "slovak", "hungary": "hungarian", "romania": "romanian", "bulgaria": "bulgarian",
    "greece": "greek", "serbia": "serbian", "croatia": "croatian", "ukraine": "ukrainian",
    "south africa": "english", "ethiopia": "amharic", "kenya": "swahili", "ghana": "english",
    "israel": "hebrew", "thailand": "thai", "vietnam": "vietnamese", "philippines": "filipino",
    "indonesia": "indonesian", "malaysia": "malay", "kazakhstan": "kazakh", "uzbekistan": "uzbek",
    "afghanistan": "pashto", "mongolia": "mongolian", "myanmar": "burmese", "taiwan": "chinese",
    "singapore": "english", "brunei": "malay", "laos": "lao", "cambodia": "khmer",
    "paraguay": "spanish", "ecuador": "spanish", "bolivia": "spanish", "uruguay": "spanish",
    "panama": "spanish", "honduras": "spanish", "guatemala": "spanish", "el salvador": "spanish",
    "costa rica": "spanish", "nicaragua": "spanish", "trinidad and tobago": "english", "haiti": "french"
}

# Country to Language Mapping
LANGUAGE_MAP = {
    "australia": "english", "usa": "english", "uk": "english", "canada": "english", "jamaica": "english",
    "india": "hindi", "nepal": "nepali", "pakistan": "urdu", "bangladesh": "bengali", "sri lanka": "sinhala",
    "france": "french", "germany": "german", "spain": "spanish", "portugal": "portuguese",
    "italy": "italian", "russia": "russian", "china": "chinese", "japan": "japanese",
    "south korea": "korean", "north korea": "korean", "saudi arabia": "arabic", "uae": "arabic",
    "turkey": "turkish", "iran": "persian", "egypt": "arabic", "nigeria": "english",
    "brazil": "portuguese", "argentina": "spanish", "colombia": "spanish", "mexico": "spanish",
    "peru": "spanish", "chile": "spanish", "venezuela": "spanish", "cuba": "spanish",
    "netherlands": "dutch", "belgium": "dutch", "sweden": "swedish", "norway": "norwegian",
    "denmark": "danish", "finland": "finnish", "poland": "polish", "czech republic": "czech",
    "slovakia": "slovak", "hungary": "hungarian", "romania": "romanian", "bulgaria": "bulgarian",
    "greece": "greek", "serbia": "serbian", "croatia": "croatian", "ukraine": "ukrainian",
    "south africa": "english", "ethiopia": "amharic", "kenya": "swahili", "ghana": "english",
    "israel": "hebrew", "thailand": "thai", "vietnam": "vietnamese", "philippines": "filipino",
    "indonesia": "indonesian", "malaysia": "malay", "kazakhstan": "kazakh", "uzbekistan": "uzbek",
    "afghanistan": "pashto", "mongolia": "mongolian", "myanmar": "burmese", "taiwan": "chinese",
    "singapore": "english", "brunei": "malay", "laos": "lao", "cambodia": "khmer",
    "paraguay": "spanish", "ecuador": "spanish", "bolivia": "spanish", "uruguay": "spanish",
    "panama": "spanish", "honduras": "spanish", "guatemala": "spanish", "el salvador": "spanish",
    "costa rica": "spanish", "nicaragua": "spanish", "trinidad and tobago": "english", "haiti": "french"
}

# Language to TTS Voice Mapping
TTS_LANGUAGE_MAP = {
    "english": "en-US-Wavenet-D",  # US English
    "hindi": "hi-IN-Wavenet-A",    # Hindi
    "nepali": "ne-NP-Wavenet-A",   # Nepali
    "urdu": "ur-PK-Wavenet-A",     # Urdu
    "bengali": "bn-IN-Wavenet-A",  # Bengali
    "sinhala": "si-LK-Wavenet-A",  # Sinhala
    "french": "fr-FR-Wavenet-C",   # French
    "german": "de-DE-Wavenet-B",   # German
    "spanish": "es-ES-Wavenet-C",  # Spanish
    "portuguese": "pt-BR-Wavenet-B",  # Portuguese
    "italian": "it-IT-Wavenet-D",  # Italian
    "russian": "ru-RU-Wavenet-D",  # Russian
    "chinese": "cmn-CN-Wavenet-C", # Mandarin Chinese
    "japanese": "ja-JP-Wavenet-C", # Japanese
    "korean": "ko-KR-Wavenet-C",   # Korean
    "arabic": "ar-XA-Wavenet-C",   # Arabic
    "turkish": "tr-TR-Wavenet-E",  # Turkish
    "persian": "fa-IR-Wavenet-A",  # Persian
    "dutch": "nl-NL-Wavenet-B",    # Dutch
    "swedish": "sv-SE-Wavenet-A",  # Swedish
    "norwegian": "nb-NO-Wavenet-A",# Norwegian
    "danish": "da-DK-Wavenet-C",   # Danish
    "finnish": "fi-FI-Wavenet-A",  # Finnish
    "polish": "pl-PL-Wavenet-E",   # Polish
    "czech": "cs-CZ-Wavenet-A",    # Czech
    "slovak": "sk-SK-Wavenet-A",   # Slovak
    "hungarian": "hu-HU-Wavenet-A",# Hungarian
    "romanian": "ro-RO-Wavenet-A", # Romanian
    "bulgarian": "bg-BG-Wavenet-A",# Bulgarian
    "greek": "el-GR-Wavenet-A",    # Greek
    "serbian": "sr-RS-Wavenet-A",  # Serbian
    "croatian": "hr-HR-Wavenet-A", # Croatian
    "ukrainian": "uk-UA-Wavenet-A",# Ukrainian
    "amharic": "am-ET-Wavenet-A",  # Amharic
    "swahili": "sw-KE-Wavenet-A",  # Swahili
    "hebrew": "he-IL-Wavenet-B",   # Hebrew
    "thai": "th-TH-Wavenet-A",     # Thai
    "vietnamese": "vi-VN-Wavenet-A",# Vietnamese
    "filipino": "fil-PH-Wavenet-A",# Filipino
    "indonesian": "id-ID-Wavenet-D",# Indonesian
    "malay": "ms-MY-Wavenet-A",    # Malay
    "kazakh": "kk-KZ-Wavenet-A",   # Kazakh
    "uzbek": "uz-UZ-Wavenet-A",    # Uzbek
    "pashto": "ps-AF-Wavenet-A",   # Pashto
    "mongolian": "mn-MN-Wavenet-A",# Mongolian
    "burmese": "my-MM-Wavenet-A",  # Burmese
    "lao": "lo-LA-Wavenet-A",      # Lao
    "khmer": "km-KH-Wavenet-A",    # Khmer
    "french": "fr-FR-Wavenet-C"    # French (Haiti)
}

class NameRequest(BaseModel):
    name: str
    country: str

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

def get_phonetic_transcription(name: str, country: str):
    country = country.lower()

    if country not in COUNTRY_LANGUAGE_MAP:
        return {"error": "Country not supported!"}

    language = COUNTRY_LANGUAGE_MAP[country]

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    audio_filename = f"{name}_{country}_{timestamp}_{unique_id}.mp3"
    audio_file = f"{AUDIO_DIR}/{audio_filename}"

    if language == "english" and name.lower() in pron_dict:
        phonetic = " ".join(pron_dict[name.lower()][0])
    elif language == "japanese":
        phonetic = pyopenjtalk.g2p(name)
    elif language in LANGUAGE_MAP:
        epi = epitran.Epitran(LANGUAGE_MAP[language])
        phonetic = epi.transliterate(name)
    else:
        phonetic = "Language not supported!"

    tts_lang = TTS_LANGUAGE_MAP.get(language, "en")
    tts = gTTS(text=name, lang=tts_lang)
    tts.save(audio_file)

    return {"name": name, "phonetic_transcription": phonetic, "audio_file": audio_filename}

@app.post("/transcription")
def transcription(request: NameRequest):
    return get_phonetic_transcription(request.name, request.country)
