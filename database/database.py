import mysql.connector
import streamlit as st
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# ── Connection ────────────────────────────────────────────────────────────────

def get_connection():
    """Return a MySQL connection. Reads credentials from .env or defaults."""
    return mysql.connector.connect(
        host     = os.getenv("DB_HOST",     "localhost"),
        port     = int(os.getenv("DB_PORT", "3306")),
        user     = os.getenv("DB_USER",     "root"),
        password = os.getenv("DB_PASSWORD", "root"),
        database = os.getenv("DB_NAME",     "smart_hostel"),
    )

def run_query(sql: str, params=None, fetch=True):
    """Execute a query and optionally return rows as list-of-dicts."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            result = cursor.fetchall()
            cursor.close(); conn.close()
            return result
        else:
            conn.commit()
            cursor.close(); conn.close()
            return True
    except Exception as e:
        # Improve error visibility: include SQL and params in the error message
        try:
            param_text = repr(params) if params is not None else "()"
        except Exception:
            param_text = "(unrepresentable)"
        st.error(f"Database error while executing SQL:\n{sql}\nparams: {param_text}\nerror: {e}")
        return [] if fetch else False


# ── Auth ──────────────────────────────────────────────────────────────────────

def verify_login(username: str, password: str) -> bool:
    rows = run_query(
        "SELECT id FROM admin_users WHERE username=%s AND password_hash=%s",
        (username, password),
    )
    return len(rows) > 0


# ── Dashboard ─────────────────────────────────────────────────────────────────

def get_total_students() -> int:
    rows = run_query("SELECT COUNT(*) AS cnt FROM students WHERE is_active=1")
    return rows[0]["cnt"] if rows else 0

def get_present_today() -> int:
    rows = run_query(
        "SELECT COUNT(*) AS cnt FROM attendance WHERE date=%s AND status='Present'",
        (date.today(),),
    )
    return rows[0]["cnt"] if rows else 0

def get_unknown_faces_today() -> int:
    rows = run_query(
        "SELECT COUNT(*) AS cnt FROM unknown_faces WHERE DATE(detected_at)=%s AND is_resolved=0",
        (date.today(),),
    )
    return rows[0]["cnt"] if rows else 0

def get_camera_counts() -> dict:
    rows = run_query(
        "SELECT status, COUNT(*) AS cnt FROM cameras GROUP BY status"
    )
    result = {"Online": 0, "Offline": 0}
    for r in rows:
        result[r["status"]] = r["cnt"]
    return result

def get_weekly_attendance() -> list:
    """Returns attendance count for each of the last 7 days."""
    rows = run_query("""
        SELECT date, COUNT(*) AS cnt
        FROM attendance
        WHERE date >= %s AND status='Present'
        GROUP BY date
        ORDER BY date
    """, (date.today() - timedelta(days=6),))
    day_map = {r["date"]: r["cnt"] for r in rows}
    result = []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        result.append({"date": d, "count": day_map.get(d, 0)})
    return result

def get_recent_activity(limit=8) -> list:
    rows = run_query(
        "SELECT timestamp, level, source, message FROM system_logs ORDER BY timestamp DESC LIMIT %s",
        (limit,),
    )
    return rows


# ── Students ──────────────────────────────────────────────────────────────────

def get_all_students(search="", class_filter="", status_filter="") -> list:
    sql = """
        SELECT s.student_id, s.first_name, s.last_name, s.room_number, s.class,
               s.guardian_phone,
               COALESCE(a.status, 'Absent') AS status,
               COALESCE(TIME_FORMAT(a.check_in,'%h:%i %p'), 'N/A') AS last_seen
        FROM students s
        LEFT JOIN attendance a ON s.student_id = a.student_id AND a.date = CURDATE()
        WHERE s.is_active = 1
    """
    params = []
    if search:
        sql += " AND (s.first_name LIKE %s OR s.last_name LIKE %s OR s.student_id LIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if class_filter and class_filter != "All Classes":
        sql += " AND s.class = %s"
        params.append(class_filter)
    if status_filter and status_filter != "All Status":
        sql += " AND COALESCE(a.status,'Absent') = %s"
        params.append(status_filter)
    sql += " ORDER BY s.student_id"
    return run_query(sql, params)

def get_classes() -> list:
    rows = run_query("SELECT DISTINCT class FROM students ORDER BY class")
    return [r["class"] for r in rows]

def add_student(data: dict) -> bool:
    rows = run_query("SELECT COUNT(*) AS cnt FROM students")
    next_id = f"STU{(rows[0]['cnt'] + 1):03d}"
    return run_query("""
        INSERT INTO students
            (student_id, first_name, last_name, roll_number, room_number, class,
             gender, dob, guardian_name, guardian_phone, guardian_email, address, notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        next_id, data["first_name"], data["last_name"], next_id,
        data["room_number"], data["class"], data["gender"], data["dob"],
        data["guardian_name"], data["guardian_phone"], data["guardian_email"],
        data["address"], data["notes"],
    ), fetch=False)

def delete_student(student_id: str) -> bool:
    return run_query(
        "UPDATE students SET is_active=0 WHERE student_id=%s",
        (student_id,), fetch=False
    )


# ── Attendance / Analytics ────────────────────────────────────────────────────

def get_monthly_attendance(year: int) -> list:
    rows = run_query("""
        SELECT MONTH(date) AS month, COUNT(*) AS cnt
        FROM attendance
        WHERE YEAR(date)=%s AND status='Present'
        GROUP BY MONTH(date)
        ORDER BY month
    """, (year,))
    month_map = {r["month"]: r["cnt"] for r in rows}
    return [month_map.get(m, 0) for m in range(1, 13)]

def get_hourly_entry_today() -> list:
    rows = run_query("""
        SELECT HOUR(check_in) AS hr, COUNT(*) AS cnt
        FROM attendance
        WHERE date=CURDATE() AND check_in IS NOT NULL
        GROUP BY HOUR(check_in)
        ORDER BY hr
    """)
    hour_map = {r["hr"]: r["cnt"] for r in rows}
    return [hour_map.get(h, 0) for h in range(24)]

def get_30day_trend() -> list:
    rows = run_query("""
        SELECT date, COUNT(*) AS cnt
        FROM attendance
        WHERE date >= %s AND status='Present'
        GROUP BY date
        ORDER BY date
    """, (date.today() - timedelta(days=29),))
    day_map = {r["date"]: r["cnt"] for r in rows}
    return [day_map.get(date.today() - timedelta(days=29-i), 0) for i in range(30)]

def get_analytics_summary() -> dict:
    avg = run_query("""
        SELECT ROUND(AVG(daily_cnt),0) AS avg_daily FROM (
            SELECT date, COUNT(*) AS daily_cnt FROM attendance
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND status='Present'
            GROUP BY date
        ) t
    """)
    alerts = run_query("""
        SELECT COUNT(*) AS cnt FROM system_logs
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        AND level IN ('WARN','ERROR')
    """)
    peak = run_query("""
        SELECT DAYNAME(date) AS day, COUNT(*) AS cnt
        FROM attendance WHERE status='Present'
        GROUP BY DAYNAME(date)
        ORDER BY cnt DESC LIMIT 1
    """)
    return {
        "avg_daily": int(avg[0]["avg_daily"]) if avg and avg[0]["avg_daily"] else 0,
        "alerts":    alerts[0]["cnt"] if alerts else 0,
        "peak_day":  peak[0]["day"] if peak else "N/A",
    }


# ── Live Logs ─────────────────────────────────────────────────────────────────

def get_logs(level_filter="", search="", limit=50) -> list:
    sql = "SELECT timestamp, level, source, message FROM system_logs WHERE 1=1"
    params = []
    if level_filter and level_filter != "all":
        sql += " AND level=%s"
        params.append(level_filter.upper())
    if search:
        sql += " AND (source LIKE %s OR message LIKE %s)"
        params += [f"%{search}%", f"%{search}%"]
    sql += " ORDER BY timestamp DESC LIMIT %s"
    params.append(limit)
    return run_query(sql, params)

def insert_log(level: str, source: str, message: str):
    run_query(
        "INSERT INTO system_logs (level, source, message) VALUES (%s,%s,%s)",
        (level, source, message), fetch=False
    )


# ── Unknown Faces ─────────────────────────────────────────────────────────────

def get_unknown_faces(resolved=False) -> list:
    rows = run_query(
        "SELECT * FROM unknown_faces WHERE is_resolved=%s ORDER BY detected_at DESC",
        (1 if resolved else 0,),
    )
    return rows

def resolve_face(face_id: int) -> bool:
    return run_query(
        "UPDATE unknown_faces SET is_resolved=1, resolved_at=NOW() WHERE id=%s",
        (face_id,), fetch=False
    )


# ── Current Status ────────────────────────────────────────────────────────────

def get_location_status() -> list:
    return run_query("SELECT * FROM location_status ORDER BY location_name")

def get_cameras() -> list:
    return run_query("SELECT * FROM cameras ORDER BY camera_name")


# ── Reports ───────────────────────────────────────────────────────────────────

def get_attendance_report(from_date, to_date) -> list:
    return run_query("""
        SELECT s.student_id, s.first_name, s.last_name, s.class, s.room_number,
               a.date, a.check_in, a.check_out, a.status, a.location
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.date BETWEEN %s AND %s
        ORDER BY a.date DESC, s.student_id
    """, (from_date, to_date))

def get_unknown_faces_report(from_date, to_date) -> list:
    return run_query("""
        SELECT * FROM unknown_faces
        WHERE DATE(detected_at) BETWEEN %s AND %s
        ORDER BY detected_at DESC
    """, (from_date, to_date))
