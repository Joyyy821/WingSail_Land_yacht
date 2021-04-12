# File: integration.py
# Plot the change of kinetic energy with respect to gamma according the 
# Work-Energy theory. The starting point is from the right side of the figure
# (as gamma is decreasing during the tacking).

import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from acceleration_relative import m, R
from get_c import get_c
from tacking_no_acc_test import get_AccLst

def integration(gamma1, gamma2, Vc, Vt):
    step = -1
    acc_lst = []
    gamma_lst = []

    gamma_lst = np.arange(gamma1, gamma2, -1, dtype=int)
    acc_lst = get_AccLst(gamma_lst, Vc, Vt)
    # print(gamma_lst)
    # integral = - R * m * np.trapz(acc_lst, gamma_lst)
    integral = - R * m * integrate.cumtrapz(acc_lst, gamma_lst, initial=0)
    # print(integral)
    return integral#[-1] * 2
    # return acc_lst


if __name__ == "__main__":
    gamma1 = 40
    gamma2 = -30

    gamma_lst1 = list(range(gamma1, gamma2, -1))
    # gamma_lst2 = list(range(gamma3, gamma2, -1))
    # gamma_lst3 = list(range(gamma4, gamma2, -1))
    vt = 2.8

    v1 = 0.4
    v2 = 0.8
    v3 = 1.2
    integral_lst1 = integration(gamma1, gamma2, v1, vt) + 0.5 * m * v1**2
    integral_lst2 = integration(gamma1, gamma2, v2, vt) + 0.5 * m * v2**2
    integral_lst3 = integration(gamma1, gamma2, v3, vt) + 0.5 * m * v3**2

    plt.plot(gamma_lst1, integral_lst1, label='integral: v = 0.4')
    plt.plot(gamma_lst1, integral_lst2, label='integral: v = 0.8')
    plt.plot(gamma_lst1, integral_lst3, label='integral: v = 1.2')
    # plt.plot(v_lst, integral_lst2, label='integral: gamma = 50')
    # plt.plot(v_lst, integral_lst3, label='integral: gamma = 70')
    # plt.plot(v_lst, Ek, label='1/2 * m * v^2')
    plt.xlabel("gamma")
    plt.legend()
    plt.show()
