from typing import Literal

from pydantic import BaseModel, EmailStr


class FacultyCreate(BaseModel):
    name: str


class FacultyUpdate(BaseModel):
    name: str


class FacultyResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class SubjectCreate(BaseModel):
    name: str


class SubjectResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class StudentCreate(BaseModel):
    last_name: str
    first_name: str


class StudentUpdate(BaseModel):
    last_name: str
    first_name: str


class StudentResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    model_config = {"from_attributes": True}


class GradeCreate(BaseModel):
    student_id: int
    faculty_id: int
    subject_id: int
    grade: int


class GradeUpdate(BaseModel):
    grade: int


class GradeResponse(BaseModel):
    id: int
    student_id: int
    faculty_id: int
    subject_id: int
    grade: int
    model_config = {"from_attributes": True}


class FailingStudentResponse(BaseModel):
    student: StudentResponse
    grade: int


class AvgGradeResponse(BaseModel):
    faculty: str
    avg_grade: float


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "readonly"] = "admin"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
