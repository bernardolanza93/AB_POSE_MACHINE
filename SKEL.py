#!/usr/bin/env python

import sender
import mediapipe as mp
import cv2
import os
import time
import configparser


def ID_to_ex_string(ID):
    # read from ex_info
    config = configparser.ConfigParser()
    config.read('exercise_info.ini')
    sections = config.sections()
    # print("sections are : {}".format(sections))

    for exercise in sections:
        ID_num = int(config[exercise]["ID"])

        if ID_num == ID:
            ex_string = exercise

            return ex_string

    # print("no ID found")
    ex_string = "0"
    return ex_string


def KP_to_render_from_config_file(segments):
    config_geometrical = configparser.ConfigParser()

    config_geometrical.read('config.ini')
    KPS_to_render = []
    # print(type(dictionary["segments"]))
    # print(type(dictionary["eva_range"]))
    for arto in segments:
        # print("analizing arto: {}".format(arto))

        kps = config_geometrical["ALIAS"][arto]

        kps = [int(x) for x in kps.split(",")]
        KPS_to_render.append(kps)

    # print(KPS_to_render)
    return KPS_to_render


def ex_string_to_config_param(ex_string):
    # read from ex_info
    config_sk = configparser.ConfigParser()
    config_sk.read('exercise_info.ini')
    sections = config_sk.sections()
    # print("sections are : {}".format(sections))

    for exercise in sections:

        if exercise == ex_string:
            segments = config_sk.get(exercise, 'segments_to_render')
            segments = segments.split(',')

            KP_2_render = KP_to_render_from_config_file(segments)
            return KP_2_render

    # print("no exercise found_cannot get config parameters for geometry analysis")
    KP_2_render = []
    return KP_2_render


def KP_renderer_on_frame(ex_string, kp, img):

    if not ex_string:
        print("no exercise // no rendering")
    else:
        kp_2_rend = ex_string_to_config_param(ex_string)
        #print("kp_2_rend : ", kp_2_rend)

        for segment in kp_2_rend:

            x = []
            y = []
            for i in range(0, 5, 2):
                x.append(kp[segment[i]])
                y.append(kp[segment[i + 1]])

            for i in range(2):
                cv2.line(img, (x[i], y[i]), (x[i + 1], y[i + 1]), (255, 255, 255), 3)

            for i in range(len(x)):
                cv2.circle(img, (x[i], y[i]), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x[i], y[i]), 15, (0, 0, 255), 2)


def read_shared_mem_for_ex_string(mem_ex_value):
    if mem_ex_value == 0:
        ex_string = ""
        return ex_string
    else:

        ex_string = ID_to_ex_string(mem_ex_value)

        return ex_string


def landmarks2keypoints(landmarks, image): #deprecated
    image_width, image_height = image.shape[1], image.shape[0]
    keypoints = []
    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        keypoints.append([landmark.visibility, (landmark_x, landmark_y)])

    return keypoints


def landmarks2KP(landmarks, image):
    image_width, image_height = image.shape[1], image.shape[0]
    keypoints = []
    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        keypoints.append(landmark_x)
        keypoints.append(landmark_y)
    return keypoints


def skeletonizer(KP_global, EX_global, q):
    # printing process id
    print("ID of process running worker1: {}".format(os.getpid()))

    cap = cv2.VideoCapture(0)
    print("now i show you")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    print(frame_width)
    print(frame_height)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(
	static_image_mode = False,
        # upper_body_only=upper_body_only,
        model_complexity=0,
        #enable_segmentation=enable_segmentation,#unespected
	#smooth_landmark= True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():

            start = time.time()
            success, image = cap.read()

            if not success:
                # print("Ignoring empty camera frame.")
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

            # converting LM to KP
            if results.pose_landmarks is not None:
                # svuoto queue
                while not q.empty():
                    bit = q.get()
                kp = landmarks2KP(results.pose_landmarks, image)
                if q.full():
                    print("impossible to insert data in full queue")
                else:

                    q.put(kp)

                # print(KP_global)

                # print("KP global found : {}".format(len(KP_global)))

                ex_string = read_shared_mem_for_ex_string(EX_global.value)
                # render in front of ex_string
                if ex_string != "":
                    KP_renderer_on_frame(ex_string, kp, image)

            # invio streaming
            sender.stream(image)
            #sender.send_status(5002, "KP_success")
            

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                return False

        cap.release()

        cv2.destroyAllWindows()
