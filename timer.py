import tkinter as tk
import customtkinter as ctk
import time
import ctypes
import ctypes.wintypes
import psutil
import json


root = tk.Tk()
root.title("Focus Timer")
root.configure(bg="black")
root.attributes("-topmost", True)
root.overrideredirect(True)
 
DEFAULTS = {"targets": "", "topmost": True, "auto_start": False}

try:
    with open("settings.json", "r") as f:
        settings = {**DEFAULTS, **json.load(f)}
except (FileNotFoundError, json.JSONDecodeError):
    settings = DEFAULTS

TARGETS = settings["targets"]
topmost = tk.BooleanVar(value=settings["topmost"])
auto_start = tk.BooleanVar(value=settings["auto_start"])

user32 = ctypes.windll.user32
timer = 0
timer_id = ""
running = False

def save_settings(key, value):
    with open("settings.json", "w") as f:
        json.dump({**settings, key: value}, f, indent=4)

def focused_app():
    current_window = user32.GetForegroundWindow()
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(current_window, ctypes.byref(pid))
    try:
        return psutil.Process(pid.value).name()
    except psutil.Error:
        return "Error"

def fmt(seconds):
    total_ms = int(seconds * 1000)
    hours, ms = divmod(total_ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    ms //= 10
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}", f".{ms:02d}"
    elif minutes:
        return f"{minutes}:{secs:02d}", f".{ms:02d}"
    return f"{secs}", f".{ms:02d}"

def grab_timer(event):
    global drag_x, drag_y
    drag_x = event.x_root - root.winfo_x()
    drag_y = event.y_root - root.winfo_y()
def move_timer(event):
    x = event.x_root - drag_x
    y = event.y_root - drag_y
    root.geometry(f"+{x}+{y}")

def start_timer():
    global start, running
    if running:
        return
    running = True
    main.config(fg="#14ff1e")
    small.config(fg="#14ff1e")
    start = time.perf_counter()
    tick()
def stop_timer():
    global timer_id, running
    if not running:
        return
    running = False
    main.config(fg="#00508c")
    small.config(fg="#00508c")
    root.after_cancel(timer_id)
def reset_timer(event=None):
    global timer
    
    stop_timer()
    main.config(text="0", fg="#285064")
    small.config(text=".00", fg="#285064")
    timer = 0

def tick():
    global timer, timer_id, start, running
    now = time.perf_counter()
    timer += now - start
    start = now
    rest, ms = fmt(timer)
    main.config(text=rest)
    small.config(text=ms)
    timer_id = root.after(10, tick)
def check_timer():
    global running
    if not auto_start.get():
        return
    if focused_app() not in TARGETS:
        if running:
            stop_timer()
    else:
        start_timer()
    root.after(100, check_timer)

def show_menu(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def open_settings():
    win = tk.Toplevel(root, padx=10, pady=5)
    win.title("Settings")
    win.geometry("600x300")

    ctk.CTkLabel(win, text="Applications: ", font=("Consolas", 17), text_color="black").grid(row=0, column=0, stick="w")
    entry = ctk.CTkEntry(
        win,
        fg_color="#e6e6e6",
        text_color="black",
        font=("Consolas", 14),
        placeholder_text="Enter the app process name here.",
        border_width=0,
        width=30
    )
    entry.insert(0, " ".join(TARGETS))
    entry.grid(row=0, column=1, pady=(5,0), stick="ew")
    win.grid_columnconfigure(1, weight=1)

    def save():
        global TARGETS
        TARGETS = [target for target in entry.get().split(" ")]
        save_settings("targets", TARGETS)
        win.destroy()

    ctk.CTkButton(
        win, 
        text="Save", 
        command=save,
        text_color="#ffffff",
        fg_color="#2C7C17",
        corner_radius=10,
        width=120,
        height=30
    ).place(relx=1, rely=1, anchor="s", x=-60, y=-10)

if __name__ == "__main__":
    # Main Timer
    timer_frame = tk.Frame(
        root,
        bg="black",
        padx=10,
        pady=5
    )
    timer_frame.pack(anchor="e")
    main = tk.Label(
        timer_frame,
        text="0",
        font=("Consolas", 35),
        bg="black",
        fg="#285064",   
        width=7,
        padx=0,
        anchor="e"
    )
    main.pack(side="left", anchor="s")
    small = tk.Label(
        timer_frame,
        text=".00",
        font=("Consolas", 30),
        bg="black",
        fg="#285064",
        padx=0,
        anchor="e"
    )
    small.pack(side="left", anchor="s", pady=(0, 1))

    # Menu
    menu = tk.Menu(root, tearoff=0)

    def on_always_on_top():
        save_settings("topmost", topmost.get())
        root.attributes("-topmost", topmost.get())
    def on_auto_start():
        save_settings("auto_start", auto_start.get())
        check_timer()

    menu.add_checkbutton(label="Always on top", variable=topmost, command=on_always_on_top)
    menu.add_checkbutton(label="Auto start", variable=auto_start, command=on_auto_start)
    menu.add_command(label="Reset", command=reset_timer)
    menu.add_command(label="Settings", command=open_settings)
    menu.add_command(label="Exit", command=root.destroy)

    root.bind("<Button-1>", grab_timer)
    root.bind("<B1-Motion>", move_timer)
    root.bind("<Button-3>", show_menu)
    root.bind("<Insert>", reset_timer)
    root.bind("<Escape>", lambda e: root.destroy())

    check_timer()

    root.mainloop()