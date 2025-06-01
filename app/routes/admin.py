# app/routes/admin.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND

from ..crud import (
    get_student, list_students, create_student, update_student, delete_student,
    get_course, list_courses, create_course, update_course, delete_course,
    list_enrollments, create_enrollment, delete_enrollment,
    calculate_due_for_student, calculate_next_month_due_for_student
)
from ..deps import get_db, ensure_admin
from ..schemas import StudentCreate, StudentUpdate, CourseCreate, CourseUpdate, EnrollmentCreate

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

# — DASHBOARD —
@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request, user=Depends(ensure_admin), db: Session = Depends(get_db)):
    if hasattr(user, "status_code"):
        return user
    total_students = len(list_students(db))
    total_courses  = len(list_courses(db))
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "total_students": total_students,
        "total_courses": total_courses
    })

# — ESTUDIANTES —
@router.get("/students", response_class=HTMLResponse)
def admin_manage_students(
    request: Request,
    edit_id: int = None,
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    students = list_students(db)
    student_to_edit = None
    if edit_id:
        student_to_edit = get_student(db, edit_id)

    return templates.TemplateResponse("admin/students.html", {
        "request": request,
        "students": students,
        "student_to_edit": student_to_edit
    })


@router.post("/students", response_class=RedirectResponse)
def admin_post_student(
    request: Request,
    id: int = Form(None),
    name: str = Form(...),
    email: str = Form(""),
    dni: str = Form(""),
    status: str = Form("activo"),
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    if id:
        update_student(db, StudentUpdate(id=id, name=name, email=email, dni=dni, status=status))
    else:
        create_student(db, StudentCreate(name=name, email=email, dni=dni, status=status))

    return RedirectResponse(url="/admin/students", status_code=HTTP_302_FOUND)


@router.get("/students/delete/{student_id}", response_class=RedirectResponse)
def admin_delete_student(student_id: int, user=Depends(ensure_admin), db: Session = Depends(get_db)):
    if hasattr(user, "status_code"):
        return user
    delete_student(db, student_id)
    return RedirectResponse(url="/admin/students", status_code=HTTP_302_FOUND)


# — CURSOS —
@router.get("/courses", response_class=HTMLResponse)
def admin_manage_courses(
    request: Request,
    edit_id: int = None,
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    courses = list_courses(db)
    course_to_edit = None
    if edit_id:
        course_to_edit = get_course(db, edit_id)

    return templates.TemplateResponse("admin/courses.html", {
        "request": request,
        "courses": courses,
        "course_to_edit": course_to_edit
    })


@router.post("/courses", response_class=RedirectResponse)
def admin_post_course(
    request: Request,
    id: int = Form(None),
    title: str = Form(...),
    monthly_fee: float = Form(15000.0),
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    if id:
        update_course(db, CourseUpdate(id=id, title=title, monthly_fee=monthly_fee))
    else:
        create_course(db, CourseCreate(title=title, monthly_fee=monthly_fee))

    return RedirectResponse(url="/admin/courses", status_code=HTTP_302_FOUND)


@router.get("/courses/delete/{course_id}", response_class=RedirectResponse)
def admin_delete_course(course_id: int, user=Depends(ensure_admin), db: Session = Depends(get_db)):
    if hasattr(user, "status_code"):
        return user
    delete_course(db, course_id)
    return RedirectResponse(url="/admin/courses", status_code=HTTP_302_FOUND)


# — INSCRIPCIONES —
@router.get("/enrollments", response_class=HTMLResponse)
def admin_manage_enrollments(
    request: Request,
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    students = list_students(db)
    courses = list_courses(db)
    enrollments = list_enrollments(db)

    return templates.TemplateResponse("admin/enrollments.html", {
        "request": request,
        "students": students,
        "courses": courses,
        "enrollments": enrollments
    })


@router.post("/enrollments", response_class=RedirectResponse)
def admin_post_enrollment(
    request: Request,
    student_id: int = Form(...),
    course_id: int = Form(...),
    status: str = Form("activo"),
    user=Depends(ensure_admin),
    db: Session = Depends(get_db)
):
    if hasattr(user, "status_code"):
        return user

    create_enrollment(db, EnrollmentCreate(student_id=student_id, course_id=course_id, status=status))
    return RedirectResponse(url="/admin/enrollments", status_code=HTTP_302_FOUND)


@router.get("/enrollments/delete/{enrollment_id}", response_class=RedirectResponse)
def admin_delete_enrollment(enrollment_id: int, user=Depends(ensure_admin), db: Session = Depends(get_db)):
    if hasattr(user, "status_code"):
        return user
    delete_enrollment(db, enrollment_id)
    return RedirectResponse(url="/admin/enrollments", status_code=HTTP_302_FOUND)


# — FACTURACIÓN (PAGOS) —
@router.get("/invoices", response_class=HTMLResponse)
def admin_invoices(request: Request, user=Depends(ensure_admin), db: Session = Depends(get_db)):
    if hasattr(user, "status_code"):
        return user

    students = list_students(db)
    dues_data = []
    for s in students:
        sub, rec, tot = calculate_due_for_student(db, s.id)
        next_sub, next_rec, next_tot = calculate_next_month_due_for_student(db, s.id)
        dues_data.append({
            "student": s,
            "subtotal": sub,
            "recargo": rec,
            "total": tot,
            "next_sub": next_sub,
            "next_rec": next_rec,
            "next_total": next_tot
        })

    return templates.TemplateResponse("admin/invoices.html", {
        "request": request,
        "dues_data": dues_data
    })
