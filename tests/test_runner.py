from ascii_birthday.payload import BirthdayPayload
from ascii_birthday.runner import render_ascii_message


def test_ascii_message_uses_ordinal_age(monkeypatch) -> None:
    rendered_parts = []

    class FakeFiglet:
        def __init__(self, **_kwargs) -> None:
            pass

        def renderText(self, text: str) -> str:
            rendered_parts.append(text)
            return f"{text}\n"

    monkeypatch.setattr("ascii_birthday.runner.Figlet", FakeFiglet)

    render_ascii_message(BirthdayPayload(name="Jordan", age=21))

    assert rendered_parts == ["Happy 21st", "Birthday", "Jordan"]


def test_ascii_message_rows_share_same_width() -> None:
    ascii_art = render_ascii_message(BirthdayPayload(name="Arshul", age=25))
    line_lengths = {len(line) for line in ascii_art.splitlines()}

    assert len(line_lengths) == 1
