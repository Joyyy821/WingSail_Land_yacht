# File: get_const.py
# This file reads the data from a SINGLE csv file recorded in Motion Capture,
# and plot 8 subfigures accordingly.
# Remember to change the file path and the starting index of required data before 
# executing this program.

import csv
import numpy as np
from matplotlib import pyplot as plt

from QuaternionToEuler import QuaternionToEuler
from sail_angle import true_wind, getBestSa
import acceleration_relative as ar 
from acceleration_relative import rho,S,Vt,m,alphaList,ClList,CdList
from get_const2 import acc_theory


################################
### Read data from csv files ###
################################


idx_lst = []
t = []
sail_rotation = []
yacht_rotation = []
x = []
y = []
t_v = []
t_a = []
vel = []
acc = []
acc_th = []
Vt_lst = []

f_i = '021' # The index of the csv file.

# TODO: Change the directory
# with open("F:\\RAIL\\WSL\\MotionCapture\\offline_csv_v3\\exp20210327\\sailyacht_0327_"+ f_i +".csv", newline='') as csv_f:
with open("sample.csv", newline='') as csv_f:
    f_reader = csv.reader(csv_f)
    i = 0 
    for row in f_reader:
        # print(row)
        i = i + 1
        if i <= 7:
            continue
        idx = eval(row[0])
        gap = 10
        if idx % gap != 0:
            continue
        idx = int(idx/gap)

        idx_lst.append(idx)
        c_t = eval(row[1])
        # if c_t >= 6:
        #     break
        t.append(c_t)

        # TODO: check the index
        if row[2] == '':
            if row[10] == '':
                if idx >= 1:
                    # print(idx)
                    sail_rot = sail_rotation[idx-1]
                else:
                    sail_rot = 0
                sail_rotation.append(sail_rot)
            # continue
            else:
                qx2, qy2, qz2, qw2 = eval(row[10]), eval(row[11]), eval(row[12]), eval(row[13])
                q2 = [qw2, qx2, qy2, qz2]
                sail_rot = QuaternionToEuler(q2)[2] + 90.5
                if sail_rot > 180:
                    sail_rot -= 360
                elif sail_rot < -180:
                    sail_rot += 360
                sail_rotation.append(sail_rot)
            if idx >= 1:
                yacht_rot = yacht_rotation[idx-1]
                # sail_rot = sail_rotation[idx-1]
                c_x = x[idx-1]
                c_y = y[idx-1]
                if idx >= 2:
                    v = vel[idx-2]
                    if idx >= 3:
                        a = acc[idx-3]
                    else:
                        a = 0
                    acc.append(a)
                    c_t_a = (c_t_v + t_v[idx-2])/2
                    t_a.append(c_t_a)
                else:
                    v = 0
                vel.append(v)
                c_t_v = (c_t + t[idx-1]) / 2
                t_v.append(c_t_v)
            else:         # idx == 0
                yacht_rot = 0
                # sail_rot = 0
                c_x = 0
                c_y = 0
            yacht_rotation.append(yacht_rot)
            # sail_rotation.append(sail_rot)
            x.append(c_x)
            y.append(c_y)
            continue

        qx1, qy1, qz1, qw1 = eval(row[2]), eval(row[3]), eval(row[4]), eval(row[5])
        q1 = [qw1, qx1, qy1, qz1]
        yacht_rot = QuaternionToEuler(q1)[2] + 121.8
        if yacht_rot > 180:
            yacht_rot -= 360
        elif yacht_rot < -180:
            yacht_rot += 360
        yacht_rotation.append(yacht_rot)

        if row[10] == '':
            if idx >= 1:
                # print(idx)
                sail_rot = sail_rotation[idx-1]
            else:
                sail_rot = 0
            sail_rotation.append(sail_rot)
            # continue
        else:
            qx2, qy2, qz2, qw2 = eval(row[10]), eval(row[11]), eval(row[12]), eval(row[13])
            q2 = [qw2, qx2, qy2, qz2]
            # print(q2)
            sail_rot = QuaternionToEuler(q2)[2] + 90.5
            if sail_rot > 180:
                    sail_rot -= 360
            elif sail_rot < -180:
                sail_rot += 360
            sail_rotation.append(sail_rot)

        c_x = eval(row[6])
        c_y = eval(row[8])
        x.append(c_x)
        y.append(c_y)

        if idx >= 1:
            # print(idx)
            v = np.sqrt((c_x - x[idx-1]) ** 2 + (c_y - y[idx-1]) ** 2) / (c_t - t[idx-1])
            c_t_v = (c_t + t[idx-1]) / 2
            # if v >= 5 and idx >= 2:
            #     v = vel[idx-2]
            # elif idx == 1:
            #     v = 0
            vel.append(v)
            t_v.append(c_t_v)    # 速度v对应的时刻
        if idx >= 2:
            # print(idx)
            a = (v - vel[idx-2]) / (c_t_v - t_v[idx-2])
            c_t_a = (c_t_v + t_v[idx-2])/2
            # if (a >= 100 or a <= -100) and idx >= 3:
            #     a = acc[idx-3]
            # elif idx == 2:
            #     a = 0
            acc.append(a)
            t_a.append(c_t_a)    # 加速度a对应的时刻
        # TODO: sail rotation

last_v = vel[-1]
vel.append(last_v)

sail_rotation, yacht_rotation = yacht_rotation, sail_rotation

# Generate list of theoretical acc
for i in range(len(x)):
    v_t = true_wind(x[i], y[i])
    Vt_lst.append(v_t)
    gamma = -yacht_rotation[i]
    v_c = vel[i]
    # print(v_t)
    # print(v_c)
    # print(gamma)
    a_th = acc_theory(v_c, v_t, gamma)
    acc_th.append(a_th)

# best alpha
best_alpha = []
for i in range(len(t)):
    vt = Vt_lst[i]
    vc = vel[i]
    gamma = yacht_rotation[i]
    alpha, sa = getBestSa(vc, vt, gamma)
    # alpha = alpha + gamma
    best_alpha.append(-alpha)

plt.subplot(241)
plt.title("x-y Position")
plt.scatter(y, x)

plt.subplot(242)
plt.title("yacht rotation - t")
plt.scatter(t, yacht_rotation)

# del vel[-1]

plt.subplot(243)
plt.title("vel - t")
# plt.plot(t_v, vel)
plt.scatter(t, vel)

sail_rotation = np.array(sail_rotation)
yacht_rotation = np.array(yacht_rotation)
sailing = yacht_rotation - sail_rotation

plt.subplot(244)
# plt.title("sail turnning - t")
plt.title("acc - t")
plt.scatter(t_a, acc)
# plt.scatter(t, sailing)

plt.subplot(245)
plt.title("acc theo - t")
plt.scatter(t, acc_th)

plt.subplot(246)
# plt.title("sail roation - t")
# plt.scatter(t, sail_rotation)
plt.title("true wind - t")
plt.scatter(t, Vt_lst)

plt.subplot(247)
# plt.title("best alpha - t")
plt.title("best sail angle - t")
plt.scatter(t, best_alpha)

plt.subplot(248)
plt.title("sail turnning - t")
plt.scatter(t, sailing)


plt.show()

