import uuid
from datetime import timedelta
from dateutil import tz
from dateutil.parser import parse, isoparse

from .rules import get_rules
from .availability import get_open_slots
from .db import insert_appointment, get_appointment, update_appointment_time, cancel_appointment

def suggest_slots(preferred_date_text: str) -> list[str]:
    rules = get_rules()
    zone = tz.gettz(rules.timezone)
    day = parse(preferred_date_text).replace(tzinfo=zone)
    return get_open_slots(day.isoformat(), count=4)

def book(name: str, contact: str, service: str, start_iso: str) -> dict:
    rules = get_rules()
    zone = tz.gettz(rules.timezone)
    start = isoparse(start_iso).astimezone(zone)
    end = start + timedelta(minutes=rules.duration_minutes)

    appt = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "contact": contact,
        "service": service,
        "start_iso": start.isoformat(),
        "end_iso": end.isoformat(),
        "status": "booked",
    }
    insert_appointment(appt)
    return appt

def reschedule(appt_id: str, new_start_iso: str) -> dict | None:
    appt = get_appointment(appt_id)
    if not appt or appt["status"] != "booked":
        return None

    rules = get_rules()
    zone = tz.gettz(rules.timezone)
    new_start = isoparse(new_start_iso).astimezone(zone)
    new_end = new_start + timedelta(minutes=rules.duration_minutes)

    update_appointment_time(appt_id, new_start.isoformat(), new_end.isoformat())
    appt["start_iso"] = new_start.isoformat()
    appt["end_iso"] = new_end.isoformat()
    return appt

def cancel(appt_id: str) -> bool:
    appt = get_appointment(appt_id)
    if not appt or appt["status"] != "booked":
        return False
    cancel_appointment(appt_id)
    return True