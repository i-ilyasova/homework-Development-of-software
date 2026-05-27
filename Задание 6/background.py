import cache
import crud
from database import SessionLocal


def load_csv_task(filepath: str) -> None:
    db = SessionLocal()
    try:
        crud.load_from_csv(db, filepath)
        cache.invalidate("students:*", "grades:*", "faculties:*", "subjects:*", "analytics:*")
    finally:
        db.close()


def bulk_delete_task(table: str, ids: list[int]) -> None:
    db = SessionLocal()
    try:
        crud.bulk_delete(db, table, ids)
        cache.invalidate(f"{table}:*", "analytics:*")
    finally:
        db.close()
