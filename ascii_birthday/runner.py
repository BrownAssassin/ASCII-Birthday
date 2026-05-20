from __future__ import annotations

import random
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import font as tkfont

from pyfiglet import Figlet

from ascii_birthday.payload import BirthdayPayload, PayloadError, read_payload_from_executable

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
BACKGROUND = "#05070a"
TEXT_COLOR = "#66ff99"
TEXT_SHADOW = "#123820"
CONFETTI_COLORS = [
    "#ff5c8a",
    "#ffd166",
    "#48cae4",
    "#9bff7a",
    "#f15bb5",
    "#cdb4db",
    "#ffffff",
]
CONFETTI_CHARS = ["*", "+", "x", "o", "#", "@", "%", "$", "!", "~"]


@dataclass
class ConfettiPiece:
    x: float
    y: float
    dx: float
    dy: float
    char: str
    color: str
    size: int


def load_payload() -> BirthdayPayload:
    if getattr(sys, "frozen", False):
        executable_path = Path(sys.executable)
    else:
        executable_path = Path(__file__)

    try:
        return read_payload_from_executable(executable_path)
    except (OSError, PayloadError):
        return BirthdayPayload(name="Friend", age=100)


def clean_ascii_block(block: str) -> list[str]:
    lines = [line.rstrip() for line in block.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def render_ascii_message(payload: BirthdayPayload) -> str:
    figlet = Figlet(font="standard", width=180)
    message_parts = [f"Happy {payload.age_label()}", "Birthday", payload.name]
    lines: list[str] = []

    for part in message_parts:
        if lines:
            lines.append("")
        lines.extend(clean_ascii_block(figlet.renderText(part)))

    return "\n".join(lines)


def fit_ascii_font(root: tk.Tk, ascii_art: str) -> tuple[str, int, str]:
    max_width = WINDOW_WIDTH - 96
    max_height = WINDOW_HEIGHT - 110
    lines = ascii_art.splitlines()

    for size in range(16, 6, -1):
        candidate = tkfont.Font(root=root, family="Consolas", size=size, weight="bold")
        width = max(candidate.measure(line) for line in lines)
        height = candidate.metrics("linespace") * len(lines)
        if width <= max_width and height <= max_height:
            return ("Consolas", size, "bold")

    return ("Consolas", 7, "bold")


class BirthdayWindow:
    def __init__(self, payload: BirthdayPayload) -> None:
        self.root = tk.Tk()
        self.root.title("ASCII Birthday")
        self.root.configure(bg=BACKGROUND)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.bind("<Key>", self.close)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.payload = payload
        self.ascii_art = render_ascii_message(payload)
        self.confetti = [self.make_piece(random.uniform(-WINDOW_HEIGHT, WINDOW_HEIGHT)) for _ in range(170)]

        self.root.update_idletasks()
        self.font = fit_ascii_font(self.root, self.ascii_art)
        self.draw()

    def make_piece(self, y: float | None = None) -> ConfettiPiece:
        return ConfettiPiece(
            x=random.uniform(0, WINDOW_WIDTH),
            y=random.uniform(-WINDOW_HEIGHT, 0) if y is None else y,
            dx=random.uniform(-1.3, 1.3),
            dy=random.uniform(1.3, 4.8),
            char=random.choice(CONFETTI_CHARS),
            color=random.choice(CONFETTI_COLORS),
            size=random.randint(12, 24),
        )

    def close(self, _event: tk.Event | None = None) -> None:
        self.root.destroy()

    def draw(self) -> None:
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill=BACKGROUND, outline="")

        for piece in self.confetti:
            self.canvas.create_text(
                piece.x,
                piece.y,
                text=piece.char,
                fill=piece.color,
                font=("Consolas", piece.size, "bold"),
            )
            piece.x += piece.dx
            piece.y += piece.dy
            if piece.y > WINDOW_HEIGHT + 30 or piece.x < -30 or piece.x > WINDOW_WIDTH + 30:
                replacement = self.make_piece()
                piece.x = replacement.x
                piece.y = replacement.y
                piece.dx = replacement.dx
                piece.dy = replacement.dy
                piece.char = replacement.char
                piece.color = replacement.color
                piece.size = replacement.size

        self.canvas.create_text(
            WINDOW_WIDTH // 2 + 4,
            WINDOW_HEIGHT // 2 + 4,
            text=self.ascii_art,
            fill=TEXT_SHADOW,
            font=self.font,
            justify="center",
            anchor="center",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=self.ascii_art,
            fill=TEXT_COLOR,
            font=self.font,
            justify="center",
            anchor="center",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 32,
            text="Press any key to close",
            fill="#94a3b8",
            font=("Consolas", 12),
            anchor="center",
        )
        self.root.after(34, self.draw)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    BirthdayWindow(load_payload()).run()


if __name__ == "__main__":
    main()
