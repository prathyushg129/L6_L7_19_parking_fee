import re
from typing import Optional


RATES = {"bike": 10, "car": 30, "truck": 60}
CLOCK = r"([0-9]{1,2}):([0-9]{1,2})"
TIME_RANGE = re.compile(rf"{CLOCK}\s*-\s*{CLOCK}")
PLATE = re.compile(r"([A-Za-z]{2}) *([0-9]{2}) *([A-Za-z]{2}) *([0-9]{4})")


def minutes_parked(times: object) -> Optional[int]:
    """Return elapsed minutes for a same-day stay, or None for invalid input."""
    if not isinstance(times, str):
        return None
    match = TIME_RANGE.fullmatch(times.strip())
    if match is None:
        return None
    start_hour, start_minute, end_hour, end_minute = map(int, match.groups())
    if max(start_hour, end_hour) > 23 or max(start_minute, end_minute) > 59:
        return None
    start = 60 * start_hour + start_minute
    end = 60 * end_hour + end_minute
    return end - start if end >= start else None


def hourly_rate(vehicle: object) -> Optional[int]:
    """Look up the hourly rate, or return None for an unknown vehicle."""
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate: object) -> Optional[str]:
    """Format a plate like KA 01 AB 1234, or return None for invalid input."""
    if not isinstance(plate, str):
        return None
    match = PLATE.fullmatch(plate.strip())
    if match is None:
        return None
    return " ".join(match.groups()).upper()


def main():
    print("==== Running minutes_parked ====")
    times = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    minutes = minutes_parked(times)
    if minutes is None:
        print("Invalid time range. Enter two 24-hour times in same-day order.")
    else:
        print("Minutes Parked:", minutes)

    print("\n==== Running hourly_rate ====")
    vehicle = input("Enter vehicle type (bike/car/truck): ")
    rate = hourly_rate(vehicle)
    if rate is None:
        print("Unknown vehicle. Choose bike, car or truck.")
    else:
        print("Hourly Rate:", rate)

    print("\n==== Running format_plate ====")
    plate = input("Enter a number plate (e.g. ka01ab1234): ")
    formatted = format_plate(plate)
    if formatted is None:
        print("Invalid plate. Use the format KA01AB1234.")
    else:
        print("Formatted Plate:", formatted)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nInput ended.")
