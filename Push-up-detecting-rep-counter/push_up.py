import cv2 # Computer vision library dependency
import mediapipe as mp # Framework for machine learning utilising ML solutions
import numpy as np # Python library incorporating arrays
mp_drawing = mp.solutions.drawing_utils # Provides drawing utilities
mp_pose = mp.solutions.pose # Importing the pose estimation model
import pudrc # Importing pudrc for start menu functionality

# Start menu upon user input 1 from pudrc.py
pudrc.start_menu()

# Live video feed
cap_push_up = cv2.VideoCapture(0)

# Rep counter variables
push_up_counter = 0
push_up_form = None
push_up_validity = None

class StartPushUp(): # Start push up class

    # Calculating the difference between 3 joints 
    def calculate_push_up(pu_a,pu_b,pu_c):

        pu_a = np.array(pu_a) # Starting angle converted to array
        pu_b = np.array(pu_b) # Anchorpoint converted to array
        pu_c = np.array(pu_c) # Ending angle converted to array

        radians = np.arctan2(pu_c[1]-pu_b[1], pu_c[0]-pu_b[0]) - np.arctan2(pu_a[1]-pu_b[1], pu_a[0]-pu_b[0])
        push_up_angle= np.abs(radians*180.0/np.pi)
        
        if push_up_angle > 180.0: # Joint can't go past 180 degrees just like forearm
            push_up_angle = 360-push_up_angle

        return push_up_angle

    ## Constantly detecting user in live video feed frame
    with mp_pose.Pose(min_detection_confidence=0.75, min_tracking_confidence=0.75) as pose:
        while cap_push_up.isOpened():
            ret, frame = cap_push_up.read()

            # Recolor of live video feed to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # User pose detection
            results = pose.process(image)

            # Recolor of live video feed to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.resize(frame, (1280, 720))

            # Extract pre-mapped joint system landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # retrieve specific joint coordinates
                r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Angle difference calculator
                push_up_angle = calculate_push_up(r_shoulder,r_elbow, r_wrist)

                # Angle vizualization of right elbow joint anchorpoint
                cv2.putText(image, str(push_up_angle), 
                            tuple(np.multiply(r_elbow, [1280, 720]).astype(int)), 
                            cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

                # Angle vizualization of left elbow joint anchorpoint
                cv2.putText(image, str(push_up_angle), 
                            tuple(np.multiply(l_elbow, [1280, 720]).astype(int)), 
                            cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                
                # Push-up counter logic
                if push_up_angle > 170:
                    push_up_form = "up"
                    push_up_validity = "Correct"
                elif push_up_angle < 170:
                    push_up_validity = "Incorrect"
                if push_up_angle < 80 and push_up_form == "up":
                    push_up_form = "down"
                    push_up_validity = "Correct"
                    push_up_counter += 1
                    print(push_up_counter)
                elif push_up_angle > 80 and push_up_form == "down":
                    push_up_validity = "Incorrect"
            except:
                pass
            
            # Rendering of push-up counter
            # Reps & Form values box
            cv2.rectangle(image, (400,0), (875,60), (245,255,16), -1)
            
            # data for Reps and counter values
            cv2.putText(image, 'Reps', (440,8), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(push_up_counter), 
                        (440,50), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2, cv2.LINE_AA)
            
            # Data for Form and up / down changing values
            cv2.putText(image, 'Form', (515,8), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, push_up_form, 
                        (515,50), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2, cv2.LINE_AA)

            # data for validity and correct / incorrect values
            cv2.putText(image, 'Validity', (650,8), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(push_up_validity), 
                        (650,50), 
                        cv2. FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2, cv2.LINE_AA)
            
            # Rendering for pose detection
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(150,105,0), thickness=1, circle_radius=3), 
                                    mp_drawing.DrawingSpec(color=(255,180,0), thickness=1, circle_radius=3)
                                    )               
            cv2.imshow('Mediapipe Feed', image)

            # Terminate camera feed using t key
            if cv2.waitKey(1) & 0xFF == ord('t'):
                exit()
                    
        cap_push_up.release()
        cv2.destroyAllWindows()
