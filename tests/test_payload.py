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
    assert payload.greeting() == "Happy 40 Birthday Avery"


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
