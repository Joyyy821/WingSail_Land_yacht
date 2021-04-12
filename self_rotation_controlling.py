# File: self_steering2.py
# Latest version
# 帆车自动在风场转圈行驶实现

import serial
import time
from threading import Thread
import keyboard

import numpy
import matplotlib.pyplot as plt

from PythonSample_mySQL import receiveNewFrame
from PythonSample_mySQL import receiveRigidBodyFrame
from PythonSample_mySQL import GetYachtPos, GetYachtRotation, GetSailRotation
from NatNetClient import NatNetClient
from QuaternionToEuler import QuaternionToEuler
from sail_angle import getBestSa

#############
# Constants #
#############
DEAD_ZONE_TH = 30        # 进入死区的角度(实验得出)
L = 0.65                    # 车长（m）
d0 = 0.12                   # 后轮中心到重心
w = 55 * numpy.pi / 180                 # 轮子转动最大弧度
D = numpy.sqrt(d0 ** 2 + (L / numpy.tan(w)) ** 2)                     # 最小转弯半径（m）

# 风场边界值
SAFE_DIS = 0.2
x_low = -2.5 + SAFE_DIS
x_up = 2 - SAFE_DIS
y_left = 5 + SAFE_DIS + 0.5
y_right = 9.5 - SAFE_DIS
# TODO: below are estimated values
xwind_low = -2.2
xwind_up = x_up - 0.85

# TODO
# start_x = xwind_low
# start_y = 5.5
# heading = -60

# gammaList = []
# for ang in range(0,180,1):
#     gammaList.append(ang*numpy.pi/180)

# f = open("max_acc3.txt", "r")
# max_acc = []
# max_acc_alpha = []
# i = 0
# for line in f:
#     if i == 0:
#         max_acc = eval(line)
#     if i == 1:
#         max_acc_alpha = eval(line)
#     i += 1
# f.close()

# This will create a new NatNet client
streamingClient = NatNetClient()
streamingClient.localIPAddress="192.168.3.43"

# Configure the streaming client to call our rigid body handler on the emulator to send data out.
streamingClient.newFrameListener = receiveNewFrame
streamingClient.rigidBodyListener = receiveRigidBodyFrame

# Start up the streaming client now that the callbacks are set up.
# This will run perpetually, and operate on a separate thread.
# dataThread, commandThread = streamingClient.run()
streamingClient.run()
time.sleep(0.001)


# Motion Capture: 读取航向角，攻角（计算得），加速度，速度。
# 检测航向(读取车的姿态根据几何位置计算)
# 输出结果: 正向左 负向右
def heading_direction():
    rotation_quaternion = GetYachtRotation()
    heading_ang = QuaternionToEuler(rotation_quaternion)
    val = heading_ang[2] + 90.5
    if val > 180:
        val -= 360
    elif val < -180:
        val += 360
    return val

def sail_direction():
    rotation_quaternion = GetSailRotation()
    sail_ang = QuaternionToEuler(rotation_quaternion)
    val = sail_ang[2] + 121.8
    if val > 180:
        val -= 360
    elif val < -180:
        val += 360
    return val

# 读取车的速度大小
def vel_amp():
    delta_t = 0.05
    # delta_t = 0.5
    pos1 = numpy.array(GetYachtPos())
    time.sleep(delta_t)
    pos2 = numpy.array(GetYachtPos())
    delta_pos = pos2 - pos1
    vel = numpy.sqrt(delta_pos[0] ** 2 + delta_pos[2] ** 2) / delta_t
    return vel

def upLimit(xwind_up):
    # global xwind_up
    global D
    # global SAFE_DIS
    theta = heading_direction()/180 * numpy.pi
    delta_x = D * (1 - numpy.cos(numpy.pi/2 - theta))
    return xwind_up - delta_x


def send_cmd(ser, servo, dir, ang):
    #若端口未打开，需打开端口。注：第一次调用时，端口处于打开状态，
    #每使用一次需关闭，因此需要判定端口是否处于开放状态。
    if not ser.isOpen():
        ser.open()
         
        #python中，我们使用decode()和encode()来进行解码和编码，utf-8是字符串编码常用类型
        #以utf-8编码对unicode对像进行编码
    # command=('+'+str(x)+'x').encode(encoding='utf-8')
    command = (servo + dir + str(ang)).encode(encoding='utf-8')
    ser.write(command)
    data = ser.readline()
    print(data)


#注意要调节电脑串口的频率与之匹配。操作路径如下：
#设备管理器——端口——对应端口（如COM4）——右键属性——端口设置——位/秒改为9600
ser = serial.Serial('COM4', 9600)
if not ser.isOpen():
    ser.open()

ser.timeout = 0.1

stop_controlling = False

def driving():
    global stop_controlling

    # t_sleep = 0.01
    # min_v = 0.8

    # init_pos = GetYachtPos()
    # print("initial position: ", init_pos[0], '\t', init_pos[2])
    # f3 = open("sail_dir_pos3", 'w')

    while True:
        if stop_controlling:
            break

        if keyboard.is_pressed('j'):
            send_cmd(ser, 'W', 'A', 45)     # 轮子向左转25度
        elif keyboard.is_pressed('k'):
            send_cmd(ser, 'W', 'D', 3)        # 轮子回正
        elif keyboard.is_pressed('l'):
            send_cmd(ser, 'W', 'D', 45)     # 轮子向右转25度

        # Sail Controlling
        # sail_pos = sailPos()
        current_heading = heading_direction()   
        v = vel_amp()
        if v >= 2:
            continue
        print("vel: ", v, end='\t')
        sail_pos = getBestSa(v, current_heading)
        servo_pos = int((sail_pos - 1.3333) / 0.8041)
        # servo_pos = sail_pos
        # sail_pos = abs(sail_pos)
        # print("sail_pos: ", sail_pos)
        # print("sail direction: ", sail_direction())
        print("current heading: ", current_heading)
        # if abs(current_heading) <= 90:
        # if current_heading <= 0 and current_heading >= -90:
        if servo_pos > 0:
            # print("against wind1")
            # cmd = ('Q'+'D'+str(sail_pos - 5)).encode(encoding='utf-8')
            cmd = ('Q'+'A'+str(servo_pos)).encode(encoding='utf-8')
            # print(cmd)
        # elif current_heading > 0 and current_heading <= 90:
        else:
            # print("against wind2")
            cmd = ('Q'+'D'+str(-servo_pos)).encode(encoding='utf-8')
            # print(cmd)
        # elif current_heading >= 70:
        #     # print("downwind 1")
        #     cmd = ('QA60').encode(encoding='utf-8')
        # elif current_heading <= -90:
        #     # print("downwind 2")
        #     cmd = ('QD60').encode(encoding='utf-8')
        # else:
        #     cmd = ('Q' + 'D' + str(sail_pos)).encode(encoding='utf-8')
        ser.write(cmd)
        data = ser.readline()
        # print("read from serial: ", data)
        # f3.write(str(current_heading)+'\t'+str(sail_pos)+'\n')
        # time.sleep(0.1)

t = Thread(target=driving)

t.start()
print("Start controlling.")

# 按q键退出程序
while True:
    if keyboard.is_pressed('q'):
        print("Program Exiting...")
        stop_controlling = True
        t.join()
        break
    else:
        time.sleep(0.1)

# Close the serial in the end
if ser.isOpen():
    ser.close()
print("Program Exits.")
exit()
