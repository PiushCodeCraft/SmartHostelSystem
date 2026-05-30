"""
logger.py - Unified logger for the Smart Hostel System.

Usage (in any recognition file):
    from utils.logger import log_info, log_warn, log_error

    log_info("face-recognition", "Aarav Mehta recognised")
    log_warn("camera", "Low light detected on Cam 3")
    log_error("db-conn", "Connection timeout")
"""

from datetime import datetime
from database.database import get_connection


def _write(level: str, source: str, message: str):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO system_logs (level, source, message) VALUES (%s, %s, %s)",
            (level, source, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Logger] DB write failed: {e}")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] [{source}] {message}")


def log_info(source: str, message: str):  _write("INFO",  source, message)
def log_warn(source: str, message: str):  _write("WARN",  source, message)
def log_error(source: str, message: str): _write("ERROR", source, message)
