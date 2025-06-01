# app/routes/landing.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.db import get_all_students, get_courses_for_student
from app.services.payments import calculate_total, create_payment_preference

import datetime
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "term": "",
            "message": "",
            "student": None,
            "courses": [],
            "surcharge": 0.0,
            "total": 0.0,
        },
    )


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, term: str = ""):
    students = get_all_students()
    message = ""
    student = None
    courses = []
    surcharge = 0.0
    total = 0.0

    if term:
        term_l = term.lower()
        matches = [
            s
            for s in students
            if term_l
            in " ".join(
                str(s[col]).lower()
                for col in ("name", "dni", "email", "status")
                if s[col]
            )
        ]

        if len(matches) == 1:
            student = matches[0]
            courses = get_courses_for_student(student["id"])
            subtotal = sum(fee for _, fee in courses)
            surcharge, total = calculate_total(subtotal)
        elif len(matches) > 1:
            message = "Se encontraron varias coincidencias."
        else:
            message = f"No se encontraron alumnos que coincidan con \"{term}\"."

    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "term": term,
            "message": message,
            "student": student,
            "courses": courses,
            "surcharge": surcharge,
            "total": total,
        },
    )


@router.get("/pay/{student_id}")
async def pay(student_id: int):
    # 1) Verificar que exista el alumno
    students = get_all_students()
    alumno = next((s for s in students if s["id"] == student_id), None)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # 2) Obtener cursos y calcular monto
    courses = get_courses_for_student(student_id)
    subtotal = sum(fee for _, fee in courses)
    surcharge, total = calculate_total(subtotal)

    # 3) Intentar crear la preferencia MP
    try:
        link_mp = create_payment_preference(student_id, alumno["name"], total)
    except ValueError as ve:
        # Error al no tener configurado MP_ACCESS_TOKEN
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        # Cualquier otro error al llamar al SDK
        # Podrías logear e imprimir e para depuración
        print("Error interno al crear preferencia MP:", e)
        raise HTTPException(status_code=500, detail="Error interno generando pago")

    if not link_mp:
        # No se obtuvo init_point ni sandbox_init_point
        raise HTTPException(
            status_code=500,
            detail="No se pudo generar el link de MercadoPago. Revisá MP_ACCESS_TOKEN y la respuesta de MP.",
        )

    # 4) Redirigir al init_point
    return RedirectResponse(url=link_mp)
