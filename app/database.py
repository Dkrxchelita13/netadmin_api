import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "netadmin.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30
    )
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS dispositivos (
                ip TEXT PRIMARY KEY,
                hostname TEXT NOT NULL,
                mac TEXT NOT NULL,
                tipo TEXT NOT NULL,
                sistema TEXT NOT NULL,
                estado TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_cambios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                accion TEXT NOT NULL,
                ip TEXT NOT NULL,
                datos_anteriores TEXT,
                datos_nuevos TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'consulta',
                token TEXT UNIQUE
            )
            """
        )

        connection.commit()