from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import tempfile
import os
from .pdf_generator import create_custom_pdf

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates/template.pdf")
LOGO_PATH = os.path.join(BASE_DIR, "templates/logo.png")

class PDFRequest(BaseModel):
    name: str
    score: str
    date: str
    countries: List[str]

@app.post("/generate-pdf")
async def generate_pdf(data: PDFRequest):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_output:
        create_custom_pdf(
            name=data.name,
            score=data.score,
            date=data.date,
            countries=data.countries,
            logo_path=LOGO_PATH,
            template_path=TEMPLATE_PATH,
            output_path=tmp_output.name
        )
        return StreamingResponse(open(tmp_output.name, "rb"), media_type="application/pdf")

