import tkinter as tk
import time

root = tk.Tk()
root.title = "Focus Timer"
root.configure(
    bg="black",
)
root.attributes("-topmost", True)
root.overrideredirect(True)

apps = []
timer = 0
timer_id = ""
running = False

def fmt(seconds):
    total_ms = int(seconds * 1000)
    hours, ms = divmod(total_ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"
    elif minutes:
        return f"{minutes:02d}:{secs:02d}.{ms:03d}"
    return f"{secs:02d}.{ms:03d}"

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
    clock.config(fg="#14ff1e")
    start = time.perf_counter()
    tick()
def stop_timer(event=None):
    global timer_id, running
    if not running:
        start_timer()
        return
    running = False
    clock.config(fg="#00508c")
    root.after_cancel(timer_id)
def reset_timer(event=None):
    global timer, running
    if running:
        stop_timer()
    clock.config(text="00.00", fg="#285064")
    timer = 0

def tick():
    global timer, timer_id, start
    now = time.perf_counter()
    timer += now - start
    start = now
    clock.config(text=fmt(timer))
    timer_id = root.after(10, tick)

if __name__ == "__main__":
    clock = tk.Label(
        root,
        text="00.00", 
        font=("Consolas", 35),
        fg="#285064",
        bg="#010101"
    )
    clock.pack()

    root.bind("<Button-1>", grab_timer)
    root.bind("<B1-Motion>", move_timer)
    root.bind("<space>", start_timer)
    root.bind("<P>", stop_timer)
    root.bind("<p>", stop_timer)
    root.bind("<Insert>", reset_timer)
    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()