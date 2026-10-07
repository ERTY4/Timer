import time
import tkinter as tk
from tkinter import ttk


class TimerApp:
    def __init__(self, root: tk.Tk) -> None:

        self.root = root

        self.is_running = False
        self.phase = "work"
        self.end_time = 0

        self.work_seconds = 0
        self.rest_seconds = 0

        self.timer_check = tk.StringVar()
        self.timer_check.set("0-0")

        self.time_output = tk.StringVar()
        self.time_output.set("00:00:00")

        self.work_check = tk.StringVar()
        self.rest_check = tk.StringVar()

        self.work_rest_change = tk.StringVar()
        self.work_rest_change.set("Work")

        # Checks when the user writes in entries
        self.work_check.trace_add("write", self.update_timer_preview)
        self.rest_check.trace_add("write", self.update_timer_preview)

        # Create the interface
        self.create_widgets()

    def parse_input(self, input_str: str) -> int:
        """Checks the raw input of the user and returns 0 if the input is not under constraints"""
        input_str = input_str.strip()

        if not input_str:
            return 0
        try:
            minutes = int(input_str)
            seconds = minutes * 60
            if seconds <= 0 or seconds > 43200:
                return 0

            return minutes
        except ValueError:
            return 0

    def update_timer_preview(self, *args: str) -> None:
        """Dynamically changes the expected time that will pass when typing in entries."""
        try:
            work_input = self.parse_input(self.work_check.get())
            rest_input = self.parse_input(self.rest_check.get())

            work_h, work_m = divmod(work_input, 60)
            rest_h, rest_m = divmod(rest_input, 60)

            start_time = f"{work_h:02d}:{work_m:02d}"

            end_h = rest_h + work_h
            end_m = rest_m + work_m

            if rest_m + work_m >= 60:
                end_h += 1
                end_m = (rest_m + work_m) % 60
            end_time = f"{end_h:02d}:{end_m:02d}"

            formatted_string = f"{start_time}-{end_time}"
            self.timer_check.set(formatted_string)
        except (ValueError, ZeroDivisionError):
            self.timer_check.set("00:00-00:00")

    def create_widgets(self) -> None:
        """Initiates the GUI in Tkinter."""

        main_frame = ttk.Frame(self.root, padding=30, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        self.current_timer = ttk.Label(
            main_frame,
            textvariable=self.work_rest_change,
            font=("Courier", 16, "bold"),
            foreground="#bb0000",
        )
        self.current_timer.pack()
        timer_preview = ttk.Label(
            main_frame,
            textvariable=self.timer_check,
            font=("Courier", 25, "bold"),
        )
        timer_preview.pack()

        timer_label = ttk.Label(
            main_frame,
            textvariable=self.time_output,
            font=("Courier", 36, "bold"),
        )
        timer_label.pack()

        work_label = ttk.Label(main_frame, text="Enter the working time (minutes)")
        work_label.pack(anchor="w", pady=(0, 5))

        work_time = ttk.Entry(main_frame, textvariable=self.work_check)
        work_time.insert(0, "5")
        work_time.pack(fill="x", pady=(0, 20))

        rest_label = ttk.Label(main_frame, text="Enter the resting time (minutes)")
        rest_label.pack(anchor="w", pady=(0, 5))

        rest_time = ttk.Entry(main_frame, textvariable=self.rest_check)
        rest_time.insert(0, "5")
        rest_time.pack(fill="x", pady=(0, 20))

        start_stop_button = ttk.Button(
            main_frame,
            text="Start/Stop timer",
            command=self.toggle_timer,
        )
        start_stop_button.pack(fill="x")

        # Style section
        style = ttk.Style()
        style.theme_use("clam")
        self.root.wm_attributes("-toolwindow", True)  # type: ignore
        self.root.configure(bg="#f7fafc")

        APP_BG = "#f8fafc"
        self.root.configure(bg=APP_BG)

        style.configure(
            "TLabel", font=("Segoe UI", 12), foreground="#334155", background=APP_BG
        )
        style.configure(
            "TEntry",
            font=("Segoe UI", 11),
            foreground="#334155",
            fieldbackground="#ffffff",
            padding=8,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#ffffff",
            background="#3b82f6",
            padding=8,
            borderwidth=0,
            relief="flat",
        )
        style.configure("TFrame", background=APP_BG)

        style.map(
            "TButton",
            background=[("pressed", "#1d4ed8"), ("active", "#2563eb")],
            foreground=[("pressed", "#e2e8f0")],
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", "#3b82f6"), ("hover", "#cbd5e1")],
            lightcolor=[("focus", "#3b82f6")],
            darkcolor=[("focus", "#3b82f6")],
        )

        self.root.after(100, lambda: self.parse_input("1"))

    def tick(self) -> None:
        """Calculates time based on time.perf_counter() and decreases it.\n ..
        Allows switching between work and rest timers"""
        if not self.is_running:
            return
        remaining = self.end_time - time.perf_counter()

        if remaining > 0:
            display_time = int(remaining)

            all_minutes, display_seconds = divmod(display_time, 60)
            display_hours, display_minutes = divmod(all_minutes, 60)
            formatted_string = (
                f"{display_hours:02d}:{display_minutes:02d}:{display_seconds:02d}"
            )
            self.time_output.set(formatted_string)
            self.root.after(50, self.tick)
        else:
            if self.phase == "rest":
                self.is_running = False
                self.time_output.set("00:00:00")
                self.current_timer.config(foreground="#004d66")
                self.work_rest_change.set("Timer has ended.")
                return

            self.current_timer.config(foreground="#00bb38")
            self.work_rest_change.set("Rest")
            self.phase = "rest"
            self.end_time = time.perf_counter() + self.rest_seconds
            self.root.after(50, self.tick)

    def toggle_timer(self) -> None:
        """Toggles the timer on and off.
        \n Checks for inputs and gives them to tick using self."""
        if self.is_running:
            self.is_running = False
            self.time_output.set("00:00:00")

            self.current_timer.config(foreground="#bb0000")
            self.work_rest_change.set("Work")
            return
        else:
            work_mins = self.parse_input(self.work_check.get())
            rest_mins = self.parse_input(self.rest_check.get())

            if work_mins == 0 or rest_mins == 0:
                return
            self.work_seconds = work_mins * 60
            self.rest_seconds = rest_mins * 60

            self.phase = "work"

            self.end_time = time.perf_counter() + self.work_seconds
            self.is_running = True
            self.root.after(50, self.tick)


# Start Program
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Timer")

    app = TimerApp(root)

    root.mainloop()
