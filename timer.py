import tkinter as tk
import time

root = tk.Tk()
root.title = "Focus Timer"

apps = []
timer_id = ""
running = False

def fmt(seconds):
    total_ms = int(seconds * 1000)
    hours, ms = divmod(total_ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:02d}"
    return f"{minutes:02d}:{secs:02d}.{ms:03d}"

def start_timer(event=None):
    global running
    if running:
        return
    running = True
    start = time.perf_counter()
    tick(start)
def stop_timer(event=None):
    global timer_id
    global running
    if not running:
        return
    running = False
    root.after_cancel(timer_id)

def tick(start):
    global timer_id
    timer = time.perf_counter() - start
    clock.config(text=fmt(timer))
    timer_id = root.after(10, tick, start)

if __name__ == "__main__":
    clock = tk.Label(root, text="00:00.00", font=("Roboto", 35))
    clock.pack()

    root.bind("<space>", start_timer)
    root.bind("<p>", stop_timer)

    root.mainloop()