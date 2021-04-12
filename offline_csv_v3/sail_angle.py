# File: sail_angle.py
# Useful functions imported in other scripts: 
# true_wind, getAcc, getBestSa

import numpy
from matplotlib import pyplot as plt
from get_c import get_c

m = 0.845                        #total mass of car (kg)
# Vt= 2.5                          #true wind speed (m/s)
S = 0.24                        #wing surface (m2)
rho = 1.225                     #air density (kg/m3)


# Wind Field: quantized to levels with gap 0.1
def true_wind(x, y):
    p00 =        -449
    p10 =      -12.85
    p01 =       255.3
    p20 =     -0.4713
    p11 =       5.376
    p02 =      -53.45
    p30 =     0.01949
    p21 =     0.07749
    p12 =     -0.7742
    p03 =       4.906
    p40 =     0.02917
    p31 =     0.02083
    p22 =    0.002041
    p13 =      0.0375
    p04 =     -0.1667

    f_xy = p00 + p10*x + p01*y + p20*x**2 + p11*x*y + p02*y**2 \
         + p30*x**3 + p21*x**2*y + p12*x*y**2 + p03*y**3 + p40*x**4 \
         + p31*x**3*y + p22*x**2*y**2 + p13*x*y**3 + p04*y**4
    f_xy = round(f_xy, 1)

    return f_xy     # 保留一位小数

alphaList = []      #angle of attack
ClList = []         #Cl from data
CdList = []         #Cd from data

#load appha and Cl Cd relation data 
# f = open("foilData.txt","r")
# f = open("polar.txt", 'r')
f = open("polarnew.txt", 'r')
for line in f:
    alphaList.append(line[1:8])
    ClList.append(line[10:17])
    CdList.append(line[20:27])
f.close()
del alphaList[:2]
del ClList[:2]
del CdList[:2]

for i in range(0,len(alphaList)):
    alphaList[i] = float(alphaList[i])
for j in range(0,len(ClList)):
    ClList[j] = float(ClList[j])
for k in range(0,len(CdList)):
    CdList[k] = float(CdList[k])

#get relative wind dirction; sail angle = theta + alpha
def getDr(Vt,Vc, gamma):  #Vc:car velocity, gamma: course angle
    theta  = numpy.arctan((Vc*numpy.sin(gamma))/(Vt+Vc*numpy.cos(gamma)))
    if Vc <= 0.01:
        theta = 0
    return theta    #return angle between true wind and relative wind

#get relative wind speed
def getVr(Vt,Vc, gamma):
    theta = getDr(Vt,Vc,gamma)
    if Vc <= 0.01 or gamma == 0:
        Vr = Vt + Vc
    else:
        Vr = Vc*numpy.sin(gamma)/numpy.sin(theta)
    return Vr   #return relative wind speed

#get best sail angle between sail and car body
def getBestSa(Vc,Vt, gamma):  # 传入参数gamma为角度值
    global alphaList
    global CdList
    global ClList
    global rho
    global S
    gamma = gamma * numpy.pi / 180  # change to radius
    rWV = getVr(Vt,Vc,gamma)
    theta = getDr(Vt,Vc,gamma)
    temp = []
    for aoa in range(2,len(alphaList)):
        D = 0.5 * rho * rWV**2 * S * CdList[aoa]    # drag
        L = 0.5 * rho * rWV**2 * S * ClList[aoa]    # lift
        beta = numpy.arctan(L / D)
        R = numpy.sqrt(L**2 + D**2)
        Fh = R * numpy.cos(numpy.pi - gamma - beta + theta) #total force along course
        a = Fh / m
        temp.append(a)
    alphaInd = numpy.argmax(temp)
    alpha1 = alphaList[numpy.argmax(temp)] #* numpy.pi / 180  # alpha in degree
    alpha = alphaList[numpy.argmax(temp)] * numpy.pi / 180    # alpha in raduis
    bestSa = abs(gamma - alpha - theta) * 180 / numpy.pi      # bestSa in degree
    besta = temp[alphaInd + int(0 / 0.25)]
    # besta = temp[alphaInd]
    # bestSa = gamma - alphaList[numpy.argmax(temp)]
    # return alpha1, besta     # return best AOA and corresponding acc
    return bestSa, besta       # return best sailing angle and corresponding acc

# Return acc of specified alpha (which may not be the best AOA)
def getAcc(alpha, gamma, vc, vt):
    global alphaList
    global CdList
    global ClList
    global rho
    global S
    gamma = gamma * numpy.pi / 180  # change to radius
    rWV = getVr(vt,vc,gamma)
    theta = getDr(vt,vc,gamma)
    alpha0 = alpha
    alpha = abs(int(alpha))
    if alpha not in alphaList:
        # if alpha == 12:
        #     i_alpha = 44
        #     print("Cl: ", ClList[i_alpha], '\t', "Cd: ", CdList[i_alpha])
        # else:
        print("wrong input of alpha with value: ", alpha)
        return -1
    else:
        i_alpha = alphaList.index(alpha)
    D = 0.5 * rho * rWV**2 * S * CdList[i_alpha]    # drag
    L = 0.5 * rho * rWV**2 * S * ClList[i_alpha]    # lift
    # if alpha0 < 0:
    #     L = -L
    beta = numpy.arctan(L / D)
    R = numpy.sqrt(L**2 + D**2)
    if alpha0 >= 0:
        Fh = R * numpy.cos(numpy.pi - gamma - beta + theta) # total force along course
    else:
        Fh = R * numpy.cos(beta + theta - gamma)
    a = Fh / m
    return a

gammaList = []
sail_pos_list = []
a_gamma_list = []

gamma = 50
Vt = 2.5
Vc = 1.3

vt_list = numpy.arange(1.8, 2.7, 0.1)
a_vt_list = []
vc_list = numpy.arange(0, 1.5, 0.1)
a_vc_list = []

for ang in range(-30,80,1):
    gammaList.append(ang)
    sail_pos, a = getBestSa(Vc, Vt, ang)
    sail_pos_list.append(sail_pos)
    c = get_c(ang, Vc)
    a_gamma_list.append(a+c)

for v_t in vt_list:
    ang, a = getBestSa(Vc, v_t, gamma)
    c = get_c(gamma, Vc)
    c = 0
    a_vt_list.append(a + c)

for v_c in vc_list:
    ang, a = getBestSa(v_c, Vt, gamma)
    c = get_c(gamma, v_c)
    c = 0
    a_vc_list.append(a + c)

if __name__ == "__main__":
    plt.plot(gammaList, a_gamma_list)
    # plt.plot(vt_list, a_vt_list)
    plt.plot(vc_list, a_vc_list)
    plt.show()
