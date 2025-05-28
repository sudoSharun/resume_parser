from dataclasses import dataclass
from fastapi import UploadFile, File
from typing import Set
from pypdf import PdfReader
from docx import Document
from app.endpoints.errors import APIException
import io

class RouteValidator:
    allowed_extensions: Set[str] = {"pdf", "doc", "docx"}

    @staticmethod
    def validate_parse_resume(resume: UploadFile = File(...)) -> UploadFile:
        try:
            ext = RouteValidator._extract_extension(resume)
            RouteValidator._validate_file_type(ext)
            RouteValidator._validate_file_content(resume, ext)
            return resume
        except AttributeError:
            raise APIException(500)

    # --- Internal helpers ---
    
    @staticmethod
    def _extract_extension(resume: UploadFile) -> str | None:
        filename = resume.filename.lower()
        return next((ext for ext in RouteValidator.allowed_extensions if filename.endswith(f".{ext}")), None)

    @staticmethod
    def _validate_file_type(ext: str | None) -> None:
        if not ext:
            raise APIException(415)

    @staticmethod
    def _validate_file_content(resume: UploadFile, ext: str) -> None:
        try:
            file_bytes = resume.file.read()
            resume.file.seek(0)

            match ext:
                case "pdf":
                    PdfReader(io.BytesIO(file_bytes))
                case "doc" | "docx":
                    Document(io.BytesIO(file_bytes))
        except Exception:
            raise APIException(422)