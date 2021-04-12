from matplotlib import pyplot as plt
import  numpy as np
from scipy import integrate

from sail_angle import getBestSa, getAcc
from acceleration_relative import m, R
from get_c import get_c

######################################
# Given a certain course angle (gamma), initial velocity, and true wind velocity,
# calculate the kinetic energy change during the tacking process
# (i.e., the change in velocity) by assuming no sailing adjustment is made 
# on the path outside of the dead zone.
# The figure plotted by this program can be used to compare with 
# the experimental result (velocity - t) plotted before.
######################################


# acc theory
def get_AccLst(gammaLst, vc0, vt0):
    if gammaLst[0] < 30:
        print("Starting point is in deadzone.")
        return []
    alpha0, a0 = getBestSa(vc0, vt0, gammaLst[0])
    acclst = []
    # acclst.append(a0)
    for gamma in gammaLst:
        # The following 4 lines is marked as comments, which means we assume
        # the sail can be timely adjusted to the position of best AOA.
        # if gamma >= 30:
        #     delta_gamma = gammaLst[0] - gamma
        #     acc = getAcc(alpha0 - delta_gamma, gamma, vc0, vt0)
        # else:
        alpha, acc = getBestSa(vc0, vt0, gamma)
        c = get_c(gamma, vc0)
        # print("c: ", c, "\t ath: ", acc, "\t acc: ", acc+c)
        acc += c
        acclst.append(acc)
    return acclst

# Theoretical value of final kinetic energy
def get_V(gamma_lst, vc0, vt0):
    # step = -1
    # gamma_lst = []
    # for gamma in range(gamma0, gamma1, step):
    #     gamma_lst.append(gamma)
    # gamma_lst = np.arange(gamma0, gamma1, step, dtype=int)
    acclst = get_AccLst(gamma_lst, vc0, vt0)
    integral = - R * m * integrate.cumtrapz(acclst, gamma_lst, initial=0)
    integral = np.array(integral)
    # print("integral: ", integral)
    kinetic_final = integral + 1/2 * m * vc0 ** 2
    # v_lst = np.sqrt(2 / m * kinetic_final)
    return kinetic_final

# plotting
def plotting():
    gamma1 = 60
    gamma2 = 50
    gamma3 = 40
    gamma4 = 30
    gamma_final = -30
    vc = 0.8
    vc = 1.5
    vt = 2.5

    step = -1
    gamma_lst1 = np.arange(gamma1, gamma_final, step, dtype=int)
    gamma_lst2 = np.arange(gamma2, gamma_final, step, dtype=int)
    gamma_lst3 = np.arange(gamma3, gamma_final, step, dtype=int)
    gamma_lst4 = np.arange(gamma4, gamma_final, step, dtype=int)

    v_lst1 = get_V(gamma_lst1, vc, vt)
    v_lst2 = get_V(gamma_lst2, vc, vt)
    v_lst3 = get_V(gamma_lst3, vc, vt)
    v_lst4 = get_V(gamma_lst4, vc, vt)

    plt.plot(gamma_lst1, v_lst1, label="initial gamma = 70")
    plt.plot(gamma_lst2, v_lst2, label="initial gamma = 60")
    plt.plot(gamma_lst3, v_lst3, label="initial gamma = 50")
    plt.plot(gamma_lst4, v_lst4, label="initial gamma = 40")

    plt.show()

def plotting2():
    gamma_init = 50
    gamma_final = -30
    step = -1
    gamma_lst = np.arange(gamma_init, gamma_final, step, dtype=int)
    vt = 2.5
    vc1 = 0
    vc2 = 0.4
    vc3 = 0.8
    vc4 = 1.2

    v_lst1 = get_V(gamma_lst, vc1, vt)
    v_lst2 = get_V(gamma_lst, vc2, vt)
    v_lst3 = get_V(gamma_lst, vc3, vt)
    v_lst4 = get_V(gamma_lst, vc4, vt)

    plt.plot(gamma_lst, v_lst1, label="initial vel: 0")
    plt.plot(gamma_lst, v_lst2, label="initial vel: 0.4")
    plt.plot(gamma_lst, v_lst3, label="initial vel: 0.8")
    plt.plot(gamma_lst, v_lst4, label="initial vel: 1.2")

    plt.xlabel("gamma")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plotting()
    # plotting2()
