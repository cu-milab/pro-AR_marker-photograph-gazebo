#-*- coding:utf-8 -*-
from Slack_Tuchi import Tuchi

def MissRead():


    with open('./miss.txt', 'r') as f:
        a1 = f.readlines()[-1]

    with open('./miss.txt', 'r') as f:
        b1 = f.readlines()[-2]

    with open('./miss.txt', 'r') as f:
        c1= f.readlines()[-3]

    with open('./miss.txt', 'r') as f:
        a2 = f.readlines()[-4]

    with open('./miss.txt', 'r') as f:
        b2 = f.readlines()[-5]

    with open('./miss.txt', 'r') as f:
        c2= f.readlines()[-6]

    with open('./miss.txt', 'r') as f:
        a3 = f.readlines()[-7]

    with open('./miss.txt', 'r') as f:
        b3 = f.readlines()[-8]

    with open('./miss.txt', 'r') as f:
        c3= f.readlines()[-9]

    if a1==a2==a3 and b1==b2==b3 and c1==c2==c3:
        print("wow")
        Tuchi("同じモデルで３回ミス")

    return a1,b1,c1,a2,b2,c2,a3,b3,c3

c = MissRead()
Tuchi("３連続同じモデルのミスはまだない")


print("roll",c[0])
print("pitch",c[1])
print("yaw",c[2])


print("roll2",c[3])
print("pitch2",c[4])
print("yaw2",c[5])


print("roll3",c[6])
print("pitch3",c[7])
print("yaw3",c[8])
