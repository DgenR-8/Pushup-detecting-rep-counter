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

rep = False
rep_activation = False
alarm_counter = 0

def beep_rep():
    
    global rep
    for _ in range(1): # number of repeats of alarm rep before breaking
        if not rep_activation:
            break
        print("You have completed one rep")
        winsound.Beep(400, 500) # Frequency of sound, duration of sound in milliseconds
        
    rep = False


while True:

    _, frame = cap.read() 
    frame = imutils.resize(frame, width=500)

    if rep_activation:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, initial_frame)
        threshold = cv2.threshold(difference, 96, 1977, cv2.THRESH_BINARY)[1]
        initial_frame = frame_bw

        if threshold.sum() > 1000000: # Sensitivity of motion detection
            alarm_counter += 1 # If sensitivity is triggered rep counter accumulates
        else:
            if alarm_counter > 0: # If senstivity isn't triggered (e.g. no motion detected)
                alarm_counter -= 1 # Rep counter decreases, subsequently reducing alarm activations
        
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    
    if alarm_counter > 1: # the higher the counter the higher the frequency of alarm activations
        if not rep:
            rep = True
            threading.Thread(target=beep_rep).start()

    key_pressed = cv2.waitKey(15) # Keypress delay
    if key_pressed == ord("t"):
        rep_activation = not rep_activation
        alarm_counter = 0
    if key_pressed == ord("q"):
        rep_activation = False
        break




cap.release()
cv2.destroyAllWindows()