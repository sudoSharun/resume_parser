import os
import tempfile
from fastapi import APIRouter, UploadFile, Depends
from app.endpoints.route_validator import RouteValidator
from app.llm.resume_parser import ResumeParser

router = APIRouter()

@router.post("/parse_resume")
async def parse_resume(resume: UploadFile = Depends(RouteValidator.validate_parse_resume)):
    file_path = os.path.join(tempfile.gettempdir(), resume.filename)

    with open(file_path, "wb") as f:
        f.write(resume.file.read())
    
    result = await ResumeParser(file_path).run()
    return result