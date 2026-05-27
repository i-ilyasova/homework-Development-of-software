import csv

from database import Base, SessionLocal, engine
from models import Faculty, Grade, Student, Subject


def load_students_csv(filepath: str) -> None:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        faculties: dict[str, Faculty] = {}
        subjects: dict[str, Subject] = {}
        students: dict[tuple, Student] = {}

        for row in reader:
            faculty_name = row["Факультет"].strip()
            subject_name = row["Курс"].strip()
            last_name = row["Фамилия"].strip()
            first_name = row["Имя"].strip()
            grade_value = int(row["Оценка"].strip())

            if faculty_name not in faculties:
                faculty = Faculty(name=faculty_name)
                session.add(faculty)
                session.flush()
                faculties[faculty_name] = faculty

            if subject_name not in subjects:
                subject = Subject(name=subject_name)
                session.add(subject)
                session.flush()
                subjects[subject_name] = subject

            student_key = (last_name, first_name)
            if student_key not in students:
                student = Student(last_name=last_name, first_name=first_name)
                session.add(student)
                session.flush()
                students[student_key] = student

            grade = Grade(
                student_id=students[student_key].id,
                faculty_id=faculties[faculty_name].id,
                subject_id=subjects[subject_name].id,
                grade=grade_value,
            )
            session.add(grade)

        session.commit()

    session.close()
    print("Данные успешно загружены")


if __name__ == "__main__":
    load_students_csv("students.csv")
