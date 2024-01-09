import tkinter as tk
from time import strftime, localtime
from datetime import datetime, time, timedelta
import winsound

class WorldClockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("World Clock")

        self.clock_label = tk.Label(self.master, font=('Arial', 80), bg='black', fg='white')
        self.clock_label.pack(padx=20, pady=20)

        locations = [("New York", 'America/New_York'), ("London", 'Europe/London'), ("Tokyo", 'Asia/Tokyo')]

        for location, timezone in locations:
            button = tk.Button(self.master, text=location, font=('Arial', 20), command=lambda tz=timezone: self.set_timezone(tz))
            button.pack(pady=5)

        self.update_time()

    def update_time(self):
        current_time = strftime('%H:%M:%S', localtime())
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_time)

    def set_timezone(self, timezone):
        current_time = datetime.now()
        formatted_time = current_time.astimezone(timezone).strftime('%H:%M:%S')
        self.clock_label.config(text=formatted_time)


class AlarmApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Jam")

        self.alarm_label = tk.Label(self.master, text="Atur Waktu Alarm:", font=("Helvetica", 14))
        self.alarm_label.pack(pady=10)

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()

        self.hour_entry = tk.Entry(self.master, textvariable=self.hour_var, width=2, font=("Helvetica", 12))
        self.hour_entry.pack(side=tk.LEFT, padx=5)

        self.minute_entry = tk.Entry(self.master, textvariable=self.minute_var, width=2, font=("Helvetica", 12))
        self.minute_entry.pack(side=tk.LEFT, padx=5)

        self.set_alarm_button = tk.Button(self.master, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)

        self.stop_alarm_button = tk.Button(self.master, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_alarm_button.pack(pady=10)

        self.alarm_time = None
        self.alarm_running = False

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())

            if 0 <= hour <= 23 and 0 <= minute <= 59:
                now = datetime.now().time()
                self.alarm_time = time(hour, minute)
                delta = datetime.combine(datetime.today(), self.alarm_time) - datetime.combine(datetime.today(), now)

                if delta.total_seconds() <= 0:
                    delta += timedelta(days=1)

                self.master.after(int(delta.total_seconds() * 1000), self.trigger_alarm)
                self.set_alarm_button.config(state=tk.DISABLED)
                self.stop_alarm_button.config(state=tk.NORMAL)
        except ValueError:
            pass

    def trigger_alarm(self):
        self.alarm_running = True
        winsound.Beep(1000, 1000)
        self.set_alarm_button.config(state=tk.NORMAL)
        self.stop_alarm_button.config(state=tk.DISABLED)

    def stop_alarm(self):
        self.alarm_running = False
        self.set_alarm_button.config(state=tk.NORMAL)
        self.stop_alarm_button.config(state=tk.DISABLED)

class StopwatchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stopwatch Jam")

        self.stopwatch_label = tk.Label(self.master, text="00:00:00", font=("Helvetica", 24))
        self.stopwatch_label.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Mulai", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.master, text="Berhenti", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_stopwatch, state=tk.DISABLED)
        self.reset_button.pack(side=tk.RIGHT, padx=10)

        self.elapsed_time = timedelta()
        self.running = False
        self.update_stopwatch()

    def start_stopwatch(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.update_stopwatch()

    def stop_stopwatch(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_stopwatch(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.elapsed_time = timedelta()
        self.update_stopwatch()

    def update_stopwatch(self):
        if self.running:
            self.elapsed_time += timedelta(seconds=1)
            stopwatch_str = str(self.elapsed_time).split(".")[0]
            self.stopwatch_label.config(text=stopwatch_str)
            self.master.after(1000, self.update_stopwatch)

if __name__ == "__main__":
    root = tk.Tk()
    WorldClockApp(root)
    AlarmApp(root)
    StopwatchApp(root)
    root.mainloop()
