"""Initialize the SQLite database for the e-commerce application."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from database.models import db, migrate_schema


def init_database():
    app = create_app()
    database_file = PROJECT_ROOT / "database" / "ecommerce.db"
    database_file.parent.mkdir(parents=True, exist_ok=True)

    with app.app_context():
        db.create_all()
        migrate_schema()

    return database_file


if __name__ == "__main__":
    created_database = init_database()
    print(f"Database initialized at {created_database}")
