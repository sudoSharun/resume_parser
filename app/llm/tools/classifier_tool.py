from pydantic import BaseModel, Field

from typing import List

class ClassifierInputSchema(BaseModel):
    PersonalInfo: List[int] = Field(default_factory=list, description="List of personal information details.")
    EducationDetails: List[int] = Field(default_factory=list, description="List of education details.")
    ProjectDetails: List[int] = Field(default_factory=list, description="List of project details.")
    JobDetails: List[int] = Field(default_factory=list, description="List of job details.")
    ProfessionalInfo: List[int] = Field(default_factory=list, description="List of professional information.")