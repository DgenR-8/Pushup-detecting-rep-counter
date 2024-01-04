import threading
import winsound

import cv2
import imutils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, initial_frame = cap.read()
initial_frame = imutils.resize(initial_frame, width=500)
initial_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
initial_frame = cv2.GaussianBlur(initial_frame, (21, 21), 0)

alarm = False
alarm_activation = False
alarm_counter = 0
rep_counter = 0

def beep_alarm():
    global alarm
    for _ in range(1, 100): # number of repeats of alarm before breaking
        if not alarm_activation:
            break
        rep_counter = _+1
        print("You are on rep ", rep_counter)
        winsound.Beep(3000, 500) # Frequency of sound, duration of sound in milliseconds
    alarm = False


while True:

    _, frame = cap.read() 
    frame = imutils.resize(frame, width=500)

    if alarm_activation:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, initial_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        initial_frame = frame_bw

        if threshold.sum() > 1000: # Sensitivity of motion detection
            alarm_counter += 1 # If sensitivity is triggered alarm counter accumulates
        else:
            if alarm_counter > 0: # If senstivity isn't trigger (e.g. no motion detected)
                alarm_counter -= 1 # Alarm counter decreases, subsequently reducing alarm activations
        
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    
    if alarm_counter > 1: # the higher the counter the higher the frequency of alarm activations
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(15) # Keypress delay
    if key_pressed == ord("t"):
        alarm_activation = not alarm_activation
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_activation = False
        break




cap.release()
cv2.destroyAllWindows()