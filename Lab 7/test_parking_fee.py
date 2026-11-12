import re
from string import ascii_letters, digits

from hypothesis import example, given, strategies as st

from parking_fee import format_plate, hourly_rate, minutes_parked


inputs = st.one_of(st.text(), st.none(), st.integers(), st.binary(), st.lists(st.text()))
minute_of_day = st.integers(min_value=0, max_value=1439)
letters = st.text(ascii_letters, min_size=2, max_size=2)
district = st.text(digits, min_size=2, max_size=2)
serial = st.text(digits, min_size=4, max_size=4)


@given(inputs)
def test_minutes_parked_no_crash(value):
    result = minutes_parked(value)
    assert result is None or (isinstance(value, str) and 0 <= result < 1440)


@given(minute_of_day, minute_of_day)
@example(0, 1439)
@example(1439, 0)
@example(0, 0)
def test_same_day_duration(entry, exit_time):
    interval = (
        f"{entry // 60:02}:{entry % 60:02}-"
        f"{exit_time // 60:02}:{exit_time % 60:02}"
    )
    expected = exit_time - entry if exit_time >= entry else None
    assert minutes_parked(interval) == expected


@given(st.integers(24, 99), st.integers(60, 99))
def test_out_of_range_clock_fields(hour, minute):
    assert minutes_parked(f"00:00-{hour}:00") is None
    assert minutes_parked(f"00:{minute}-23:59") is None


@given(inputs)
def test_hourly_rate_no_crash(value):
    expected_rates = {"bike": 10, "car": 30, "truck": 60}
    expected = expected_rates.get(value.strip().lower()) if isinstance(value, str) else None
    assert hourly_rate(value) == expected


@given(st.sampled_from([("bike", 10), ("car", 30), ("truck", 60)]), st.booleans())
def test_known_vehicle_rates(vehicle_and_rate, uppercase):
    vehicle, expected = vehicle_and_rate
    assert hourly_rate(" " + (vehicle.upper() if uppercase else vehicle) + " ") == expected


@given(inputs)
def test_format_plate_no_crash(value):
    result = format_plate(value)
    if result is not None:
        assert isinstance(value, str)
        assert re.fullmatch(r"[A-Z]{2} [0-9]{2} [A-Z]{2} [0-9]{4}", result)
        assert result.replace(" ", "") == value.strip().replace(" ", "").upper()


@given(letters, district, letters, serial)
def test_plate_formatting(state, area, series, number):
    compact = state + area + series + number
    expected = f"{state.upper()} {area} {series.upper()} {number}"
    assert format_plate(compact) == expected
    assert format_plate(expected) == expected
    assert format_plate(compact + "0") is None
