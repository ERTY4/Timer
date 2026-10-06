import queue
import threading
import tkinter as tk
from tkinter import ttk


# Signal for the timer to stop, Also a queue for tkinter to handle threading
stop_signal = threading.Event()
time_queue = queue.Queue()


# Function section


def change_time_from_queue():
    """Instantly gets the time from queue and changes it. \n
    Also checks if the queue is empty"""
    try:
        while True:
            new_time = time_queue.get_nowait()
            time_output.set(new_time)
    except queue.Empty:
        pass


def parse_input(input: any, entry: str) -> tuple:
    """Check the if the input is valid.\n
    input takes in the time for both rest and work times, while entry is just the name."""
    input = input.strip()

    if not input:
        return (False, f"{entry} is empty!")
    try:
        seconds = int(input)
        if seconds <= 0:
            return (False, f"{entry} must be bigger than 0!")

        return (True, seconds)
    except ValueError:
        return (False, f"{entry} is not a valid number")


def start_timer(work_time: any, rest_time: any):
    """Start the timer."""
    global timer_thread
    if timer_thread and timer_thread.is_alive():
        stop_signal.set()
        timer_thread.join()

    stop_signal.clear()

    def update_queue(time: int):
        """Updates the timer display."""
        while not stop_signal.is_set():
            time -= 1
            time_queue.put(time)

            change_time_from_queue()
            stop_signal.wait(1)

    is_work, worktime = parse_input(work_time, "Working Time Entry")
    is_rest, restime = parse_input(rest_time, "Resting Time Entry")

    if is_rest and is_work:
        pass

    timer_thread = threading.Thread(target=update_queue(1))


def stop_timer():
    """Stop the timer."""
    stop_signal.set()


# Tkinter section
root = tk.Tk()
root.geometry("400x400")
root.title("Timer")


# GUI section

main_frame = ttk.Frame(root, padding=30, style="TFrame")
main_frame.pack(fill="both", expand=True)

time_output = tk.StringVar()
time_output.set("00:00")

dynamic_label = ttk.Label(
    main_frame,
    textvariable=time_output,
)
dynamic_label.pack()

input_label = ttk.Label(main_frame, text="Enter the working time (minutes)")
input_label.pack(anchor="w", pady=(0, 5))

work_time = ttk.Entry(main_frame)
work_time.insert(0, "5")
work_time.pack(fill="x", pady=(0, 20))

input_label = ttk.Label(main_frame, text="Enter the resting time (minutes)")
input_label.pack(anchor="w", pady=(0, 5))

rest_time = ttk.Entry(main_frame)
rest_time.insert(0, "5")
rest_time.pack(fill="x", pady=(0, 20))


start_button = ttk.Button(main_frame, text="Start timer", command=start_timer)
start_button.pack(fill="x")

stop_button = ttk.Button(main_frame, text="Start timer", command=stop_timer)
stop_button.pack(fill="x")


# Style section
style = ttk.Style()
style.theme_use("clam")
root.wm_attributes("-toolwindow", True)
root.configure(bg="#f7fafc")

APP_BG = "#f8fafc"
root.configure(bg=APP_BG)

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
    background="#3b82f6",  # Light blue (Normal)
    padding=8,
    borderwidth=0,
    relief="flat",
)
style.configure("TFrame", background=APP_BG)

# Style for when the button is hovered or clicked
style.map(
    "TButton",
    background=[
        ("pressed", "#1d4ed8"),
        ("active", "#2563eb"),
    ],
    foreground=[("pressed", "#e2e8f0")],
)
style.map(
    "TEntry",
    bordercolor=[
        ("focus", "#3b82f6"),
        ("hover", "#cbd5e1"),
    ],
    lightcolor=[("focus", "#3b82f6")],
    darkcolor=[("focus", "#3b82f6")],
)
root.after(100, change_time_from_queue)
root.mainloop()
stop_signal.set()
