# Exercise Counter

A Python-based computer vision fitness application that uses **MediaPipe Pose** and **OpenCV** to detect body movements and automatically count repetitions for different exercises.

The application provides a live camera feed with body landmarks, tracks the user's exercise state, counts completed repetitions, provides an exercise timer, and plays an audio cue when a repetition is completed.

## Features

* **Live Camera Feed**
  Displays the user's webcam feed in real time with MediaPipe body landmarks and pose connections.

* **Exercise Detection and Rep Counting**
  Automatically counts repetitions based on the user's body position and joint angles.

* **Multiple Exercise Options**
  Supports:

  * Bicep Curls
  * Squats
  * Push Ups
  * Jumping Jacks

* **Live Exercise State**
  Displays the current state of the exercise, such as:

  * `UP`
  * `DOWN`
  * `CLOSED`
  * `OPEN`

* **Workout Timer**
  Includes a stopwatch that can be started and paused during a workout.

* **Audio Feedback**
  Plays an audio cue (`ding.mp3`) whenever a new repetition is successfully counted.

* **Reset Function**
  Allows the user to reset the repetition counter, exercise state, and timer.

* **Graphical User Interface**
  Built using Tkinter with a dedicated control panel for selecting exercises and monitoring workout statistics.

---

## Tech Stack

| Technology | Purpose                                                |
| ---------- | ------------------------------------------------------ |
| Python     | Main programming language                              |
| OpenCV     | Webcam access and image processing                     |
| MediaPipe  | Human pose detection and body landmark tracking        |
| NumPy      | Mathematical calculations and joint-angle calculations |
| Tkinter    | Graphical user interface                               |
| Pillow     | Converts OpenCV frames for display in Tkinter          |
| Playsound  | Audio feedback                                         |
| Threading  | Allows audio playback without blocking the GUI         |

---

## Project Structure

```text
CV_Exercise_Counter/
│
├── __pycache__/          # Python-generated cache files
├── myex_c/               # Project/environment-related directory
│
├── .gitignore            # Files and folders excluded from Git
├── ding.mp3              # Audio feedback played after a completed rep
├── LICENSE               # Project license
├── main.py               # Main application and GUI
├── tracker.py            # Exercise tracking and repetition logic
└── README.md             # Project documentation
```

### Main Components

#### `main.py`

This is the main application file. It is responsible for:

* Creating the Tkinter application window
* Accessing the webcam
* Processing video frames using OpenCV
* Running MediaPipe Pose detection
* Displaying pose landmarks
* Updating the repetition counter
* Updating the exercise state
* Managing the workout timer
* Playing the audio feedback
* Allowing the user to select an exercise

#### `tracker.py`

This file contains the `ExerciseTracker` class.

It is responsible for the actual exercise logic, including:

* Calculating joint angles
* Calculating distances between landmarks
* Determining exercise states
* Counting completed repetitions
* Resetting exercise statistics
* Switching between exercises

The tracker currently uses rule-based logic rather than a trained machine learning model.

#### `ding.mp3`

This audio file is played whenever a repetition is successfully completed.

---

# How It Works

The application follows this general pipeline:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Pose Detection
   ↓
Body Landmarks
   ↓
ExerciseTracker
   ↓
Joint Angle / Distance Calculation
   ↓
Exercise State
   ↓
Rep Counter
   ↓
GUI + Audio Feedback
```

For example, during a bicep curl, the application tracks the:

```text
Shoulder → Elbow → Wrist
```

The angle at the elbow is calculated to determine whether the arm is extended or contracted.

A simplified process is:

```text
Arm Extended
     ↓
  "Down"
     ↓
Arm Contracted
     ↓
    "Up"
     ↓
Rep Counter +1
     ↓
  Ding Sound
```

---

# Exercise Tracking Logic

## Bicep Curl

The application calculates the angle between the:

* Shoulder
* Elbow
* Wrist

A repetition is counted when the arm moves from an extended position to a contracted position.

```text
Angle > 160° → Down

Angle < 30° + previous state is Down
             ↓
           Up
             ↓
         Rep + 1
```

## Squat

The application uses the:

* Hip
* Knee
* Ankle

to calculate the knee angle.

```text
Angle > 160° → Up

Angle < 90° + previous state is Up
             ↓
          Down
             ↓
         Rep + 1
```

## Push Up

The application uses the:

* Shoulder
* Elbow
* Wrist

to calculate the elbow angle.

The general logic is similar to the squat:

```text
Arms extended → Up

Arms bent + previous state is Up
              ↓
            Down
              ↓
           Rep + 1
```

## Jumping Jack

Instead of calculating a joint angle, the application calculates the distance between the left and right ankles.

```text
Feet close together → Closed

Feet far apart + previous state is Closed
                    ↓
                  Open
                    ↓
                Rep + 1
```

---

# Installation

## Prerequisites

Make sure Python is installed on your computer.

You can check your Python installation with:

```bash
python --version
```

It is recommended to use a virtual environment for the project.

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

# Install Dependencies

Install the required Python packages:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pillow
pip install playsound
```

Alternatively, install everything at once:

```bash
pip install opencv-python mediapipe numpy pillow playsound
```

---

# Running the Application

Make sure your webcam is connected and that `ding.mp3` is located in the same directory as `main.py`.

Run:

```bash
python main.py
```

The application should open a window containing:

* Live camera feed
* Pose landmarks
* Exercise selection menu
* Rep counter
* Exercise state
* Workout timer
* Reset button

---

# Using the Application

### 1. Start the application

Run:

```bash
python main.py
```

### 2. Select an exercise

Use the **Select Exercise** dropdown to choose:

* Bicep Curl
* Squat
* Push Up
* Jumping Jack

### 3. Position yourself in front of the camera

Make sure your body and the relevant joints are visible to the camera.

### 4. Perform the exercise

The application will track your body landmarks and determine your current exercise state.

### 5. Monitor your repetitions

The interface displays:

```text
REPS: 10
STATE: UP
```

### 6. Use the timer

Click:

```text
START TIMER
```

to begin tracking workout duration.

The button changes to:

```text
PAUSE TIMER
```

when the timer is running.

### 7. Reset the workout

Click:

```text
RESET ALL METRICS
```

to reset the timer, repetition counter, and exercise state.

---

# Important Notes

## Camera Position

The accuracy of the application depends heavily on camera positioning.

For best results:

* Ensure there is sufficient lighting.
* Keep the relevant parts of your body visible.
* Avoid objects blocking your body.
* Stand far enough away from the camera to keep your body within the frame.
* For exercises that use the left side of the body, ensure the left-side landmarks are clearly visible.

## Pose Detection

The application uses MediaPipe Pose with:

```python
model_complexity=1
min_detection_confidence=0.5
min_tracking_confidence=0.5
```

These settings provide a balance between detection accuracy and processing speed.

---

# Known Limitations

This project currently uses manually defined thresholds rather than a trained exercise classification model.

For example:

```python
if angle > 160:
    self.stage = "Down"

if angle < 30 and self.stage == "Down":
    self.stage = "Up"
```

This means the application may not count repetitions correctly if:

* The camera angle changes significantly.
* The user performs an exercise differently.
* Body landmarks are temporarily lost.
* The user is too far from the camera.
* Lighting conditions are poor.
* Another object/person interferes with pose detection.

The thresholds may need to be adjusted for different users and camera setups.

---

# Troubleshooting

### Camera does not open

Make sure another application is not already using the webcam.

You can also check whether OpenCV can access the camera.

### Repetitions are not being counted

Check that:

1. Your body is clearly visible.
2. The relevant joints are detected.
3. You are performing the movement through the required range of motion.
4. Your camera is positioned correctly.

### Audio does not play

Make sure:

```text
ding.mp3
```

is located in the same directory from which the application is being executed.

You can also check that the computer's audio output is working.


# Future Improvements

Possible improvements for future versions include:

* Add more exercises.
* Improve repetition-counting accuracy.
* Support both left and right sides of the body.
* Automatically calibrate thresholds for each user.
* Add exercise form/error detection.
* Add workout history and statistics.
* Add calories-burned estimation.
* Add a voice coach.
* Add a trained machine learning model for exercise classification.
* Add support for multiple people.
* Improve the GUI design.
* Add configurable camera selection.
* Save workout results to a database or file.

---

# License

This project is distributed under the license included in the `LICENSE` file.

---

# Author

**Exercise Counter**

A computer vision-based fitness application developed using Python, OpenCV, MediaPipe, and Tkinter.


