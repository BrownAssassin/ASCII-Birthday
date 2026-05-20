"""Shared payload helpers for generated birthday executables."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
import struct
from pathlib import Path

MAGIC = b"ASCII_BDAY_PAYLOAD_V1"
LENGTH_STRUCT = struct.Struct("<I")
MAX_PAYLOAD_BYTES = 16 * 1024
DEFAULT_EXE_SUFFIX = "Birthday.exe"


class PayloadError(ValueError):
    """Raised when a birthday payload cannot be read or validated."""


@dataclass(frozen=True)
class BirthdayPayload:
    name: str
    age: int
    message_version: int = 1

    def age_label(self) -> str:
        return ordinal_age(self.age)

    def greeting(self) -> str:
        return f"Happy {self.age_label()} Birthday {self.name}"


def ordinal_age(age: int) -> str:
    if 10 <= age % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(age % 10, "th")
    return f"{age}{suffix}"


def validate_name(name: str) -> str:
    cleaned = " ".join(name.strip().split())
    if not cleaned:
        raise PayloadError("Name is required.")
    if len(cleaned) > 80:
        raise PayloadError("Name must be 80 characters or fewer.")
    return cleaned


def validate_age(age: str | int) -> int:
    try:
        value = int(str(age).strip())
    except ValueError as exc:
        raise PayloadError("Age must be a whole number.") from exc

    if value < 1 or value > 150:
        raise PayloadError("Age must be between 1 and 150.")
    return value


def make_payload(name: str, age: str | int) -> BirthdayPayload:
    return BirthdayPayload(name=validate_name(name), age=validate_age(age))


def payload_to_bytes(payload: BirthdayPayload) -> bytes:
    data = {
        "name": payload.name,
        "age": payload.age,
        "message_version": payload.message_version,
    }
    return json.dumps(data, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def payload_from_bytes(raw: bytes) -> BirthdayPayload:
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PayloadError("Birthday payload is not valid JSON.") from exc

    try:
        name = data["name"]
        age = data["age"]
    except KeyError as exc:
        raise PayloadError("Birthday payload is missing required data.") from exc

    message_version = int(data.get("message_version", 1))
    return BirthdayPayload(
        name=validate_name(str(name)),
        age=validate_age(age),
        message_version=message_version,
    )


def append_payload(executable_path: Path, payload: BirthdayPayload) -> None:
    raw = payload_to_bytes(payload)
    if len(raw) > MAX_PAYLOAD_BYTES:
        raise PayloadError("Birthday payload is too large.")

    with executable_path.open("ab") as file:
        file.write(raw)
        file.write(LENGTH_STRUCT.pack(len(raw)))
        file.write(MAGIC)


def read_payload_from_executable(executable_path: Path) -> BirthdayPayload:
    with executable_path.open("rb") as file:
        file.seek(0, 2)
        file_size = file.tell()
        trailer_size = len(MAGIC) + LENGTH_STRUCT.size
        if file_size < trailer_size:
            raise PayloadError("No birthday payload was found.")

        file.seek(file_size - len(MAGIC))
        if file.read(len(MAGIC)) != MAGIC:
            raise PayloadError("No birthday payload was found.")

        file.seek(file_size - len(MAGIC) - LENGTH_STRUCT.size)
        payload_size = LENGTH_STRUCT.unpack(file.read(LENGTH_STRUCT.size))[0]
        if payload_size < 1 or payload_size > MAX_PAYLOAD_BYTES:
            raise PayloadError("Birthday payload length is invalid.")

        payload_start = file_size - len(MAGIC) - LENGTH_STRUCT.size - payload_size
        if payload_start < 0:
            raise PayloadError("Birthday payload length is invalid.")

        file.seek(payload_start)
        return payload_from_bytes(file.read(payload_size))


def sanitize_name_for_filename(name: str) -> str:
    cleaned = validate_name(name)
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", cleaned)
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip(" ._")
    return cleaned or "Birthday"


def default_output_filename(name: str, age: str | int) -> str:
    return f"{sanitize_name_for_filename(name)}_{validate_age(age)}_{DEFAULT_EXE_SUFFIX}"
