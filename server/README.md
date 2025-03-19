# 🌍 Phonetic Transcription & Pronunciation API

This project provides a **FastAPI**-based REST API that generates **phonetic transcriptions** and **audio pronunciations** for names based on country-specific languages. It utilizes **Epitran** for phonetic transcription, **CMU Pronouncing Dictionary (CMUdict) for English phonemes**, and **gTTS for audio synthesis**.

---

## 🚀 Features
- Convert names to **phonetic transcription** based on country/language
- Generate **spoken pronunciations** as MP3 files
- Process **single names** or **batch files (CSV/Excel)**
- REST API built with **FastAPI** for easy integration

---


## 🛠 Installation

### 1️⃣ Using Conda (Recommended)
Create and activate a Conda environment:

```bash
conda create --name phonetic-api python=3.10 -y
conda activate phonetic-api
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the **CMU Pronouncing Dictionary** (only needed once):

```bash
python -c "import nltk; nltk.download('cmudict')"
```

---

### 2️⃣ Using Python Virtual Environment (venv)
If you prefer using **venv**, follow these steps:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download CMUdict (only needed once)
python -c "import nltk; nltk.download('cmudict')"
```
