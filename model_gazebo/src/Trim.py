# -- coding: utf-8 --

from pickle import NONE

import sys
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import rospy
from Slack_Tuchi import Tuchi
import time
import cv2
import numpy as n
import message_filters
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import *
import tf.transformations as tft

#import tf as tft

import os, glob, shutil
import numpy as np
import random as rn

from subprocess import Popen,PIPE,call

#path_hozon = "/mnt/test/practice_ws/src/model_gazebo/src/img/"
path = "./img/"
hokan_path = "./hokan/"
def Torim():
    for infile in glob.glob( path+ '*.png' ):

        re_namae = infile.replace(path,"")
        img = cv2.imread(infile)
        x, y = 896, 476
        h, w = 128, 128
        img_trim = img[y:y+h, x:x+w]
        cv2.imwrite(hokan_path + re_namae, img_trim)

Torim()
Tuchi("TRIM_完了しやした為、")
sys.exit()
    
"""
        print(str(infile))
        img = cv2.imread(infile)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        color_lower = np.array([50, 50, 190, 255])
        color_upper = np.array([208, 208, 255, 255])
        img_mask = cv2.inRange(img, color_lower, color_upper)
        img_bool_2 = cv2.bitwise_not(img, img, mask=img_mask)
        cv2.imwrite(infile,img_bool_2)

        re_namae = infile.replace(path,"")
        print("'''''''''''''''''''",re_namae)
"""