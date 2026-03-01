import json
from fastapi.middleware.cors import CORSMiddleware
from dateutil import tz
from dateutil.parser import parse
from booking.ai_agent import run_agent
from fastapi import FastAPI
from pydantic import BaseModel

from booking.db import init_db
from booking.availability import get_open_slots
from booking.agent import book, reschedule, cancel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SlotIn(BaseModel):
    day_iso: str

class BookIn(BaseModel):
    name: str
    contact: str
    service: str
    start_iso: str

class RescheduleIn(BaseModel):
    appt_id: str
    new_start_iso: str

class CancelIn(BaseModel):
    appt_id: str

class ChatIn(BaseModel):
    message: str

@app.on_event("startup")
def startup():
    init_db()

@app.post("/availability")
def availability(payload: SlotIn):
    slots = get_open_slots(payload.day_iso, count=4)
    return {"slots": slots}

@app.post("/book")
def book_api(payload: BookIn):
    appt = book(payload.name, payload.contact, payload.service, payload.start_iso)
    return {"appointment": appt}

@app.post("/reschedule")
def reschedule_api(payload: RescheduleIn):
    appt = reschedule(payload.appt_id, payload.new_start_iso)
    if not appt:
        return {"ok": False, "message": "Appointment not found or not active"}
    return {"ok": True, "appointment": appt}

@app.post("/cancel")
def cancel_api(payload: CancelIn):
    ok = cancel(payload.appt_id)
    return {"ok": ok}

@app.post("/chat")
def chat(payload: ChatIn):
    answer = run_agent(payload.message, TOOLS, tool_handler)
    return {"answer": answer}

def tool_handler(name: str, arguments_json: str) -> str:
    args = json.loads(arguments_json or "{}")

    if name == "check_availability":
        day_text = args.get("day_text", "")
        timezone = args.get("timezone", "America/Chicago")
        zone = tz.gettz(timezone)
        day = parse(day_text).replace(tzinfo=zone)
        slots = get_open_slots(day.isoformat(), count=4)
        return json.dumps({"slots": slots})

    if name == "create_booking":
        appt = book(
            name=args["name"],
            contact=args["contact"],
            service=args["service"],
            start_iso=args["start_iso"],
        )
        return json.dumps({"appointment": appt})

    if name == "reschedule_booking":
        appt = reschedule(
            appt_id=args["appt_id"],
            new_start_iso=args["new_start_iso"],
        )
        if not appt:
            return json.dumps({"ok": False})
        return json.dumps({"ok": True, "appointment": appt})

    if name == "cancel_booking":
        ok = cancel(appt_id=args["appt_id"])
        return json.dumps({"ok": ok})

    return json.dumps({"error": "Unknown tool"})

TOOLS = [
    {
        "type": "function",
        "name": "check_availability",
        "description": "Find open slots for a given day in a timezone.",
        "parameters": {
            "type": "object",
            "properties": {
                "day_text": {"type": "string"},
                "timezone": {"type": "string"}
            },
            "required": ["day_text"]
        }
    },
    {
        "type": "function",
        "name": "create_booking",
        "description": "Create a booking after the user confirms a slot.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "contact": {"type": "string"},
                "service": {"type": "string"},
                "start_iso": {"type": "string"}
            },
            "required": ["name", "contact", "service", "start_iso"]
        }
    },
    {
        "type": "function",
        "name": "reschedule_booking",
        "description": "Reschedule an existing booking using confirmation ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "appt_id": {"type": "string"},
                "new_start_iso": {"type": "string"}
            },
            "required": ["appt_id", "new_start_iso"]
        }
    },
    {
        "type": "function",
        "name": "cancel_booking",
        "description": "Cancel an existing booking using confirmation ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "appt_id": {"type": "string"}
            },
            "required": ["appt_id"]
        }
    }
]