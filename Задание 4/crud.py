import csv

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Faculty, Grade, Student, Subject


def create_faculty(db: Session, name: str) -> Faculty:
    obj = Faculty(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_faculty(db: Session, faculty_id: int) -> Faculty | None:
    return db.get(Faculty, faculty_id)


def get_all_faculties(db: Session) -> list[Faculty]:
    return db.query(Faculty).all()


def update_faculty(db: Session, faculty_id: int, name: str) -> Faculty | None:
    obj = get_faculty(db, faculty_id)
    if not obj:
        return None
    obj.name = name
    db.commit()
    db.refresh(obj)
    return obj


def delete_faculty(db: Session, faculty_id: int) -> bool:
    obj = get_faculty(db, faculty_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_subject(db: Session, name: str) -> Subject:
    obj = Subject(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_subject(db: Session, subject_id: int) -> Subject | None:
    return db.get(Subject, subject_id)


def get_all_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).all()


def update_subject(db: Session, subject_id: int, name: str) -> Subject | None:
    obj = get_subject(db, subject_id)
    if not obj:
        return None
    obj.name = name
    db.commit()
    db.refresh(obj)
    return obj


def delete_subject(db: Session, subject_id: int) -> bool:
    obj = get_subject(db, subject_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_student(db: Session, last_name: str, first_name: str) -> Student:
    obj = Student(last_name=last_name, first_name=first_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def get_all_students(db: Session) -> list[Student]:
    return db.query(Student).all()


def update_student(db: Session, student_id: int, last_name: str, first_name: str) -> Student | None:
    obj = get_student(db, student_id)
    if not obj:
        return None
    obj.last_name = last_name
    obj.first_name = first_name
    db.commit()
    db.refresh(obj)
    return obj


def delete_student(db: Session, student_id: int) -> bool:
    obj = get_student(db, student_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_grade(db: Session, student_id: int, faculty_id: int, subject_id: int, grade: int) -> Grade:
    obj = Grade(student_id=student_id, faculty_id=faculty_id, subject_id=subject_id, grade=grade)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_grade(db: Session, grade_id: int) -> Grade | None:
    return db.get(Grade, grade_id)


def get_all_grades(db: Session) -> list[Grade]:
    return db.query(Grade).all()


def update_grade(db: Session, grade_id: int, grade: int) -> Grade | None:
    obj = get_grade(db, grade_id)
    if not obj:
        return None
    obj.grade = grade
    db.commit()
    db.refresh(obj)
    return obj


def delete_grade(db: Session, grade_id: int) -> bool:
    obj = get_grade(db, grade_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def get_students_by_faculty(db: Session, faculty_name: str) -> list[Student]:
    return (
        db.query(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .filter(Faculty.name == faculty_name)
        .distinct()
        .all()
    )


def get_unique_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).all()


def get_failing_students_by_subject(db: Session, subject_name: str) -> list[dict]:
    rows = (
        db.query(Student, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name, Grade.grade < 30)
        .all()
    )
    return [{"student": student, "grade": grade} for student, grade in rows]


def get_avg_grade_by_faculty(db: Session, faculty_name: str) -> float | None:
    return (
        db.query(func.avg(Grade.grade))
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .filter(Faculty.name == faculty_name)
        .scalar()
    )


def load_from_csv(db: Session, filepath: str) -> int:
    faculties: dict[str, Faculty] = {}
    subjects: dict[str, Subject] = {}
    students: dict[tuple, Student] = {}
    count = 0

    with open(filepath, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            faculty_name = row["Факультет"].strip()
            subject_name = row["Курс"].strip()
            last_name = row["Фамилия"].strip()
            first_name = row["Имя"].strip()
            grade_value = int(row["Оценка"].strip())

            if faculty_name not in faculties:
                existing = db.query(Faculty).filter(Faculty.name == faculty_name).first()
                faculties[faculty_name] = existing or Faculty(name=faculty_name)
                if not existing:
                    db.add(faculties[faculty_name])
                    db.flush()

            if subject_name not in subjects:
                existing = db.query(Subject).filter(Subject.name == subject_name).first()
                subjects[subject_name] = existing or Subject(name=subject_name)
                if not existing:
                    db.add(subjects[subject_name])
                    db.flush()

            student_key = (last_name, first_name)
            if student_key not in students:
                existing = db.query(Student).filter(
                    Student.last_name == last_name,
                    Student.first_name == first_name,
                ).first()
                students[student_key] = existing or Student(last_name=last_name, first_name=first_name)
                if not existing:
                    db.add(students[student_key])
                    db.flush()

            db.add(Grade(
                student_id=students[student_key].id,
                faculty_id=faculties[faculty_name].id,
                subject_id=subjects[subject_name].id,
                grade=grade_value,
            ))
            count += 1

    db.commit()
    return count


def export_to_csv_data(db: Session) -> list[dict]:
    rows = (
        db.query(Student, Faculty, Subject, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .all()
    )
    return [
        {
            "Фамилия": student.last_name,
            "Имя": student.first_name,
            "Факультет": faculty.name,
            "Курс": subject.name,
            "Оценка": grade,
        }
        for student, faculty, subject, grade in rows
    ]
