from pathlib import Path

import pytest

from ascii_birthday.payload import (
    BirthdayPayload,
    PayloadError,
    append_payload,
    default_output_filename,
    make_payload,
    read_payload_from_executable,
    sanitize_name_for_filename,
)


def test_payload_round_trip(tmp_path: Path) -> None:
    exe = tmp_path / "runner.exe"
    exe.write_bytes(b"fake exe")

    append_payload(exe, BirthdayPayload(name="Avery", age=40))

    payload = read_payload_from_executable(exe)
    assert payload.name == "Avery"
    assert payload.age == 40
    assert payload.greeting() == "Happy 40th Birthday Avery"


def test_missing_payload_raises(tmp_path: Path) -> None:
    exe = tmp_path / "runner.exe"
    exe.write_bytes(b"fake exe")

    with pytest.raises(PayloadError, match="No birthday payload"):
        read_payload_from_executable(exe)


def test_default_filename_uses_name_age_scheme() -> None:
    assert default_output_filename("Ada Lovelace", "36") == "Ada_Lovelace_36_Birthday.exe"


def test_filename_sanitizes_windows_reserved_characters() -> None:
    assert sanitize_name_for_filename(' Al<e/x:a|?* ') == "Al_e_x_a"


@pytest.mark.parametrize("age", ["0", "151", "abc"])
def test_invalid_age_rejected(age: str) -> None:
    with pytest.raises(PayloadError):
        make_payload("Morgan", age)


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (1, "Happy 1st Birthday Morgan"),
        (2, "Happy 2nd Birthday Morgan"),
        (3, "Happy 3rd Birthday Morgan"),
        (4, "Happy 4th Birthday Morgan"),
        (11, "Happy 11th Birthday Morgan"),
        (12, "Happy 12th Birthday Morgan"),
        (13, "Happy 13th Birthday Morgan"),
        (21, "Happy 21st Birthday Morgan"),
        (22, "Happy 22nd Birthday Morgan"),
        (23, "Happy 23rd Birthday Morgan"),
        (111, "Happy 111th Birthday Morgan"),
    ],
)
def test_greeting_uses_ordinal_age(age: int, expected: str) -> None:
    assert BirthdayPayload(name="Morgan", age=age).greeting() == expected
