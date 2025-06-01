# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    name: str
    email: Optional[str] = ""
    dni: Optional[str] = ""
    status: Optional[str] = "activo"

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    id: int

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = ""
    monthly_fee: Optional[float] = 15000.0

class CourseBase(BaseModel):
    title: str
    monthly_fee: float

class CourseCreate(CourseBase):
    # Al crear, solo necesitamos título y mensualidad (si quieres podrías hacer monthly_fee opcional con default)
    pass

class CourseUpdate(CourseBase):
    id: int  # Al actualizar, requerimos el ID del curso que se va a modificar

    class Config:
        orm_mode = True


# (Si lo deseas, también puedes definir un schema “CourseOut” para usar en respuestas JSON)
class CourseOut(BaseModel):
    id: int
    title: str
    monthly_fee: float

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: Optional[str] = "activo"

class EnrollmentCreate(EnrollmentBase):
    pass

class DueOut(BaseModel):
    subtotal: float
    recargo: float
    total: float


class StudentBase(BaseModel):
    name: str
    email: Optional[str] = ""
    dni: Optional[str] = ""
    status: Optional[str] = "activo"

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    id: int
