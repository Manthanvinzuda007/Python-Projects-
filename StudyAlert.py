
import json
import time
import os
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# Attempt to import plyer for desktop notifications
try:
    from plyer import notification
    HAS_NOTIFICATIONS = True
except ImportError:
    HAS_NOTIFICATIONS = False

# --- CONFIGURATION & CONSTANTS ---
DATA_FILE = "study_data.json"
STRICT_MESSAGES = [
    "Discipline beats talent when talent doesn't work hard.",
    "GPSC doesn't crack itself. Get back to work.",
    "Your competition is studying right now. Are you?",
    "An hour wasted now is a lifetime of regret later.",
    "The pain of discipline is far less than the pain of regret."
]
PRAISE_MESSAGES = [
    "Excellent consistency. You're building the mind of an officer.",
    "Great work today. One step closer to your goal!",
    "The grind is hard, but the result is worth it. Keep going."
]

# --- DATA MODELS ---

@dataclass
class StudyAlert:
    subject: str
    topic: str
    start_time: str  # Format: HH:MM
    duration_mins: int
    repeat: str = "Daily"
    status: str = "Pending" # Pending, Completed, Skipped

@dataclass
class UserProfile:
    name: str
    goal: str
    daily_hours_goal: int
    joined_date: str = datetime.now().strftime("%Y-%m-%d")

# --- CORE MODULES ---

class StorageManager:
    """Handles persistence for Profile, Schedules, and Analytics."""
    @staticmethod
    def save_data(profile: UserProfile, alerts: List[StudyAlert], logs: List[Dict]):
        data = {
            "profile": asdict(profile),
            "alerts": [asdict(a) for a in alerts],
            "logs": logs
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_data():
        if not os.path.exists(DATA_FILE):
            return None
        with open(DATA_FILE, "r") as f:
            return json.load(f)

class MentorEngine:
    """Rule-based logic for motivation and discipline enforcement."""
    @staticmethod
    def get_feedback(consistency_score: float):
        if consistency_score < 0.5:
            return f"CRITICAL WARNING: {STRICT_MESSAGES[int(time.time()) % len(STRICT_MESSAGES)]}"
        elif consistency_score < 0.8:
            return "You are drifting. Real aspirants don't make excuses."
        else:
            return PRAISE_MESSAGES[int(time.time()) % len(PRAISE_MESSAGES)]

    @staticmethod
    def send_notification(title, message, urgent=False):
        print(f"\n[{'!!!' if urgent else 'INFO'}] {title}: {message}")
        if HAS_NOTIFICATIONS:
            notification.notify(
                title=title,
                message=message,
                app_name="StudyAlert Mentor",
                timeout=10 if not urgent else 30
            )

class StudyScheduler:
    """Background engine that monitors time and triggers alerts."""
    def __init__(self, app_instance):
        self.app = app_instance
        self.running = True

    def run(self):
        while self.running:
            now = datetime.now().strftime("%H:%M")
            for alert in self.app.alerts:
                if alert.start_time == now and alert.status == "Pending":
                    self.trigger_alert(alert)
            time.sleep(30) # Check every 30 seconds

    def trigger_alert(self, alert: StudyAlert):
        MentorEngine.send_notification(
            "STUDY SESSION STARTING", 
            f"Subject: {alert.subject}\nTopic: {alert.topic}\nDuration: {alert.duration_mins}m",
            urgent=True
        )
        # Mark as notified so it doesn't trigger multiple times in the same minute
        alert.status = "Notified" 

class StudyAlertApp:
    def __init__(self):
        self.profile: Optional[UserProfile] = None
        self.alerts: List[StudyAlert] = []
        self.logs: List[Dict] = []
        self.scheduler = StudyScheduler(self)
        self.load_state()

    def load_state(self):
        data = StorageManager.load_data()
        if data:
            self.profile = UserProfile(**data['profile'])
            self.alerts = [StudyAlert(**a) for a in data['alerts']]
            self.logs = data['logs']
        else:
            self.setup_wizard()

    def setup_wizard(self):
        print("=== WELCOME TO STUDY ALERT SYSTEM (DSP MINDSET) ===")
        name = input("Enter your name: ")
        goal = input("Enter your exam goal (e.g., GPSC, UPSC): ")
        hours = int(input("Daily study hour goal: "))
        self.profile = UserProfile(name, goal, hours)
        self.save_state()

    def save_state(self):
        StorageManager.save_data(self.profile, self.alerts, self.logs)

    def add_alert(self):
        print("\n--- ADD NEW STUDY ALERT ---")
        sub = input("Subject: ")
        topic = input("Topic: ")
        t_start = input("Start Time (HH:MM 24h): ")
        dur = int(input("Duration (minutes): "))
        
        # Simple overlap check
        for a in self.alerts:
            if a.start_time == t_start:
                print("Error: Conflict with existing alert!")
                return
        
        self.alerts.append(StudyAlert(sub, topic, t_start, dur))
        self.save_state()
        print("Alert scheduled successfully.")

    def start_focus_mode(self, duration_mins, subject="Emergency", topic="Intensive"):
        """Locks the user into a countdown timer."""
        print(f"\n🔥 FOCUS MODE ACTIVATED: {subject} - {topic} 🔥")
        print("No excuses. No snoozing. Finish the mission.")
        
        end_time = datetime.now() + timedelta(minutes=duration_mins)
        try:
            while datetime.now() < end_time:
                remaining = end_time - datetime.now()
                mins, secs = divmod(remaining.seconds, 60)
                timer = f"{mins:02d}:{secs:02d}"
                print(f"\rRemaining: {timer} | Goal: {self.profile.goal}", end="")
                time.sleep(1)
            
            print("\n\n✅ Session Completed!")
            self.log_session(subject, duration_mins, "Completed")
        except KeyboardInterrupt:
            print("\n\n❌ SESSION ABANDONED. This will reflect in your discipline report.")
            self.log_session(subject, 0, "Skipped")

    def log_session(self, subject, minutes, status):
        log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "subject": subject,
            "minutes": minutes,
            "status": status
        }
        self.logs.append(log_entry)
        self.save_state()

    def show_analytics(self):
        print("\n--- DISCIPLINE REPORT ---")
        today = datetime.now().strftime("%Y-%m-%d")
        today_mins = sum(l['minutes'] for l in self.logs if l['date'] == today)
        completed = len([l for l in self.logs if l['status'] == "Completed"])
        skipped = len([l for l in self.logs if l['status'] == "Skipped"])
        
        total_sessions = completed + skipped
        score = completed / total_sessions if total_sessions > 0 else 1.0
        
        print(f"User: {self.profile.name} | Goal: {self.profile.goal}")
        print(f"Today's Study Time: {today_mins // 60}h {today_mins % 60}m")
        print(f"Total Sessions: {total_sessions} (✅ {completed} / ❌ {skipped})")
        print(f"Consistency Score: {score*100:.1f}%")
        print(f"\nMENTOR FEEDBACK: {MentorEngine.get_feedback(score)}")

    def run_cli(self):
        # Start background scheduler
        thread = threading.Thread(target=self.scheduler.run, daemon=True)
        thread.start()

        while True:
            print(f"\n--- {self.profile.name.upper()}'S DASHBOARD ---")
            print("1. View/Add Study Alerts")
            print("2. Manual Focus Mode (Timer)")
            print("3. Emergency Study Mode (90m Hardcore)")
            print("4. Discipline Analytics")
            print("5. Reset All Alerts for Today")
            print("6. Exit")
            
            choice = input("\nAction >> ")
            
            if choice == "1":
                self.manage_alerts()
            elif choice == "2":
                sub = input("Subject: ")
                dur = int(input("Duration (mins): "))
                self.start_focus_mode(dur, subject=sub)
            elif choice == "3":
                self.start_focus_mode(90, "HARDCORE", "Emergency Discipline")
            elif choice == "4":
                self.show_analytics()
            elif choice == "5":
                for a in self.alerts: a.status = "Pending"
                print("All alerts reset.")
            elif choice == "6":
                print("Mentor: Remember, results follow consistency. Goodbye.")
                break

    def manage_alerts(self):
        print("\n--- CURRENT SCHEDULE ---")
        for i, a in enumerate(self.alerts):
            print(f"{i+1}. [{a.start_time}] {a.subject} - {a.topic} ({a.duration_mins}m) | {a.status}")
        
        print("\na) Add Alert  d) Delete Alert  b) Back")
        cmd = input(">> ")
        if cmd == "a": self.add_alert()
        elif cmd == "d":
            idx = int(input("Index to delete: ")) - 1
            self.alerts.pop(idx)
            self.save_state()

if __name__ == "__main__":
    app = StudyAlertApp()
    try:
        app.run_cli()
    except KeyboardInterrupt:
        print("\nApp closed. Stay disciplined.")
