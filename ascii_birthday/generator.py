from __future__ import annotations

import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ascii_birthday.payload import (
    PayloadError,
    append_payload,
    default_output_filename,
    make_payload,
)

APP_TITLE = "ASCII Birthday"
WINDOW_WIDTH = 580
WINDOW_HEIGHT = 380


def app_base_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[1]


def runner_stub_path() -> Path:
    candidates = [
        app_base_path() / "runner_stub.exe",
        Path(__file__).resolve().parents[1] / "dist" / "runner_stub.exe",
        Path(__file__).resolve().parents[1] / "build" / "runner_stub.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("runner_stub.exe was not found. Run scripts/build.ps1 first.")


class GeneratorApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        self.filename_var = tk.StringVar(value="Birthday.exe")
        self.status_var = tk.StringVar(value="Enter a name and age to generate a birthday exe.")

        self.build_ui()
        self.bind_events()
        self.refresh_filename()

    def build_ui(self) -> None:
        self.root.configure(bg="#101820")
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Hint.TLabel", foreground="#526071")

        ttk.Label(frame, text="ASCII Birthday Generator", style="Title.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 16)
        )

        ttk.Label(frame, text="Name").grid(row=1, column=0, sticky="w", pady=6)
        name_entry = ttk.Entry(frame, textvariable=self.name_var, width=38)
        name_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=6)
        name_entry.focus_set()

        ttk.Label(frame, text="Age").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Spinbox(frame, from_=1, to=150, textvariable=self.age_var, width=8).grid(
            row=2, column=1, sticky="w", pady=6
        )

        ttk.Label(frame, text="Output folder").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=self.output_dir_var, width=38).grid(
            row=3, column=1, sticky="ew", pady=6
        )
        ttk.Button(frame, text="Browse", command=self.choose_output_dir).grid(
            row=3, column=2, sticky="e", padx=(8, 0), pady=6
        )

        ttk.Label(frame, text="Generated file").grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=self.filename_var, state="readonly", width=38).grid(
            row=4, column=1, columnspan=2, sticky="ew", pady=6
        )

        ttk.Button(frame, text="Generate EXE", command=self.generate).grid(
            row=5, column=1, sticky="e", pady=(22, 8)
        )
        ttk.Button(frame, text="Exit", command=self.root.destroy).grid(
            row=5, column=2, sticky="e", padx=(8, 0), pady=(22, 8)
        )

        ttk.Label(frame, textvariable=self.status_var, style="Hint.TLabel", wraplength=500).grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(10, 0)
        )

        frame.columnconfigure(1, weight=1)

    def bind_events(self) -> None:
        self.name_var.trace_add("write", lambda *_args: self.refresh_filename())
        self.age_var.trace_add("write", lambda *_args: self.refresh_filename())
        self.root.bind("<Return>", lambda _event: self.generate())

    def refresh_filename(self) -> None:
        try:
            self.filename_var.set(default_output_filename(self.name_var.get(), self.age_var.get()))
        except PayloadError:
            name = self.name_var.get().strip() or "Name"
            age = self.age_var.get().strip() or "Age"
            self.filename_var.set(f"{name}_{age}_Birthday.exe")

    def choose_output_dir(self) -> None:
        selected = filedialog.askdirectory(
            initialdir=self.output_dir_var.get() or str(Path.home()),
            title="Choose output folder",
        )
        if selected:
            self.output_dir_var.set(selected)

    def generate(self) -> None:
        try:
            payload = make_payload(self.name_var.get(), self.age_var.get())
            output_dir = Path(self.output_dir_var.get()).expanduser()
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / default_output_filename(payload.name, payload.age)
            shutil.copyfile(runner_stub_path(), output_path)
            append_payload(output_path, payload)
        except (OSError, PayloadError, FileNotFoundError) as exc:
            messagebox.showerror(APP_TITLE, str(exc))
            self.status_var.set(str(exc))
            return

        self.status_var.set(f"Created {output_path}")
        messagebox.showinfo(APP_TITLE, f"Created:\n{output_path}")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    GeneratorApp().run()


if __name__ == "__main__":
    main()
