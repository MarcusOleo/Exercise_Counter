import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mediapipe as mp
import threading
from playsound import playsound  # Reliable cross-platform audio player
from tracker import ExerciseTracker

class FitnessApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("950x550")
        self.window.configure(bg="#1e1e24")

        # Core Tracking Elements
        self.tracker = ExerciseTracker()
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)

        # Timer State Settings
        self.seconds_elapsed = 0
        self.timer_running = False

        self.setup_ui_layout()
        self.update_frame_loop()
        self.window.mainloop()

    def audio_worker(self):
        """Worker thread to execute audio playback without breaking the main loop layout."""
        try:
            # Replaces the unstable pyttsx3 speech engine with a sound file trigger
            playsound('ding.mp3')
        except Exception as e:
            print(f"Audio Playback Error: {e}")

    def trigger_sound_effect(self):
        """Asynchronously triggers the repetition audio chime."""
        threading.Thread(target=self.audio_worker, daemon=True).start()

    def update_timer_increment(self):
        """Handles background time increments via delayed execution maps."""
        if self.timer_running:
            self.seconds_elapsed += 1
            mins, secs = divmod(self.seconds_elapsed, 60)
            self.timer_label.config(text=f"TIME: {mins:02d}:{secs:02d}")
            self.window.after(1000, self.update_timer_increment)

    def toggle_timer(self):
        """Plays/pauses workout duration stopwatch metrics."""
        if self.timer_running:
            self.timer_running = False
            self.toggle_time_btn.config(text="START TIMER", bg="#2ed573")
        else:
            self.timer_running = True
            self.toggle_time_btn.config(text="PAUSE TIMER", bg="#ffa502")
            self.update_timer_increment()

    def reset_all_metrics(self):
        """Flushes time tallies and rep numbers simultaneously."""
        self.tracker.reset()
        self.seconds_elapsed = 0
        self.timer_label.config(text="TIME: 00:00")

    def setup_ui_layout(self):
        # Left Panel: Video Feed
        self.video_frame = tk.Frame(self.window, width=640, height=480, bg="black")
        self.video_frame.pack(side=tk.LEFT, padx=15, pady=15)
        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack()

        # Right Panel: Workspace Controls
        self.control_frame = tk.Frame(self.window, width=260, height=480, bg="#2a2a35")
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=15)

        tk.Label(self.control_frame, text="FITNESS CORE v2", font=("Helvetica", 14, "bold"), fg="#ff4757", bg="#2a2a35").pack(pady=10)

        # Dropdown Menu
        tk.Label(self.control_frame, text="Select Exercise:", font=("Helvetica", 9), fg="white", bg="#2a2a35").pack(anchor="w", padx=15)
        self.exercise_var = tk.StringVar(value="Bicep Curl")
        exercise_menu = ttk.Combobox(self.control_frame, textvariable=self.exercise_var, state="readonly", values=["Bicep Curl", "Squat", "Push Up", "Jumping Jack"])
        exercise_menu.pack(fill=tk.X, padx=15, pady=5)
        exercise_menu.bind("<<ComboboxSelected>>", self.on_exercise_change)

        # Timer Controls UI Block
        self.timer_label = tk.Label(self.control_frame, text="TIME: 00:00", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#2a2a35")
        self.timer_label.pack(pady=15)

        self.toggle_time_btn = tk.Button(self.control_frame, text="START TIMER", font=("Helvetica", 9, "bold"), bg="#2ed573", fg="white", command=self.toggle_timer, relief="flat")
        self.toggle_time_btn.pack(fill=tk.X, padx=30, pady=2)

        # Rep Counters UI Block
        self.rep_label = tk.Label(self.control_frame, text="REPS: 0", font=("Helvetica", 24, "bold"), fg="#2ed573", bg="#2a2a35")
        self.rep_label.pack(pady=20)

        self.stage_label = tk.Label(self.control_frame, text="STATE: Neutral", font=("Helvetica", 11), fg="#1e90ff", bg="#2a2a35")
        self.stage_label.pack(pady=2)

        # Master Clear Configuration
        reset_btn = tk.Button(self.control_frame, text="RESET ALL METRICS", font=("Helvetica", 10, "bold"), bg="#ff4757", fg="white", command=self.reset_all_metrics, relief="flat", height=2)
        reset_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

    def on_exercise_change(self, event):
        selection_mapping = {
            "Bicep Curl": "bicep_curl",
            "Squat": "squat",
            "Push Up": "push_up",
            "Jumping Jack": "jumping_jack"
        }
        self.tracker.set_exercise(selection_mapping[self.exercise_var.get()])

    def update_frame_loop(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            rgb_image.flags.writeable = False
            results = self.pose.process(rgb_image)
            rgb_image.flags.writeable = True

            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(rgb_image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                try:
                    self.tracker.process_pose(results.pose_landmarks.landmark)
                    
                    # Intercept repetition tally state changes
                    if not self.tracker.audio_announced:
                        self.trigger_sound_effect()
                        self.tracker.audio_announced = True
                except Exception:
                    pass

            # Sync Frame updates to Tkinter Elements
            self.rep_label.config(text=f"REPS: {self.tracker.counter}")
            self.stage_label.config(text=f"STATE: {self.tracker.stage.upper()}")

            img = Image.fromarray(rgb_image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.window.after(15, self.update_frame_loop)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    FitnessApp(tk.Tk(), "AI Analytics Dashboard with Audio Coach")
