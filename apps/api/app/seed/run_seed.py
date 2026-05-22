from app.db.session import SessionLocal
from app.seed.phase2_seed import seed_phase2


def main() -> None:
    db = SessionLocal()
    try:
        seed_phase2(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
