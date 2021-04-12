# File: get_const2.py
# This program read offline data obtained by Motion Capture.
# By processing the data with noise filter and differentiator,
# we obtain experimental vel and acc.
# Theoretical acc is also calculated to get the difference.
# Results will be write into a text file for further smoothing
# and visualization in Matlab.

# REMEMBER: 注意向txt文件写入数据会覆盖之前的数据，若要保留原始数据记得在运行程序前修改文件名

# Edition notes: This file was later used to plot the experimental data and theoretical reference
# line and interval.

#############################################
### Import relative modules and functions ###
#############################################

import csv
import numpy as np
from matplotlib import pyplot as plt

from QuaternionToEuler import QuaternionToEuler
from sail_angle import true_wind, getBestSa, getDr, getVr
from acceleration_relative import rho,S,Vt,m,alphaList,ClList,CdList
# import calculate_V0


###############################
### Initialization of lists ###
###############################

t_lst = []                         # time
sail_rot_lst = []                  # alpha
yacht_rot_lst = []                 # gamma
x_lst = []                         # yacht position x
y_lst = []                         # yacht position y
Vc_lst = []                        # car velocity
Vt_lst = []                        # true wind velocity
acc_exp_lst = []                   # experimental acceleration
acc_th_lst = []                    # theoretical acceleration
c_lst = []                         # differnece between acc_exp and acc_th


################################
### Read data from csv files ###
################################

# TODO: change the file path
file_path = "F:\\RAIL\\WSL\\MotionCapture\\offline_csv_v3\\exp20210327\\sailyacht_0327_"

def get_file(file_idx, file_path):
    file_extension = ".csv"
    str_f_idx = str(file_idx)
    l = len(str_f_idx)

    if l == 1:
        str_f_idx = "00" + str_f_idx
    elif l == 2:
        str_f_idx = "0" + str_f_idx
    else:
        print("Invalid file name with wrong file index.")

    return file_path + str_f_idx + file_extension

# Read data from all csv files
# TODO: abandant exp data which is not good
def read_csv(file_path, data_gap=1):
    global t_lst
    global sail_rot_lst
    global yacht_rot_lst
    global x_lst
    global y_lst

    i_start = 1
    i_end = 21
    # i_rm_lst = [4, 5, 6, 10, 13, 15, 17, 19]

    i_t_st_map = [16, 4, 16, 0, 15, 2, 12, 5, 4, 2, 18, 7.5, 0, 14, 2, 6, 2.5, 2, 0, 4, 10]
    i_t_end_map = [22, 8, 21, 7.5, 25, 6, 16, 10, 8, 4, 26, 15, 0, 18, 6, 11, 7.5, 8, 0, 12, 15]

    for i in range(i_start, i_end+1):
        # if i in i_rm_lst:
        #     if i == 19:
        #         continue
            # else:

        file_name = get_file(i, file_path)
        with open(file_name, newline='') as csv_f:
            f_reader = csv.reader(csv_f)
            row_i = 0
            for row in f_reader:
                row_i += 1
                if row_i <= 7:
                    continue
                idx = eval(row[0])
                if idx % data_gap != 0:
                    continue
                if row[10] == '':
                    continue

                # time
                t = eval(row[1])
                if t <= i_t_st_map[i - i_start]:
                    continue
                if t >= i_t_end_map[i - i_start]:
                    break
                t_lst.append(t - i_t_st_map[i - i_start])

                # yacht rotation
                qx1, qy1, qz1, qw1 = eval(row[10]), eval(row[11]), eval(row[12]), eval(row[13])
                q1 = [qw1, qx1, qy1, qz1]
                yacht_rot = QuaternionToEuler(q1)[2] + 90.5
                yacht_rot_lst.append(yacht_rot)

                # yacht position
                x = eval(row[14])
                y = eval(row[16])
                x_lst.append(x)
                y_lst.append(y)


########################################################
### Process data to obtain velocity and acceleration ###
########################################################

def get_gamma(data_gap=10):
    global t_lst
    global yacht_rot_lst
    l = len(yacht_rot_lst)
    for i in range(0, l, data_gap):
        if yacht_rot_lst[i] > 0:
            if t_lst[i] == 0:
                yacht_rot_lst[i] = 0
            else:
                yacht_rot_lst[i] = yacht_rot_lst[i-1]
        yacht_rot_lst[i] = abs(yacht_rot_lst[i])
    # return []


def get_true_wind(data_gap=10):
    global Vt_lst
    global x_lst
    global y_lst
    l = len(x_lst)
    for i in range(0, l, data_gap):
        v_t = true_wind(x_lst[i], y_lst[i])
        Vt_lst.append(v_t)


def get_car_vel(data_gap=10):
    global Vc_lst
    global x_lst
    global y_lst
    global t_lst
    
    l = len(x_lst)
    for i in range(0, l, data_gap):
        # print(i)
        if i + data_gap >= l or t_lst[i] >= t_lst[i+data_gap]:
            # print(i/data_gap - 1)
            v = Vc_lst[int(i/data_gap - 1)]
            # Vc_lst.append(v)
        else:
            v = np.sqrt((x_lst[i] - x_lst[i+data_gap]) ** 2 \
                 + (y_lst[i] - y_lst[i+data_gap]) ** 2) / (t_lst[i+data_gap] - t_lst[i])
        Vc_lst.append(v)

    # TODO: filtering
    i_v = 0
    for i in range(0, l, data_gap):
        if i + data_gap < l and t_lst[i] < t_lst[i+data_gap]:
            diff = Vc_lst[i_v+1] - Vc_lst[i_v]
            if diff >= 0.2:
                Vc_lst[i_v+1] = Vc_lst[i_v]
            elif diff <= -0.2:
                Vc_lst[i_v] = Vc_lst[i_v+1]
        i_v += 1
    # l_v = len(Vc_lst)
    # for i_v in range(l_v):
    #     if i_v < l_v-1:
    #         diff = Vc_lst[i_v]
    #         if Vc_lst[i_v]


def get_exp_acc(data_gap=10):
    # Differential
    global t_lst
    global Vc_lst
    global acc_exp_lst

    i_st = 0
    i_ed = 0
    l = len(t_lst)
    current_t_lst = []
    current_v_lst = []
    current_a_lst = []

    i_v = 0
    i_v_st = 0
    i_v_ed = 0
    for i in range(0, l, data_gap):
        if i + data_gap >= l or t_lst[i] >= t_lst[i+data_gap]:
            i_ed = i + 1
            i_v_ed = i_v + 1
            current_t_lst = t_lst[i_st:i_ed:data_gap]
            current_v_lst = Vc_lst[i_v_st:i_v_ed]
            current_t_lst = np.array(current_t_lst)
            current_v_lst = np.array(current_v_lst)
            # print(len(current_t_lst))
            # print(len(current_v_lst))
            current_a_lst = np.gradient(current_v_lst, current_t_lst)
            for a in current_a_lst:
                acc_exp_lst.append(a)
            i_st = i + data_gap
            i_v_st = i_v_ed
        i_v += 1
    
    # Filtering of exp acc
    i_a = 0
    for i in range(0, l, data_gap):
        if abs(acc_exp_lst[i_a]) >= 1.0:
            if i == 0 or t_lst[i-data_gap] >= t_lst[i]:
                acc_exp_lst[i_a] = 0
            else:
                acc_exp_lst[i_a] = acc_exp_lst[i_a-1]
        i_a += 1
    # pass


# Calculate theoretical acceleration based on given Vc, Vt, and gamma
def acc_theory(Vc, Vt, gamma):
    alpha, a = getBestSa(Vc, Vt, gamma)
    return a


def get_theo_acc(data_gap=10):
    global Vc_lst
    global Vt_lst
    global yacht_rot_lst
    global acc_th_lst

    l = len(Vc_lst)
    for i in range(0, l):
        a_th = acc_theory(Vc_lst[i], Vt_lst[i], yacht_rot_lst[i * data_gap])
        acc_th_lst.append(a_th)
    # pass


vt_tack_lst = []
def get_v(data_gap=10):
    global Vc_lst
    global t_lst
    global vt_tack_lst

    i_rm_lst = [4, 5, 6, 10, 14, 16]

    v0_lst = []
    v1_lst = []
    Vc_lst = np.array(Vc_lst)

    l = len(Vc_lst)
    i_start = 0
    for i in range(0, l):
        if i < l-1 and t_lst[i * data_gap] >= t_lst[(i+1) * data_gap]:
            # find max and min between i_Start and i, then append values to v0 and v1 list, then set new i_Start
            current_vc_lst = Vc_lst[i_start:i+1]
            v0 = np.amax(current_vc_lst)
            i_tack = np.argmax(current_vc_lst)
            vt_tack = Vt_lst[i_tack]
            vt_tack_lst.append(vt_tack)
            v1 = np.amin(current_vc_lst)
            # Ek0 = 0.5 * m * v0**2
            # Ek1 = 0.5 * m * v1**2
            v0_lst.append(v0)
            v1_lst.append(v1)
            i_start = i

    current_vc_lst = Vc_lst[i_start:]
    v0 = np.amax(current_vc_lst)
    i_tack = np.argmax(current_vc_lst)
    vt_tack = Vt_lst[i_tack]
    vt_tack_lst.append(vt_tack)
    v1 = np.amin(current_vc_lst)
    v0_lst.append(v0)
    v1_lst.append(v1)

    i_st = 1
    for i in range(i_st, len(v0_lst)+1):
        if i in i_rm_lst:
            v1_lst[i-1] = 0
    return v0_lst, v1_lst

#########################################
### Write data lists into a text file ###
#########################################

def writing(data_gap=10):
    global yacht_rot_lst
    global Vc_lst
    global Vt_lst
    global c_lst

    l = len(yacht_rot_lst)
    f = open("exp_acc_polar_high.txt", 'w')
    i_c = 0
    for i in range(0, l, data_gap):
        current_gamma = str(yacht_rot_lst[i])
        current_Vc = str(Vc_lst[i_c])
        current_Vt = str(Vt_lst[i_c])
        current_c = str(c_lst[i_c])
        f.write(current_gamma + '\t' + current_Vc + '\t' + current_Vt + '\t' + current_c + '\n')
        i_c += 1
    f.close()
    print("finish writing")


################
### Plotting ###
################

def plotting():
    global Vc_lst
    global acc_th_lst
    global acc_exp_lst
    global c_lst

    l = len(Vc_lst)
    x = list(range(l))

    plt.subplot(221)
    plt.title("Vc")
    plt.scatter(x, Vc_lst)

    plt.subplot(222)
    plt.title("acc exp")
    plt.scatter(x, acc_exp_lst)

    plt.subplot(223)
    plt.title("acc theo")
    plt.scatter(x, acc_th_lst)

    plt.subplot(224)
    plt.title("Difference c")
    plt.scatter(x, c_lst)

    plt.show()
    # pass


#####################
### Main function ###
#####################

if __name__ == '__main__':
    data_gap = 10
    read_csv(file_path)

    # Calculation
    get_gamma(data_gap)
    get_true_wind(data_gap)
    get_car_vel(data_gap)
    # get_exp_acc(data_gap)
    # get_theo_acc(data_gap)


    # Difference between experimental and theoretical results
    # l = len(acc_exp_lst)
    # for i in range(l):
    #     c = acc_exp_lst[i] - acc_th_lst[i]
    #     c_lst.append(c)

    # Write data
    # writing(data_gap)

    # Plot
    # plotting()

    v0_lst, v1_lst = get_v(data_gap)
    print(v0_lst)
    print("---------------")
    print(v1_lst)
    v0_lst_success = []
    v0_lst_fail = []
    v1_lst_success = []
    v1_lst_fail = np.zeros(6)

    l = len(v0_lst)
    for i in range(l):
        if v1_lst[i] == 0:
            v0_lst_fail.append(v0_lst[i])
        else:
            v0_lst_success.append(v0_lst[i])
            v1_lst_success.append(v1_lst[i])

    plt.scatter(v0_lst_success, v1_lst_success, color="r", marker='o', facecolors='none')
    plt.scatter(v0_lst_fail, v1_lst_fail, s=50, color='black', marker='x')
    plt.show()
    # vt_tack_lst = np.array(vt_tack_lst)
    # v_Avg = np.average(vt_tack_lst)
    # v_min = np.amin(vt_tack_lst)
    # v_max = np.amax(vt_tack_lst)
    # print(v_Avg)
    # print(v_min)
    # print(v_max)
