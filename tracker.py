import numpy as np
import mediapipe as mp



class ExerciseTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.counter = 0
        self.stage = "Neutral"
        self.current_exercise = "bicep_curl"
        self.audio_announced = True  # Flag to prevent repeating the same number

    def reset(self):
        """Resets the counter and stage metrics."""
        self.counter = 0
        self.stage = "Neutral"
        self.audio_announced = True

    def set_exercise(self, name):
        """Changes target workout and clears stale tracking history."""
        if self.current_exercise != name:
            self.current_exercise = name
            self.reset()

    def _calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180.0 else angle

    def _calculate_distance(self, p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def process_pose(self, landmarks):
        """Runs rule engine against detected joint structures."""
        if not landmarks:
            return

        # 1. BICEP CURL
        if self.current_exercise == "bicep_curl":
            shldr = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbw  = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrst  = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            angle = self._calculate_angle(shldr, elbw, wrst)
            
            if angle > 160: self.stage = "Down"
            if angle < 30 and self.stage == "Down":
                self.stage = "Up"
                self.counter += 1
                self.audio_announced = False  # Ready for voice cue

        # 2. SQUATS
        elif self.current_exercise == "squat":
            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankl = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            angle = self._calculate_angle(hip, knee, ankl)
            
            if angle > 160: self.stage = "Up"
            if angle < 90 and self.stage == "Up":
                self.stage = "Down"
                self.counter += 1
                self.audio_announced = False  # Ready for voice cue

        # 3. PUSH-UPS
        elif self.current_exercise == "push_up":
            shldr = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbw  = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].value, landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrst  = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            angle = self._calculate_angle(shldr, elbw, wrst)
            
            if angle > 160: self.stage = "Up"
            if angle < 90 and self.stage == "Up":
                self.stage = "Down"
                self.counter += 1
                self.audio_announced = False  # Ready for voice cue

        # 4. JUMPING JACKS
        elif self.current_exercise == "jumping_jack":
            l_foot = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            r_foot = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            dist = self._calculate_distance(l_foot, r_foot)
            
            if dist < 0.25: self.stage = "Closed"
            if dist > 0.55 and self.stage == "Closed":
                self.stage = "Open"
                self.counter += 1
                self.audio_announced = False  # Ready for voice cue






