# AI Rock-Paper-Scissors (Computer Vision Game)

## Overview

This project is a real-time interactive game that uses computer vision to recognize hand gestures and simulate a Rock-Paper-Scissors match against an intelligent AI opponent.

The system captures live video input, detects hand landmarks, classifies gestures, and determines the game outcome instantly.

## Key Highlights

* Real-time gesture recognition using webcam
* Hand tracking powered by MediaPipe
* Adaptive AI opponent (learns user patterns)
* Multi-round gameplay with scoring system
* Countdown-based round control
* Lightweight and fast execution

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame (for optional sound)

## How It Works

1. The webcam captures live frames
2. MediaPipe detects hand landmarks
3. Finger positions are analyzed to classify:

   * Rock
   * Paper
   * Scissors
4. The AI predicts user behavior using past moves
5. Game result is computed using rule-based logic

## Game Logic

* Rock defeats Scissors
* Paper defeats Rock
* Scissors defeats Paper
* Same moves result in a draw

## Installation & Setup

Install dependencies:

```
pip install opencv-python mediapipe==0.10.9 numpy pygame
```

Run the project:

```
python main.py
```

## Controls

* Show your hand in front of the camera
* Press 'R' to restart the game
* Press 'ESC' to exit

## Project Structure

```
AI-Rock-Paper-Scissors/
│
├── main.py
├── .gitignore
├── requirements.txt
```

## Challenges Faced

* Handling real-time gesture accuracy
* Managing lighting and hand positioning variations
* Resolving library compatibility issues (MediaPipe, protobuf)

## Possible Improvements

* Train a custom ML model for better gesture accuracy
* Add GUI using Tkinter or PyQt
* Deploy as a web application
* Improve AI strategy using machine learning

## Author

Riya Chauhan
