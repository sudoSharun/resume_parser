import re
from typing import List, Optional
from dateutil import parser
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator


class CleanBaseModel(BaseModel):
    @model_validator(mode="before")
    def sanitize_values(cls, values):
        junks = {
            "NONE", "NULL", "NAN", "UNKNOWN", "<UNKNOWN>",
            "N/A", "NA", "N.A", "NONE.", "UNDEFINED", "?", "--", "NOT PROVIDED", "NOT SPECIFIED", "NOT AVAILABLE",
            "NOT MENTIONED", "NOT APPLICABLE", "NOT GIVEN", "NO DATA", "NO INFORMATION", "NO DETAILS", "NO ANSWER",
        }

        def sanitize(val):
            if val is None:
                return ""
            if isinstance(val, str) and val.strip().upper() in junks:
                return ""
            return val

        if isinstance(values, dict):
            return {key: sanitize(value) for key, value in values.items()}
        return values

    @field_validator("fromDate", "toDate", "dob", mode="before", check_fields=False)
    def format_date(cls, value):
        try:
            return parser.parse(value).strftime("%Y-%m-%d")
        except Exception:
            return ""

    @field_validator("phoneNumber", mode="before", check_fields=False)
    def extract_digits_only(cls, value):
        return re.sub(r'\D', '', value or "")


class JobDetails(CleanBaseModel):
    companyName: Optional[str] = ""
    designation: Optional[str] = ""
    fromDate: Optional[str] = ""
    toDate: Optional[str] = ""
    isCurrentlyWorking: Optional[bool] = False
    reportingTo: Optional[str] = ""
    location: Optional[str] = ""
    skills: Optional[List[str]] = []


class ProjectDetails(CleanBaseModel):
    companyName: Optional[str] = ""
    projectTitle: Optional[str] = ""
    fromDate: Optional[str] = ""
    toDate: Optional[str] = ""
    role: Optional[str] = ""
    projectDescription: Optional[str] = ""
    client: Optional[str] = ""
    skills: Optional[List[str]] = []


class EducationDetails(CleanBaseModel):
    specialization: Optional[str] = ""
    degree: Optional[str] = ""
    qualification: Optional[str] = ""
    percentageMarksOrGrade: Optional[str] = ""
    modeOfEducation: Optional[str] = ""
    yearOfPassing: Optional[str] = ""
    college: Optional[str] = ""
    university: Optional[str] = ""


class ResumeDetails(CleanBaseModel):
    firstName: Optional[str] = ""
    middleName: Optional[str] = ""
    lastName: Optional[str] = ""
    primaryEmail: Optional[str] = ""
    linkedinUrl: Optional[str] = ""
    countryCode: Optional[str] = ""
    phoneNumber: Optional[str] = ""
    dob: Optional[str] = ""
    experienceYears: Optional[str] = ""
    latestJobDesignation: Optional[str] = ""
    gender: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    nativeLocation: Optional[str] = ""
    marriageStatus: Optional[str] = ""
    jobs: Optional[List[JobDetails]] = []
    projects: Optional[List[ProjectDetails]] = []
    education: Optional[List[EducationDetails]] = []
    skills: Optional[List[str]] = []
    noticePeriod: Optional[str] = ""
    summary: Optional[str] = ""

    @model_validator(mode="before")
    def clean_empty_lists(cls, values):
        for field in ['jobs', 'projects', 'education', 'skills']:
            if field in values and isinstance(values[field], list):
                values[field] = [item for item in values[field] if item]
        return values

    @field_validator("email", mode="before", check_fields=False)
    def validate_email(cls, value):
        if not value or not isinstance(value, str) or '@' not in value:
            return ""
        try:
            EmailStr.validate(value)
            return value
        except Exception:
            return ""