import tkinter as tk
import time

root = tk.Tk()
root.title = "Focus Timer"

apps = []
timer = 3590
start = time.perf_counter()

def format(seconds):
    total_ms = int(seconds * 1000)
    hours, ms = divmod(total_ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:02d}"
    return f"{minutes:02d}:{secs:02d}.{ms:02d}"

def tick():
    timer = time.perf_counter() - start
    clock.config(text=format(timer))
    root.after(10, tick)

if __name__ == "__main__":
    clock = tk.Label(root, text="00:00.00", font=("Arial", 35))
    clock.pack()

    root.mainloop()