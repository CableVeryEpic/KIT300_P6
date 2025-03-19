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

---

## 🚀 Running the API Server
After installation, start the **FastAPI** server:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

You can also explore the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📌 API Endpoints

### 1️⃣ Get Phonetic Transcription
```http
POST /transcription/
```
**Request JSON:**
```json
{
    "name": "John",
    "country": "USA"
}
```
**Response JSON:**
```json
{
    "name": "John",
    "country": "USA",
    "phonetic": "JH AA N"
}
```
---

## 🛠 Fixes and Enhancements

### **Issue: UnicodeEncodeError on Windows**
When running the API on Windows, the `epitran.download.cedict()` function may encounter a `UnicodeEncodeError` due to the default encoding (`cp1252`) being unable to handle certain Unicode characters (e.g., `\u5340`).

### **Solution**
To resolve this issue, modify the `cedict()` function in the `download.py` file to explicitly use UTF-8 encoding when writing the downloaded dictionary file. This ensures compatibility with all Unicode characters.

#### **Changes Made**
1. **Update the `cedict()` Function**:
   - Add `encoding='utf-8'` to the `open()` call when writing the file.
   - This ensures that the file is written using UTF-8 encoding, which supports all Unicode characters.

   ```python
   def cedict():
       gzfilename = os.path.join(get_dir(), 'cedict.txt.gz')
       txtfilename = os.path.join(get_dir(), 'cedict.txt')
       r = requests.get(CEDICT_URL)
       with open(gzfilename, 'wb') as f:
           f.write(r.content)
       with gzip.open(gzfilename, 'rb') as ip_byte, open(txtfilename, 'w', encoding='utf-8') as op:
           op.write(ip_byte.read().decode('utf-8'))
   ```

### **Impact**
- The API now works seamlessly on Windows and other platforms without encountering encoding issues.
- All Unicode characters in the CC-CEDict dictionary are handled correctly.


## 📄 License
This project is licensed under the [MIT License](https://mit-license.org/). 

---

## 🙏 Acknowledgments
