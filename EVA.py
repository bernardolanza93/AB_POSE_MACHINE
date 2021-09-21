#!/usr/bin/env python
import sender
import mediapipe as mp
import cv2
import os
import time
import math
import receiver
import numpy as np


def findAngle( p1, p2, p3):
    # Get the landmarks
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3

    # Calculate the Angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    # print(angle)



    return angle



def counter1(kp,dir,ex_count):




    angle = findAngle((kp[22], kp[23]), (kp[26], kp[27]), (kp[30], kp[31]))
    #print("angle from EVA : {}".format(angle))
    per = np.interp(angle, (10, 170), (100, 0))
    if angle > 160:
        dir = "down"
    if angle < 40 and dir == "down":
        dir = "up"
        ex_count.value += 1
    print("dir : {}".format(dir))

    print("COUNTING  {} ".format(ex_count.value))
    print("percentage : {} %".format(per))
    return True















def evaluator(KP_global,EX_global,q,ex_count):

    # printing process id
    print("ID of process running worker2: {}".format(os.getpid()))
    time.sleep(3)
    kp = []
    dir = ""








    while True:

        time.sleep(0.5)
        EX_global.value = 1




        if q.empty():
            print("no data aviable")
            continue
        else:
            kp = q.get(False)

        #print(kp)
        #print("ex {} selected".format(EX_global.value))


#exercise_name = tcp_read(port)
#evaluate_exercise(exercise_name)
        #case exercise_name =  curl
            #Keypoints,evaluation_range = read_exercise_info(curl)/read_config(arm_l)
            #evaluation_range = read(exercise_info)
            #joints =read(ex_info/config)
        #(count,ex_status) = def curl(joints,evaluation_range)

    #send_Tcp(count, ex_status)





        if counter1(kp,dir,ex_count):
            pass
        # Check for the dumbbell curls






        continue

















