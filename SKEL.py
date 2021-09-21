#!/usr/bin/env python
import sender
import mediapipe as mp
import cv2
import os
import time

import receiver








def ROI_render1(img,kp):

    x1 = kp[22]
    x2 = kp[26]
    x3 = kp[30]
    y1 = kp[23]
    y2 = kp[27]
    y3 = kp[31]
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
    cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
    cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
    cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)


    return True

def ROI_render2(img,kp):
    x1 = kp[24]
    x2 = kp[28]
    x3 = kp[32]
    y1 = kp[25]
    y2 = kp[29]
    y3 = kp[33]
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
    cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
    cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
    cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
    return True



def landmarks2keypoints(landmarks,image):


    image_width, image_height = image.shape[1], image.shape[0]
    keypoints = []
    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        keypoints.append([landmark.visibility, (landmark_x, landmark_y)])


    return keypoints
def landmarks2KP(landmarks,image):
    image_width, image_height = image.shape[1], image.shape[0]
    keypoints = []
    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        keypoints.append(landmark_x)
        keypoints.append(landmark_y)
    return keypoints




def skeletonizer(KP_global,EX_global,q):



    # printing process id
    print("ID of process running worker1: {}".format(os.getpid()))

    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    print(frame_width)
    print(frame_height)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(
            static_image_mode=False,  # false for prediction
            upper_body_only=False,
            smooth_landmarks=True,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8) as pose:
        while cap.isOpened():

            start = time.time()
            success, image = cap.read()

            if not success:
                #print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                return False
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = pose.process(image)








            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            end = time.time()
            seconds = end - start
            fps = 1 / seconds
            cv2.putText(image, 'FPS: {}'.format(int(fps)), (frame_width - 190, 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                        255)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )






            #converting LM to KP
            if results.pose_landmarks is not None:
                # svuoto queue
                while not q.empty():
                    bit = q.get()
                kp = landmarks2KP(results.pose_landmarks,image)
                if q.full():
                    print("impossible to insert data in full queue")
                else:


                    q.put(kp)


                #print(KP_global)


                #print("KP global found : {}".format(len(KP_global)))


                if EX_global.value == 1:
                    if ROI_render1(image, kp):
                        pass

                        #print("ex1 running..._____!!!!___")


                elif EX_global.value == 2:
                    if ROI_render2(image, kp):
                        pass

                        #print("ex2 running...___!!!!_______")

                else:
                    print("no exercise...___________")
                    pass


            #invio streaming
            sender.stream(image)
            sender.send_status(5002,"KP_success")

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                return False

        cap.release()

        cv2.destroyAllWindows()
