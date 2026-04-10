import cv2
import mediapipe as mp
import random
import time
from collections import Counter
import pygame

# -------- SOUND SAFE SETUP --------
pygame.mixer.init()

def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return None

win_sound = load_sound("win.wav")
lose_sound = load_sound("lose.wav")
count_sound = load_sound("count.wav")

# -------- MEDIAPIPE --------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not working")
    exit()

# -------- GESTURE DETECTION (IMPROVED) --------
def get_gesture(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total = sum(fingers)

    if total == 0:
        return "Rock"
    elif total == 5:
        return "Paper"
    elif total == 2 and fingers[1] == 1 and fingers[2] == 1:
        return "Scissors"
    else:
        return "Unknown"

# -------- AI --------
user_history = []

def get_ai_move():
    if len(user_history) < 3:
        return random.choice(["Rock", "Paper", "Scissors"])

    most_common = Counter(user_history).most_common(1)[0][0]

    if most_common == "Rock":
        return "Paper"
    elif most_common == "Paper":
        return "Scissors"
    else:
        return "Rock"

# -------- GAME LOGIC (YOUR RULES) --------
wins = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock"
}

# -------- VARIABLES --------
user_score = 0
computer_score = 0
round_number = 1
max_rounds = 5

round_active = False
round_start_time = time.time()
countdown_time = 3

computer_move = "None"
result_text = ""
last_count = -1

# -------- MAIN LOOP --------
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # UI overlay (transparent)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0,0), (640,480), (30,30,30), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    user_move = "None"

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            user_move = get_gesture(handLms)

    elapsed = time.time() - round_start_time

    # -------- COUNTDOWN --------
    if not round_active:
        if elapsed < countdown_time:
            count = int(countdown_time - elapsed) + 1

            cv2.putText(frame, f"Round {round_number}", (200,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            cv2.putText(frame, str(count), (300,220),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,255), 5)

            if count != last_count:
                if count_sound:
                    count_sound.play()
                last_count = count

        else:
            round_active = True
            computer_move = get_ai_move()
            last_count = -1

    # -------- GAME RESULT --------
    else:
        if result_text == "":
            if user_move in ["Rock", "Paper", "Scissors"]:
                user_history.append(user_move)

                if user_move == computer_move:
                    result_text = "Draw"

                elif wins[user_move] == computer_move:
                    result_text = "You Win!"
                    user_score += 1
                    if win_sound:
                        win_sound.play()

                else:
                    result_text = "Computer Wins!"
                    computer_score += 1
                    if lose_sound:
                        lose_sound.play()

        # Display
        cv2.putText(frame, f"You: {user_move}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        cv2.putText(frame, f"AI: {computer_move}", (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

        cv2.putText(frame, result_text, (20,170),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        # AI prediction
        if len(user_history) > 0:
            most_common = Counter(user_history).most_common(1)[0][0]
            cv2.putText(frame, f"AI predicts: {most_common}", (20,220),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        if elapsed > countdown_time + 2:
            round_number += 1
            round_active = False
            round_start_time = time.time()
            result_text = ""

    # -------- SCORE --------
    cv2.putText(frame, f"You: {user_score}", (450,80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.putText(frame, f"AI: {computer_score}", (450,120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

    # -------- GAME OVER --------
    if round_number > max_rounds:
        winner = "YOU WIN!" if user_score > computer_score else "AI WINS!"
        cv2.putText(frame, winner, (180,300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 4)

        cv2.putText(frame, "Press R to Restart", (150,350),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("AI Rock Paper Scissors", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

    if key == ord('r'):
        user_score = 0
        computer_score = 0
        round_number = 1
        round_active = False
        round_start_time = time.time()
        result_text = ""
        user_history.clear()

cap.release()
cv2.destroyAllWindows()