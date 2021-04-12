# File: calculate_V0.py
# Plotting: the work done by net force during the tacking/the 
# initial kinetic energy of the land-yacht v.s. the initial speed.

import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from get_const2 import acc_theory
from acceleration_relative import m, R
from tacking_no_acc_test import get_AccLst
from get_c import get_c


no_tacking_lst = []

def integration(gamma1, gamma2, Vc, Vt):
    step = -1
    acc_lst = []
    gamma_lst = []
    global no_tacking_lst

    # Vc = Vc * 0.5
    
    # for gamma in range(gamma1, gamma2, step):
    #     gamma_lst.append(gamma)
        # a_th = acc_theory(Vc, Vt, gamma)
        # c = get_c(gamma, Vc)
        # # print(c)
        # # print(a_th)
        # a = a_th + c
        # # if gamma == gamma1:
        # #     print(c)
        #     # print(a_th)
        # acc_lst.append(a)
    # print(acc_lst)
    # print(gamma_lst)
    gamma_lst = np.arange(gamma1, gamma2, step, dtype=int)
    acc_lst = get_AccLst(gamma_lst, Vc, Vt)
    # print(gamma_lst)
    # integral = R * m * np.trapz(acc_lst, gamma_lst)
    integral = R * m * integrate.cumtrapz(acc_lst, gamma_lst, initial=0)
    # print(integral)
    Ek0 = 0.5 * m * Vc ** 2
    # if integral[-1] <= Ek0:
    #     for i in integral:
    #         ek = Ek0 - i
    #         if ek < 0:
    #             no_tacking_lst.append(Vc)
    #             return
    # print(Vc)
    i_min = np.argmin(integral)
    integral = integral[i_min:]
    return np.amax(integral)
    # return integral[-1]
    # return acc_lst


# if __name__ == "__main__":
gamma1 = 40
gamma2 = -30
# gamma3 = 40
# gamma4 = 50
# gamma5 = 60
# gamma6 = 70
# gamma_lst = list(range(gamma1, gamma2, -1))

v_lst = []
integral_lst1 = []
integral_lst2 = []
integral_lst3 = []
integral_lst4 = []
integral_lst5 = []
vt = 2.3

vt1 = 2.13
vt2 = 2.17
vt3 = 2.2
# vt4 = 2.6
# vt5 = 2.8

# integral_lst1 = integration(gamma1, gamma2, 1.2, vt)
for i in range(20, 100):
    v = i/100
    v_lst.append(v)
    integral1 = integration(gamma1, gamma2, v, vt1)
    integral2 = integration(gamma1, gamma2, v, vt2)
    integral3 = integration(gamma1, gamma2, v, vt3)
    # integral4 = integration(gamma1, gamma2, v, vt4)
    # integral5 = integration(gamma1, gamma2, v, vt5)

    integral_lst1.append(integral1)
    integral_lst2.append(integral2)
    integral_lst3.append(integral3)
    # integral_lst4.append(integral4)
    # integral_lst5.append(integral5)

# for v in no_tacking_lst:
#     integral2 = integration(gamma1, gamma2, v, vt)
#     integral_lst2.append(integral2)
# print(integral_lst1)
v_lst = np.array(v_lst)
Ek = 0.5 * m * v_lst ** 2

integral_lst1 = Ek - integral_lst1
integral_lst2 = Ek - integral_lst2
integral_lst3 = Ek - integral_lst3
# integral_lst4 = Ek - integral_lst4
# integral_lst5 = Ek - integral_lst5

E_final_lst1 = np.maximum(integral_lst1, 0)
E_final_lst2 = np.maximum(integral_lst2, 0)
E_final_lst3 = np.maximum(integral_lst3, 0)

E_final_lst1 = np.sqrt(2 * E_final_lst1 / m)
E_final_lst2 = np.sqrt(2 * E_final_lst2 / m)
E_final_lst3 = np.sqrt(2 * E_final_lst3 / m)

zero = np.zeros(len(v_lst))
print(E_final_lst2)
for i in range(len(E_final_lst2)):
    if E_final_lst2[i] == 0:
        continue
    else:
        E0 = v_lst[i-1]
        break


# E_final_lst4 = Ek - integral_lst4
# E_final_lst5 = Ek - integral_lst5
# print(v_lst)
# print("-------------------")
# print(integral_lst1)
# plt.plot(v_lst, integral_lst1, label="vt = 2.0")
# plt.plot(v_lst, integral_lst2, label="vt = 2.2")
# plt.plot(v_lst, integral_lst3, label="vt = 2.4")
# plt.plot(v_lst, integral_lst4, label="vt = 2.6")
# plt.plot(v_lst, integral_lst5, label="vt = 2.8")
# plt.plot(v_lst, Ek, label='Initial kinetic energy')
# plt.plot(v_lst, E_final_lst1, label="vt = 2.1")
plt.plot(v_lst, E_final_lst2, label="vt = 2.2")
# plt.plot(v_lst, E_final_lst3, label="vt = 2.3")
# plt.plot(v_lst, zero, label="zero")
# plt.plot(v_lst, E_final_lst4, label="vt = 2.2")
# plt.plot(v_lst, E_final_lst5, label="vt = 2.4")
plt.fill_between(v_lst, E_final_lst1, E_final_lst3, color="cyan", alpha="0.25")
x = [0.2, 0.2, E0, E0]
y = [0, 1.4, 1.4, 0]
plt.fill(x, y, facecolor='grey', alpha = 0.5)

plt.xlabel("Initial velocity V0 (m/s)")
# plt.ylabel("Initial kinetic energy or Work done in the tacking process (J)")
plt.ylabel("Final velocity V1 (m/s)")
# plt.legend()
# plt.show()
