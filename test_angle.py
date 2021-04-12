import serial
import time
from threading import Thread
import keyboard

import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from PythonSample_mySQL import receiveNewFrame
from PythonSample_mySQL import receiveRigidBodyFrame
from PythonSample_mySQL import GetYachtPos, GetYachtRotation, GetSailRotation
# from PythonSample_mySQL import GetYachtPos, GetYachtRotation
from NatNetClient import NatNetClient
# from NatNetClient import terminate
from QuaternionToEuler import QuaternionToEuler

import inspect
import ctypes

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

def heading_direction():
    rotation_quaternion = GetYachtRotation()
    sail_quaternion = GetSailRotation()
    heading_ang = QuaternionToEuler(rotation_quaternion)  # TODO: 取数组中的一个方向的值
    sail_ang = QuaternionToEuler(sail_quaternion)
    yacht_val = heading_ang[2] + 90.5          # sail: + 116; yacht: -45
    sail_val = sail_ang[2] + 121.8
    if yacht_val > 180:
        yacht_val -= 360
    elif yacht_val < -180:
        yacht_val += 360
    
    if sail_val > 180:
        sail_val -= 360
    elif yacht_val < -360:
        sail_val += 360
    return yacht_val, sail_val


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# print("hello")
while True:
    time.sleep(0.01)
    print(heading_direction())

    if keyboard.is_pressed('z'):
        # terminate(streamingClient)
        # streamingClient.exit_flag = True
        # stop_thread(commandThread)
        # stop_thread(dataThread)
        # print("Before join.")
        # dataThread.join()
        # print("command thread joined")
        # commandThread.join()
        print("Program Exits.")
        break

# streamingClient.exit_flag = True
# stop_thread(commandThread)
# stop_thread(dataThread)
# print("Before join")
# dataThread.join()
# print("data thread")
# exit()
# commandThread.join()
