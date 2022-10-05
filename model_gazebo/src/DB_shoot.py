#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from tkinter import N
import rospy,cv2,sys,time,random,math,message_filters,os,shutil
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import *
import tf.transformations as tft

from Slack_Tuchi import Tuchi

path = "./img/"
hokan_path = "./hokan/"

def RenzokuStop():
    dir=os.listdir("./img/")

    if len(dir) >= 5000:
        Tuchi("2500枚撮影したので再起動しますね")
        print("wow")
        f = open('miss.txt', 'a')
        print("miss")
        f.write(str(r)+"\n"+str(p)+"\n"+str(y)+"\n")
        f.close()
        Tuchi(str(str(r)+"\n"+str(p)+"\n"+str(y))+"をミスした為、")
        sys.exit()
        

def MissRead():
    with open('./miss.txt', 'r') as f:
        yaw= f.readlines()[-1]
        print("yaw",yaw)

    with open('./miss.txt', 'r') as f:
        pitch = f.readlines()[-2]
        print("pitch",pitch)

    with open('./miss.txt', 'r') as f:
        roll = f.readlines()[-3]
        print("roll",roll)

    Tuchi("roll"+roll+",pitch"+pitch+",yaw"+yaw+"より開始")
    return  roll,pitch,yaw


class image_converter:
    def __init__(self):
        rospy.init_node('image_converter', anonymous=True)
        self.bridge = CvBridge()
        sub_rgb = message_filters.Subscriber("/camera2/color/image_raw", Image)
        sub_depth = message_filters.Subscriber("/camera/depth/image_raw", Image)
        self.mf = message_filters.ApproximateTimeSynchronizer(
            [sub_rgb, sub_depth], 100, 10.0)
        self.mf.registerCallback(self.ImageCallback)
        self.max = 162.635
        self.min = 128

    def ImageCallback(self, rgb_data, depth_data):
        try:
            color_image = self.bridge.imgmsg_to_cv2(rgb_data, 'passthrough')
        except CvBridgeError:# ,e:
            rospy.logerr(e)
        color_image.flags.writeable = True
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        h, w, c = color_image.shape
        self.color_image = color_image

    def SaveImage(self, num,r,p,y):
        cv2.imwrite(path+ str(num).zfill(6) +".png", self.color_image)
        #print("save_img"+ str(num).zfill(6))
        s=os.path.getsize(path + str(num).zfill(6) +".png")
        print("save_img"+ str(num).zfill(6),s)
        if s < 10000:#9600:
            f = open('miss.txt', 'a')
            print("miss")
            f.write(str(r)+"\n"+str(p)+"\n"+str(y)+"\n")
            f.close()
            Tuchi(str(str(r)+"\n"+str(p)+"\n"+str(y))+"をミスした為、")
            sys.exit()

        else:
            return


    def SaveImage1(self, num,r,p,y):
        cv2.imwrite(path+ str(num).zfill(6) +".png", self.color_image)
        #print("save_img"+ str(num).zfill(6))
        s=os.path.getsize(path + str(num).zfill(6) +".png")
        print("save_img"+ str(num).zfill(6),s)
        if s < 10000:#9600:
            f = open('first_miss.txt', 'a')
            print("======miss==========")
            f.write(str(r)+"\n"+str(p)+"\n"+str(y)+"\n")
            f.close()

        else:
            return


if __name__ == '__main__':
    try:
        ic = image_converter()
    except rospy.ROSInterruptException:
        pass
    rospy.wait_for_service("gazebo/delete_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)

    model_list = ["ID0_130"]
    model_name = model_list[0]

    xyz = [0.8, 0.0, 0.5]
    rpy = [0.0, 0.0, 0.0]

    shutil.rmtree("./img")#「img」を一旦削除
    os.mkdir('./img')#「img」を作成

    c = MissRead()

    while not rospy.is_shutdown():
        if model_name == "ID0_130":
            seed_number = 1
            model_name_1 =  "ID0_100000"
            cx = 0.8
        elif model_name == "2":
            seed_number = 2
            model_name_1 = "2_"
            cx = 0.81
        else:
            seed_number = 3
            model_name_1 = "AR1_50_"
            cx = 0.9
        l=[]
        print("len(l)",len(l))
        #l.append(1)
        for r in range(int(c[0]),360,1):
            if len(l)==0:
                print("len(l)",len(l))
                l.append(1)
                print("1")
                for p in range(int(c[1]),13,1):
                    for y in range(int(c[2]),13,1):
                        #Shoot()
                                        #角度をラジアン表記に変換
                        rad_r= r*(math.pi/180)
                        rad_p= p*(math.pi/180)
                        rad_y= y*(math.pi/180)
                        with open("../models/"+ model_name +"/model.sdf", "r") as f:
                            product_xml = f.read()
                        item_pose = Pose()
                        item_pose.position.x = xyz[0]
                        item_pose.position.y = xyz[1]
                        item_pose.position.z =  xyz[2]
                        tmpq = tft.quaternion_from_euler(rad_r,rad_p,rad_y)
                        q = Quaternion(tmpq[0],tmpq[1],tmpq[2],tmpq[3])
                        item_pose.orientation = q
                        spawn_model(model_name, product_xml, "", item_pose, "world")
                        time.sleep(0.3)
                        save_name = "r"+str(r)+"p"+str(p)+"y"+ str(y)
                        print(save_name)
                        roll  = str(r)
                        pitch = str(p)
                        yaw   = str(y)
                        ic.SaveImage1(save_name,roll,pitch,yaw)

                        delete_model(model_name)
            else:
                print("2")
                for p in range(-12,13,1):
                    for y in range(-12,13,1):
                        #Shoot()
                        rad_r= r*(math.pi/180)
                        rad_p= p*(math.pi/180)
                        rad_y= y*(math.pi/180)
                        with open("../models/"+ model_name +"/model.sdf", "r") as f:
                            product_xml = f.read()
                        item_pose = Pose()
                        item_pose.position.x = xyz[0]
                        item_pose.position.y = xyz[1]
                        item_pose.position.z =  xyz[2]
                        tmpq = tft.quaternion_from_euler(rad_r,rad_p,rad_y)
                        q = Quaternion(tmpq[0],tmpq[1],tmpq[2],tmpq[3])
                        item_pose.orientation = q
                        spawn_model(model_name, product_xml, "", item_pose, "world")
                        time.sleep(0.3)
                        save_name = "r"+str(r)+"p"+str(p)+"y"+ str(y)
                        print(save_name)
                        roll  = str(r)
                        pitch = str(p)
                        yaw   = str(y)
                        ic.SaveImage(save_name,roll,pitch,yaw)

                        delete_model(model_name)
                        
                        RenzokuStop()
