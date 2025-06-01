# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    __tablename__ = "students"
    id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name    = Column(String(255), unique=True, nullable=False)
    email   = Column(String(255), default="", nullable=True)
    dni     = Column(String(50), default="", nullable=True)
    status  = Column(String(50), default="activo", nullable=False)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.id} {self.name}>"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    monthly_fee = Column(Float, default=15000.0, nullable=False)

    # Relación bidireccional con Enrollment, si la necesitas
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course {self.id} {self.title}>"

class Enrollment(Base):
    __tablename__ = "enrollments"
    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id  = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id   = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status      = Column(String(50), default="activo", nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uix_student_course"),
    )

    def __repr__(self):
        return f"<Enrollment {self.id} s:{self.student_id} c:{self.course_id}>"
