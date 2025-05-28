from typing import List
from pydantic import BaseModel, Field
# --- Atomic Detail Models ---

class JobDetails(BaseModel):
    companyName: str = Field(default="NA", description="Name of the company where the candidate worked.")
    designation: str = Field(default="NA", description="Job title or designation held by the candidate.")
    fromDate: str = Field(default="NA", description="Start date of employment (format: YYYY-MM or similar).")
    toDate: str = Field(default="NA", description="End date of employment (format: YYYY-MM or similar).")
    isCurrentlyWorking: bool = Field(default=False, description="True if the candidate is still employed at this company, otherwise False.")
    reportingTo: str = Field(default="NA", description="Manager or supervisor to whom the candidate reported.")
    location: str = Field(default="NA", description="Work location (city and/or country) of the job.")
    skills: List[str] = Field(default_factory=list, description="List of key skills, technologies, or tools used in this job role.")

class ProjectDetails(BaseModel):
    companyName: str = Field(default="NA", description="Name of the company where the project was executed.")
    projectTitle: str = Field(default="NA", description="Title or name of the project.")
    fromDate: str = Field(default="NA", description="Start date of the project (format: YYYY-MM or similar).")
    toDate: str = Field(default="NA", description="End date of the project (format: YYYY-MM or similar).")
    role: str = Field(default="NA", description="Role or position of the candidate in the project.")
    projectDescription: str = Field(default="NA", description="Brief description of the project, including objectives and technologies used.")
    client: str = Field(default="NA", description="Client for whom the project was executed. If no client is mentioned, use the company name.")
    skills: List[str] = Field(default_factory=list, description="List of key skills, technologies, or tools used in this project.")

class EducationDetails(BaseModel):
    specialization: str = Field(default="NA", description="Area of specialization or major studied by the candidate.")
    degree: str = Field(default="NA", description="Academic degree obtained (e.g., BE, B.Tech, M.Tech, MBA).")
    qualification: str = Field(
        default="Others",
        description="Qualification level achieved. One of: ['Bachelors', 'Masters', 'Doctorate', 'Diploma', 'Others']."
    )
    percentageMarksOrGrade: str = Field(default="NA", description="Percentage, CGPA, or other grade obtained.")
    modeOfEducation: str = Field(default="NA", description="Mode of study such as Full-time, Part-time, or Distance education.")
    yearOfPassing: str = Field(default="NA", description="Year the candidate completed or passed the qualification.")
    college: str = Field(default="NA", description="Name of the college attended.")
    university: str = Field(default="NA", description="Name of the university under which the qualification was obtained.")

# --- Grouped Info Models ---

class ProfessionalInputSchema(BaseModel):
    skills: List[str] = Field(default_factory=list, description="List of professional skills explicitly mentioned in the resume. Do not infer or assume skills based on job titles or descriptions. Only extract if directly stated.")
    experienceYears: str = Field(default="NA", description="Total years of professional experience of the candidate.")
    noticePeriod: str = Field(default="NA", description="Notice period duration (in weeks or months) required by the candidate before leaving current employer.")
    summary: str = Field(default="NA", description="Brief professional summary or career overview provided by the candidate.")

class EducationInputSchema(BaseModel):
    education: List[EducationDetails] = Field(default_factory=list, description="List of educational qualifications and details.")

class ProjectInputSchema(BaseModel):
    projects: List[ProjectDetails] = Field(default_factory=list, description="List of projects the candidate has worked on.")

class JobInputSchema(BaseModel):
    jobs: List[JobDetails] = Field(default_factory=list, description="List of previous or current jobs held by the candidate.")

class PersonalInputSchema(BaseModel):
    firstName: str = Field(default="NA", description="First name of the candidate as mentioned in the resume. Mostly on the start of the resume.")
    middleName: str = Field(default="NA", description="Middle name of the candidate, if available.")
    lastName: str = Field(default="NA", description="Last name (surname) of the candidate.")
    primaryEmail: str = Field(default="NA", description="Candidate's official email address. Return only one email id if multiple are available. Leave empty if not available.")
    linkedinUrl: str = Field(default="NA", description="URL of the candidate's LinkedIn profile.")
    countryCode: str = Field(default="NA", description="International country code of the candidate's phone number (e.g., +1, +91, +44).")
    phoneNumber: str = Field(default="NA", description="Phone number of the candidate without the country code.")
    dob: str = Field(default="NA", description="Date of birth of the candidate in YYYY-MM-DD format.")
    latestJobDesignation: str = Field(default="NA", description="Designation or job title held by the candidate in their most recent job.")
    gender: str = Field(default="NA", description="Gender of the candidate, if mentioned.")
    city: str = Field(default="NA", description="Current city where the candidate resides or works.")
    state: str = Field(default="NA", description="Current state corresponding to the city where the candidate resides.")
    nativeLocation: str = Field(default="NA", description="Candidate's native place or hometown.")
    marriageStatus: str = Field(default="NA", description="Marital status of the candidate (e.g., Single, Married, Divorced).")