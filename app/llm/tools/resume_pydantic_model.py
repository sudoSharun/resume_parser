from pydantic import BaseModel, Field, model_validator
from typing import List

class Job(BaseModel):
    companyName: str = Field(..., description="Name of the company.")
    designation: str = Field(..., description="Designation held at the company.")
    fromDate: str = Field(..., description="Start date of the job.")
    toDate: str = Field(..., description="End date of the job.")
    isCurrentlyWorking: bool = Field(..., description="True if the candidate is currently working at the company.")
    reportingTo: str = Field(..., description="Person to whom the candidate reported.")
    location: str = Field(..., description="Location of the job.")

class Project(BaseModel):
    company_name: str = Field(..., description="Name of the company.")
    project_title: str = Field(..., description="Name or title of the project.")
    role: str = Field(..., description="Role of the candidate in this project.")
    project_description: str = Field(..., description="Description of the project, including scope and technologies used.")
    client: str = Field(..., description="Name of the client for whom this project was done. If not explicit, return the company name.")
    duration: str = Field(..., description="From and to date for the project. Follow MM/DD/YYYY format.")

class Education(BaseModel):
    specialization: str = Field(..., description="Specialization obtained.")
    degree: str = Field(..., description="Degree obtained.")
    qualification: str = Field(..., description="Qualification obtained.", enum=["Bachelors", "Masters", "Doctorate", "Diploma", "Others"])
    percentage_marks_or_grade: str = Field(..., description="Percentage marks or grade obtained (CGPA, Percentage, or Grade). Look under Education for these fields.")
    modeOfEducation: str = Field(..., description="Mode of education (e.g., Full-time, Part-time).")
    yearOfPassing: str = Field(..., description="Year of graduation or passing.")
    college: str = Field(..., description="College attended.")
    university: str = Field(..., description="University attended.")

class ToolSpecInputSchema(BaseModel):
    first_name: str = Field(..., description="First name of the candidate.")
    middle_name: str = Field(..., description="Middle name of the candidate.")
    last_name: str = Field(..., description="Last name of the candidate.")
    Jobs: List[Job]
    Projects: List[Project]
    education: List[Education]
    skill: List[str] = Field(..., description="Skills of the candidate.")
    summary: str = Field(..., description="Summary of the candidate mentioned in the resume. No line breaks allowed.")

class ToolSpec(BaseModel):
    name: str = Field(..., description="Name of the tool.")
    description: str = Field(..., description="Description of the tool.")
    inputSchema: ToolSpecInputSchema

class ToolSpecWrapper(BaseModel):
    toolSpec: ToolSpec