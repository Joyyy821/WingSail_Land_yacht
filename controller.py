# File: controller.py
# 检测键盘按键向轮子和帆的舵机分别发送指令

import serial
import keyboard
from getkey import getkey
from pynput.keyboard import Listener
import time

#注意要调节电脑串口的频率与之匹配。操作路径如下：
#设备管理器——端口——对应端口（如COM4）——右键属性——端口设置——位/秒改为9600
ser = serial.Serial('COM4',9600)
if not ser.isOpen():
    ser.open()

#定义函数将指令传给arduino
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
    
    # command=('*'+str(y)+'y').encode(encoding='utf-8')
    # ser.write(command)
    #每一次操作完成后，需关闭端口
    # ser.close()


def send_cmd_reset(ser, servo):
    if not ser.isOpen():
        ser.open()

    command = (servo).encode(encoding='utf-8')
    ser.write(command)

    # ser.close()

# a s d 控制帆，j k l 控制舵
# 帆通过差量控制(5°)，轮子只有 -25 0 (reset) 25三个值
def detect_key():
    # i = 0
    while True:
        # i += 1
        # print("detecting...", i)
        if keyboard.is_pressed('a'):
            send_cmd(ser, 'S', 'A', 5)      # 帆向左转5度
            # print('a')
        elif keyboard.is_pressed('s'):
            send_cmd(ser, 'Q', 'A', 5)        # 帆回正
            # print('s')
        elif keyboard.is_pressed('d'):
            send_cmd(ser, 'S', 'D', 5)      # 帆向右转5度
            # print('d')
        elif keyboard.is_pressed('j'):
            send_cmd(ser, 'W', 'A', 45)     # 轮子向左转25度
            # print('j')
        elif keyboard.is_pressed('k'):
            send_cmd(ser, 'W', 'D', 3)        # 轮子回正
            # print('k')
        elif keyboard.is_pressed('l'):
            send_cmd(ser, 'W', 'D', 45)     # 轮子向右转25度
            # print('l')
        elif keyboard.is_pressed('q'):
            ser.close()
            print('Program exits.')
            break
        else:
            continue
        time.sleep(0.01)


detect_key()

if ser.isOpen():
    ser.close()
    