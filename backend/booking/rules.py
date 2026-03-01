from dataclasses import dataclass

@dataclass
class BookingRules:
    timezone: str = "India/Kolkata"
    work_days: set[int] = None
    day_start: str = "09:00"
    day_end: str = "17:00"
    lunch_start: str = "12:00"
    lunch_end: str = "13:00"
    duration_minutes: int = 30
    buffer_minutes: int = 5

def get_rules() -> BookingRules:
    return BookingRules(work_days={0, 1, 2, 3, 4})