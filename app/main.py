from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Student Marks API", version="1.0.0")

# In-memory store — no database needed
students_db: List[dict] = [
    {"id": 1, "name": "Alice Johnson", "subject": "Mathematics", "marks": 88},
    {"id": 2, "name": "Bob Smith",    "subject": "Science",      "marks": 75},
    {"id": 3, "name": "Carol White",  "subject": "English",      "marks": 92},
]
next_id = 4


class Student(BaseModel):
    name: str
    subject: str
    marks: int


# ── Health endpoint (used by Kubernetes liveness/readiness probes) ──────────
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "student-marks-api"}


# ── GET /students ────────────────────────────────────────────────────────────
@app.get("/students")
def get_all_students():
    """Return the full list of student records."""
    return {"students": students_db, "total": len(students_db)}


# ── GET /students/{id} ───────────────────────────────────────────────────────
@app.get("/students/{student_id}")
def get_student(student_id: int):
    """Return a single student by ID."""
    for s in students_db:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")


# ── POST /students ───────────────────────────────────────────────────────────
@app.post("/students", status_code=201)
def add_student(student: Student):
    """Add a new student record."""
    global next_id
    if not (0 <= student.marks <= 100):
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")
    new_record = {"id": next_id, **student.dict()}  # .dict() works in pydantic v1
    students_db.append(new_record)
    next_id += 1
    return new_record
