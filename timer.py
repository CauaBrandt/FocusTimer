import tkinter as tk
import time

root = tk.Tk()
root.title = "Focus Timer"
root.configure(
    bg="#010101",
    border=0
)
root.attributes("-transparentcolor", "#010101")
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
    return f"{minutes:02d}:{secs:02d}.{ms:03d}"

def start_timer(event=None):
    global start, running
    if running:
        return
    running = True
    start = time.perf_counter()
    tick()
def stop_timer(event=None):
    global timer_id, running
    if not running:
        start_timer()
        return
    running = False
    root.after_cancel(timer_id)
def reset_timer(event=None):
    global timer
    stop_timer()
    clock.config(text="00:00.00")
    timer = 0

def tick():
    global timer
    global timer_id
    global start
    now = time.perf_counter()
    timer += now - start
    start = now
    clock.config(text=fmt(timer))
    timer_id = root.after(10, tick)

if __name__ == "__main__":
    clock = tk.Label(
        root, 
        text="00:00.00", 
        font=("Roboto", 35),
        fg="#ffffff",
        bg="#010101"
    )
    clock.pack()

    root.bind("<space>", start_timer)
    root.bind("<P>", stop_timer)
    root.bind("<p>", stop_timer)
    root.bind("<Insert>", reset_timer)
    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()