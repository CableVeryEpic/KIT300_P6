from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

class NameRequest(BaseModel):
    name: str
    country: str

# Redirecting root ("/") to Swagger UI ("/docs")
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/transcription")
def transcription(request: NameRequest):
    """Transcribes a single name and generates audio"""
    return None