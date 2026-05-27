import csv
import io

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import crud
from auth import get_current_user, require_write, router as auth_router
from database import Base, engine, get_db
from models import User
from schemas import (
    AvgGradeResponse,
    FailingStudentResponse,
    FacultyCreate,
    FacultyResponse,
    FacultyUpdate,
    GradeCreate,
    GradeResponse,
    GradeUpdate,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    SubjectCreate,
    SubjectResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API with Auth")
app.include_router(auth_router)

AuthDep = Depends(get_current_user)
WriteDep = Depends(require_write)


@app.post("/faculties/", response_model=FacultyResponse, status_code=201, dependencies=[WriteDep])
def create_faculty(data: FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db, data.name)


@app.get("/faculties/", response_model=list[FacultyResponse], dependencies=[AuthDep])
def get_faculties(db: Session = Depends(get_db)):
    return crud.get_all_faculties(db)


@app.get("/faculties/{faculty_id}", response_model=FacultyResponse, dependencies=[AuthDep])
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    obj = crud.get_faculty(db, faculty_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return obj


@app.put("/faculties/{faculty_id}", response_model=FacultyResponse, dependencies=[WriteDep])
def update_faculty(faculty_id: int, data: FacultyUpdate, db: Session = Depends(get_db)):
    obj = crud.update_faculty(db, faculty_id, data.name)
    if not obj:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return obj


@app.delete("/faculties/{faculty_id}", status_code=204, dependencies=[WriteDep])
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db, faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")


@app.post("/subjects/", response_model=SubjectResponse, status_code=201, dependencies=[WriteDep])
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, data.name)


@app.get("/subjects/", response_model=list[SubjectResponse], dependencies=[AuthDep])
def get_subjects(db: Session = Depends(get_db)):
    return crud.get_all_subjects(db)


@app.get("/subjects/{subject_id}", response_model=SubjectResponse, dependencies=[AuthDep])
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    obj = crud.get_subject(db, subject_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return obj


@app.post("/students/", response_model=StudentResponse, status_code=201, dependencies=[WriteDep])
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, data.last_name, data.first_name)


@app.get("/students/", response_model=list[StudentResponse], dependencies=[AuthDep])
def get_students(db: Session = Depends(get_db)):
    return crud.get_all_students(db)


@app.get("/students/{student_id}", response_model=StudentResponse, dependencies=[AuthDep])
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@app.put("/students/{student_id}", response_model=StudentResponse, dependencies=[WriteDep])
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_student(db, student_id, data.last_name, data.first_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@app.delete("/students/{student_id}", status_code=204, dependencies=[WriteDep])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")


@app.post("/grades/", response_model=GradeResponse, status_code=201, dependencies=[WriteDep])
def create_grade(data: GradeCreate, db: Session = Depends(get_db)):
    return crud.create_grade(db, data.student_id, data.faculty_id, data.subject_id, data.grade)


@app.get("/grades/", response_model=list[GradeResponse], dependencies=[AuthDep])
def get_grades(db: Session = Depends(get_db)):
    return crud.get_all_grades(db)


@app.get("/grades/{grade_id}", response_model=GradeResponse, dependencies=[AuthDep])
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    obj = crud.get_grade(db, grade_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Grade not found")
    return obj


@app.put("/grades/{grade_id}", response_model=GradeResponse, dependencies=[WriteDep])
def update_grade(grade_id: int, data: GradeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_grade(db, grade_id, data.grade)
    if not obj:
        raise HTTPException(status_code=404, detail="Grade not found")
    return obj


@app.delete("/grades/{grade_id}", status_code=204, dependencies=[WriteDep])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grade(db, grade_id):
        raise HTTPException(status_code=404, detail="Grade not found")


@app.post("/data/load", dependencies=[WriteDep])
def load_data(filepath: str = "students.csv", db: Session = Depends(get_db)):
    count = crud.load_from_csv(db, filepath)
    return {"loaded": count}


@app.get("/analytics/students/by-faculty/{faculty_name}", response_model=list[StudentResponse], dependencies=[AuthDep])
def students_by_faculty(faculty_name: str, db: Session = Depends(get_db)):
    return crud.get_students_by_faculty(db, faculty_name)


@app.get("/analytics/subjects/unique", response_model=list[SubjectResponse], dependencies=[AuthDep])
def unique_subjects(db: Session = Depends(get_db)):
    return crud.get_unique_subjects(db)


@app.get("/analytics/students/failing/{subject_name}", response_model=list[FailingStudentResponse], dependencies=[AuthDep])
def failing_students(subject_name: str, db: Session = Depends(get_db)):
    return crud.get_failing_students_by_subject(db, subject_name)


@app.get("/analytics/faculties/{faculty_name}/avg-grade", response_model=AvgGradeResponse, dependencies=[AuthDep])
def avg_grade_by_faculty(faculty_name: str, db: Session = Depends(get_db)):
    avg = crud.get_avg_grade_by_faculty(db, faculty_name)
    if avg is None:
        raise HTTPException(status_code=404, detail="Faculty not found or has no grades")
    return {"faculty": faculty_name, "avg_grade": round(avg, 2)}


@app.get("/data/export", dependencies=[AuthDep])
def export_data(db: Session = Depends(get_db)):
    rows = crud.export_to_csv_data(db)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Фамилия", "Имя", "Факультет", "Курс", "Оценка"])
    writer.writeheader()
    writer.writerows(rows)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_export.csv"},
    )
