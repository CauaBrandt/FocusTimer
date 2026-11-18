import tkinter as tk
import time
import ctypes
import ctypes.wintypes
import psutil

root = tk.Tk()
root.title = "Focus Timer"
root.configure(bg="black")
root.attributes("-topmost", True)
root.overrideredirect(True)

TARGETS = ["Code.exe", "Claude.exe", "Anki.exe"]
user32 = ctypes.windll.user32
timer = 0
timer_id = ""
running = False

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

def start_timer(event=None):
    global start, running
    if running:
        return
    running = True
    main.config(fg="#14ff1e")
    small.config(fg="#14ff1e")
    start = time.perf_counter()
    tick()
def stop_timer(event=None):
    global timer_id, running
    if not running and event:
        start_timer()
        return
    running = False
    main.config(fg="#00508c")
    small.config(fg="#00508c")
    root.after_cancel(timer_id)
def reset_timer(event=None):
    global timer, running
    if running:
        stop_timer()
    main.config(text="00.00", fg="#285064")
    small.config(text="00.00", fg="#285064")
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
    if focused_app() not in TARGETS:
        if running:
            stop_timer(False)
    else:
        start_timer()
    root.after(10, check_timer)

if __name__ == "__main__":
    timer_frame = tk.Frame(
        root, 
        bg="black",
        padx=10,
        pady=5
    )
    timer_frame.pack(anchor="e")
    main = tk.Label(
        timer_frame,
        text="0.",
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
        text="00",
        font=("Consolas", 30),
        bg="black",
        fg="#285064",
        padx=0,
        anchor="e"
    )
    small.pack(side="left", anchor="s")

    root.bind("<Button-1>", grab_timer)
    root.bind("<B1-Motion>", move_timer)
    root.bind("<space>", start_timer)
    root.bind("<P>", stop_timer)
    root.bind("<p>", stop_timer)
    root.bind("<Insert>", reset_timer)
    root.bind("<Escape>", lambda e: root.destroy())

    check_timer()

    root.mainloop()