import csv
import io

import cache
import crud
from auth import get_current_user, require_write, router as auth_router
from background import bulk_delete_task, load_csv_task
from database import Base, engine, get_db
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from models import User
from schemas import (
    AvgGradeResponse,
    BulkDeleteRequest,
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
    SubjectUpdate,
)
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API — Background Tasks & Caching")
app.include_router(auth_router)

AuthDep = Depends(get_current_user)
WriteDep = Depends(require_write)


@app.post("/faculties/", response_model=FacultyResponse, status_code=201, dependencies=[WriteDep])
def create_faculty(data: FacultyCreate, db: Session = Depends(get_db)):
    obj = crud.create_faculty(db, data.name)
    cache.invalidate("faculties:*", "analytics:*")
    return obj


@app.get("/faculties/", response_model=list[FacultyResponse], dependencies=[AuthDep])
def get_faculties(db: Session = Depends(get_db)):
    key = "faculties:all"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [FacultyResponse.model_validate(f).model_dump() for f in crud.get_all_faculties(db)]
    cache.set_value(key, data)
    return data


@app.get("/faculties/{faculty_id}", response_model=FacultyResponse, dependencies=[AuthDep])
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    key = f"faculties:{faculty_id}"
    if (hit := cache.get(key)) is not None:
        return hit
    obj = crud.get_faculty(db, faculty_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Faculty not found")
    data = FacultyResponse.model_validate(obj).model_dump()
    cache.set_value(key, data)
    return data


@app.put("/faculties/{faculty_id}", response_model=FacultyResponse, dependencies=[WriteDep])
def update_faculty(faculty_id: int, data: FacultyUpdate, db: Session = Depends(get_db)):
    obj = crud.update_faculty(db, faculty_id, data.name)
    if not obj:
        raise HTTPException(status_code=404, detail="Faculty not found")
    cache.invalidate("faculties:*", "analytics:*")
    return obj


@app.delete("/faculties/{faculty_id}", status_code=204, dependencies=[WriteDep])
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db, faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")
    cache.invalidate("faculties:*", "analytics:*")


@app.post("/subjects/", response_model=SubjectResponse, status_code=201, dependencies=[WriteDep])
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    obj = crud.create_subject(db, data.name)
    cache.invalidate("subjects:*", "analytics:*")
    return obj


@app.get("/subjects/", response_model=list[SubjectResponse], dependencies=[AuthDep])
def get_subjects(db: Session = Depends(get_db)):
    key = "subjects:all"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [SubjectResponse.model_validate(s).model_dump() for s in crud.get_all_subjects(db)]
    cache.set_value(key, data)
    return data


@app.get("/subjects/{subject_id}", response_model=SubjectResponse, dependencies=[AuthDep])
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    key = f"subjects:{subject_id}"
    if (hit := cache.get(key)) is not None:
        return hit
    obj = crud.get_subject(db, subject_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Subject not found")
    data = SubjectResponse.model_validate(obj).model_dump()
    cache.set_value(key, data)
    return data


@app.put("/subjects/{subject_id}", response_model=SubjectResponse, dependencies=[WriteDep])
def update_subject(subject_id: int, data: SubjectUpdate, db: Session = Depends(get_db)):
    obj = crud.update_subject(db, subject_id, data.name)
    if not obj:
        raise HTTPException(status_code=404, detail="Subject not found")
    cache.invalidate("subjects:*", "analytics:*")
    return obj


@app.delete("/subjects/{subject_id}", status_code=204, dependencies=[WriteDep])
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    if not crud.delete_subject(db, subject_id):
        raise HTTPException(status_code=404, detail="Subject not found")
    cache.invalidate("subjects:*", "analytics:*")


@app.post("/students/", response_model=StudentResponse, status_code=201, dependencies=[WriteDep])
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    obj = crud.create_student(db, data.last_name, data.first_name)
    cache.invalidate("students:*", "analytics:*")
    return obj


@app.get("/students/", response_model=list[StudentResponse], dependencies=[AuthDep])
def get_students(db: Session = Depends(get_db)):
    key = "students:all"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [StudentResponse.model_validate(s).model_dump() for s in crud.get_all_students(db)]
    cache.set_value(key, data)
    return data


@app.get("/students/{student_id}", response_model=StudentResponse, dependencies=[AuthDep])
def get_student(student_id: int, db: Session = Depends(get_db)):
    key = f"students:{student_id}"
    if (hit := cache.get(key)) is not None:
        return hit
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    data = StudentResponse.model_validate(obj).model_dump()
    cache.set_value(key, data)
    return data


@app.put("/students/{student_id}", response_model=StudentResponse, dependencies=[WriteDep])
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_student(db, student_id, data.last_name, data.first_name)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    cache.invalidate("students:*", "analytics:*")
    return obj


@app.delete("/students/{student_id}", status_code=204, dependencies=[WriteDep])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    cache.invalidate("students:*", "analytics:*")


@app.post("/grades/", response_model=GradeResponse, status_code=201, dependencies=[WriteDep])
def create_grade(data: GradeCreate, db: Session = Depends(get_db)):
    obj = crud.create_grade(db, data.student_id, data.faculty_id, data.subject_id, data.grade)
    cache.invalidate("grades:*", "analytics:*")
    return obj


@app.get("/grades/", response_model=list[GradeResponse], dependencies=[AuthDep])
def get_grades(db: Session = Depends(get_db)):
    key = "grades:all"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [GradeResponse.model_validate(g).model_dump() for g in crud.get_all_grades(db)]
    cache.set_value(key, data)
    return data


@app.get("/grades/{grade_id}", response_model=GradeResponse, dependencies=[AuthDep])
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    key = f"grades:{grade_id}"
    if (hit := cache.get(key)) is not None:
        return hit
    obj = crud.get_grade(db, grade_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Grade not found")
    data = GradeResponse.model_validate(obj).model_dump()
    cache.set_value(key, data)
    return data


@app.put("/grades/{grade_id}", response_model=GradeResponse, dependencies=[WriteDep])
def update_grade(grade_id: int, data: GradeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_grade(db, grade_id, data.grade)
    if not obj:
        raise HTTPException(status_code=404, detail="Grade not found")
    cache.invalidate("grades:*", "analytics:*")
    return obj


@app.delete("/grades/{grade_id}", status_code=204, dependencies=[WriteDep])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grade(db, grade_id):
        raise HTTPException(status_code=404, detail="Grade not found")
    cache.invalidate("grades:*", "analytics:*")


@app.post("/data/load", dependencies=[WriteDep])
def load_data(background_tasks: BackgroundTasks, filepath: str = "students.csv"):
    background_tasks.add_task(load_csv_task, filepath)
    return {"detail": "Data loading started in background", "file": filepath}


@app.delete("/data/bulk", dependencies=[WriteDep])
def bulk_delete(data: BulkDeleteRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(bulk_delete_task, data.table, data.ids)
    return {"detail": f"Bulk deletion of {len(data.ids)} record(s) from '{data.table}' started in background"}


@app.get("/analytics/students/by-faculty/{faculty_name}", response_model=list[StudentResponse], dependencies=[AuthDep])
def students_by_faculty(faculty_name: str, db: Session = Depends(get_db)):
    key = f"analytics:students_by_faculty:{faculty_name}"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [StudentResponse.model_validate(s).model_dump() for s in crud.get_students_by_faculty(db, faculty_name)]
    cache.set_value(key, data)
    return data


@app.get("/analytics/subjects/unique", response_model=list[SubjectResponse], dependencies=[AuthDep])
def unique_subjects(db: Session = Depends(get_db)):
    key = "analytics:unique_subjects"
    if (hit := cache.get(key)) is not None:
        return hit
    data = [SubjectResponse.model_validate(s).model_dump() for s in crud.get_unique_subjects(db)]
    cache.set_value(key, data)
    return data


@app.get("/analytics/students/failing/{subject_name}", response_model=list[FailingStudentResponse], dependencies=[AuthDep])
def failing_students(subject_name: str, db: Session = Depends(get_db)):
    key = f"analytics:failing:{subject_name}"
    if (hit := cache.get(key)) is not None:
        return hit
    data = crud.get_failing_students_by_subject(db, subject_name)
    serialized = [
        {"student": StudentResponse.model_validate(row["student"]).model_dump(), "grade": row["grade"]}
        for row in data
    ]
    cache.set_value(key, serialized)
    return serialized


@app.get("/analytics/faculties/{faculty_name}/avg-grade", response_model=AvgGradeResponse, dependencies=[AuthDep])
def avg_grade_by_faculty(faculty_name: str, db: Session = Depends(get_db)):
    key = f"analytics:avg_grade:{faculty_name}"
    if (hit := cache.get(key)) is not None:
        return hit
    avg = crud.get_avg_grade_by_faculty(db, faculty_name)
    if avg is None:
        raise HTTPException(status_code=404, detail="Faculty not found or has no grades")
    data = {"faculty": faculty_name, "avg_grade": round(avg, 2)}
    cache.set_value(key, data)
    return data


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
