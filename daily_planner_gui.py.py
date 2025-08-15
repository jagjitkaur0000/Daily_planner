import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
from datetime import datetime, timedelta

# 🧠 Plan Generator Logic
def time_diff(start, end):
    FMT = "%H:%M"
    tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    return int(tdelta.total_seconds() // 3600)

def generate_plan(goals, wake, sleep):
    try:
        hours = time_diff(wake, sleep)
        if hours <= 0:
            raise ValueError
    except:
        messagebox.showerror("Invalid Time", "Make sure sleep time is after wake-up time.")
        return []

    plan = []
    random.shuffle(goals)
    blocks = hours // (len(goals) + 2)

    current = datetime.strptime(wake, "%H:%M")

    for goal in goals:
        end = current + timedelta(hours=blocks)
        plan.append(f"{current.strftime('%H:%M')} - {end.strftime('%H:%M')} ➤ {goal}")
        current = end
        current += timedelta(minutes=30)  # 30 min break

    plan.append(f"{current.strftime('%H:%M')} - {sleep} ➤ Free Time / Relaxation")
    return plan

# 🎨 GUI Layout
def generate_and_display():
    name = entry_name.get().strip()
    goals_raw = entry_goals.get().strip()
    wake = entry_wake.get().strip()
    sleep = entry_sleep.get().strip()

    if not all([name, goals_raw, wake, sleep]):
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    goals = [g.strip() for g in goals_raw.split(",")]
    plan = generate_plan(goals, wake, sleep)

    if plan:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"🗓️ Hello {name}, here is your AI-generated plan:\n\n")
        for p in plan:
            result_text.insert(tk.END, p + "\n")

# 🪟 Main Window
root = tk.Tk()
root.title("Daily Planner - AI Routine Generator")
root.geometry("500x600")

# 🔠 Input Fields
tk.Label(root, text="Your Name").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Goals (comma separated)").pack()
entry_goals = tk.Entry(root, width=40)
entry_goals.pack()

tk.Label(root, text="Wake-up Time (HH:MM)").pack()
entry_wake = tk.Entry(root, width=40)
entry_wake.pack()

tk.Label(root, text="Sleep Time (HH:MM)").pack()
entry_sleep = tk.Entry(root, width=40)
entry_sleep.pack()

# ⚡ Button
tk.Button(root, text="Generate Plan", command=generate_and_display, bg="green", fg="white").pack(pady=10)

# 📄 Result Output
result_text = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
result_text.pack(pady=10)

# 🚀 Start GUI
root.mainloop()
