import os
import sys
from datetime import datetime

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from database.database import run_query


def mark_attendance(student_name: str):

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Get previous attendance
    query = """
    SELECT status
    FROM attendance_logs
    WHERE student_name = %s
    ORDER BY id DESC
    LIMIT 1
    """

    rows = run_query(query, (student_name,))

    # IN / OUT logic
    if not rows:
        status = "IN"
    else:
        last_status = rows[0]["status"]
        status = "OUT" if last_status == "IN" else "IN"

    # Insert attendance
    insert_query = """
    INSERT INTO attendance_logs
    (student_name, status, date, time)
    VALUES (%s, %s, %s, %s)
    """

    run_query(
        insert_query,
        (student_name, status, date, time),
        fetch=False
    )

    # Logger
    try:
        from utils.logger import log_info

        log_info(
            "attendance",
            f"{student_name} marked {status} at {time}"
        )

    except Exception:
        pass

    print(
        f"[Attendance] {student_name} -> {status} at {time}"
    )