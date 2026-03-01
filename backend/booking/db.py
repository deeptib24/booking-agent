import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "bookings.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          contact TEXT NOT NULL,
          service TEXT NOT NULL,
          start_iso TEXT NOT NULL,
          end_iso TEXT NOT NULL,
          status TEXT NOT NULL
        )
        """
    )
    con.commit()
    con.close()

def insert_appointment(appt: dict):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO appointments (id, name, contact, service, start_iso, end_iso, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (appt["id"], appt["name"], appt["contact"], appt["service"], appt["start_iso"], appt["end_iso"], appt["status"]),
    )
    con.commit()
    con.close()

def get_appointments_between(start_iso: str, end_iso: str) -> list[dict]:
    con = connect()
    cur = con.cursor()
    cur.execute(
        "SELECT id, name, contact, service, start_iso, end_iso, status FROM appointments WHERE start_iso < ? AND end_iso > ? AND status = 'booked'",
        (end_iso, start_iso),
    )
    rows = cur.fetchall()
    con.close()
    return [
        {"id": r[0], "name": r[1], "contact": r[2], "service": r[3], "start_iso": r[4], "end_iso": r[5], "status": r[6]}
        for r in rows
    ]

def get_appointment(appt_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "SELECT id, name, contact, service, start_iso, end_iso, status FROM appointments WHERE id = ?",
        (appt_id,),
    )
    row = cur.fetchone()
    con.close()
    if not row:
        return None
    return {"id": row[0], "name": row[1], "contact": row[2], "service": row[3], "start_iso": row[4], "end_iso": row[5], "status": row[6]}

def update_appointment_time(appt_id: str, start_iso: str, end_iso: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "UPDATE appointments SET start_iso = ?, end_iso = ? WHERE id = ?",
        (start_iso, end_iso, appt_id),
    )
    con.commit()
    con.close()

def cancel_appointment(appt_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "UPDATE appointments SET status = 'cancelled' WHERE id = ?",
        (appt_id,),
    )
    con.commit()
    con.close()