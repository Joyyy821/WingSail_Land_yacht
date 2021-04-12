# File: acceleration_relative.py
# This file initially used for checking the calculation of the value of
# acceleration and the best angle of attack.
# This file is edited at the early stage of this project. The 
# theoretical model may be different from the final one.
# The constant physical quantities are imported in other scripts.

import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Constant physical quantities
m = 0.845                        #total mass of car (kg)
Vt= 2.5                          #true wind speed (m/s)
S = 0.24                        #wing surface (m2)
rho = 1.225                     #air density (kg/m3)

L = 0.65                    # Lenght of the land-yacht body(m)
d0 = 0.12                   # Length from the center of mass to the rear wheels(m)
w = 50 * numpy.pi / 180                 # Maximum steering angle (radian)
R = numpy.sqrt(d0 ** 2 + (L / numpy.tan(w)) ** 2)    # Minimum steering radius(m)

alphaList = []      #angle of attack
ClList = []         #Cl from data
CdList = []         #Cd from data
gammaList = []      #course angle
dgamma = 1          #course angle step size/ degree
wsaList = []

VcList = []         #car speed

VcList = [0.1*v for v in range(0,12,3)]

#get relative wind dirction; sail angle = theta + alpha
def getDr (Vt,Vc, gamma):  #Vc:car velocity, gamma: course angle
    gamma = gamma * 180 / numpy.pi
    theta  = numpy.arctan((Vc*numpy.sin(gamma))/(Vt+Vc*numpy.cos(gamma)))
    theta = theta * 180 / numpy.pi
    return theta    #return angle between true wind and relative wind

#get relative wind speed
def getVr (Vt, Vc, gamma):
    gamma = gamma * 180 / numpy.pi
    theta = getDr(Vt,Vc,gamma)
    if Vc == 0 or gamma == 0:
        Vr = Vt + Vc
    else:
        Vr = Vc*numpy.sin(gamma)/numpy.sin(theta)
    return Vr   #return relative wind speed

for ang in range(0,181,dgamma):
    gammaList.append(ang*numpy.pi/180)

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

def getAcc (Vc):
    accList = [[]]      #acceleration along course direction
    for course in gammaList:
        temp = []
        rWV = getVr(Vt,Vc,course)
        for aoa in range(0,len(alphaList)):
        
            D = 0.5 * rho * rWV**2 * S * CdList[aoa]    #drag
            L = 0.5 * rho * rWV**2 * S * ClList[aoa]    #lift
            beta = numpy.arctan(L / D)
            theta = getDr(Vt,Vc,course)
            R = numpy.sqrt(L**2 + D**2)
            Fh = R * numpy.cos(numpy.pi - course - beta + theta) #total force along course
            a = Fh / m
            temp.append(a)

        accList.append(temp)
    del accList[0]
    return accList


#get the best aoa for different course angles
def getBestAoa(Vc,gamma):
    rWV = getVr(Vt,Vc,gamma)
    temp = []
    for aoa in range(2,len(alphaList)):
            D = 0.5 * rho * rWV**2 * S * CdList[aoa]    #drag
            L = 0.5 * rho * rWV**2 * S * ClList[aoa]    #lift
            beta = numpy.arctan(L / D)
            R = numpy.sqrt(L**2 + D**2)
            Fh = R * numpy.cos(numpy.pi - gamma - beta) #total force along course
            a = Fh / m
            temp.append(a)
    bestAoa = alphaList[numpy.argmax(temp)]
    return bestAoa

#get best sail angle between sail and car body
def getBestSa(Vc,gamma):
    rWV = getVr(Vt,Vc,gamma)
    theta = getDr(Vt,Vc,gamma)
    temp = []
    for aoa in range(2,len(alphaList)):
            D = 0.5 * rho * rWV**2 * S * CdList[aoa]    #drag
            L = 0.5 * rho * rWV**2 * S * ClList[aoa]    #lift
            beta = numpy.arctan(L / D)
            R = numpy.sqrt(L**2 + D**2)
            Fh = R * numpy.cos(numpy.pi - gamma - beta + theta) #total force along course
            a = Fh / m
            temp.append(a)
    bestSa = gamma - abs(alphaList[numpy.argmax(temp)]) - abs(theta)
    return bestSa


def getF(Vc,gamma,c):
    rWV = getVr(Vt,Vc,gamma)
    temp = []
    for aoa in range(2,len(alphaList)):
            D = 0.5 * rho * rWV**2 * S * CdList[aoa]    #drag
            L = 0.5 * rho * rWV**2 * S * ClList[aoa]    #lift
            beta = numpy.arctan(L / D)
            R = numpy.sqrt(L**2 + D**2)
            Fh = R * numpy.cos(numpy.pi - gamma - beta) #total force along course
            a = Fh / m
            temp.append(a)
    F = max(temp)
    return F+c

def getV1(v0,gamma,c):
    ek = 0.5*m*v0**2
    work = getF(v0,gamma,c)*dgamma*R
    v1 = numpy.sqrt(2*(ek-work)/m)
    return v1

def getdz(v0,gamma0):
    global c
    global R
    gamma1 = gamma0 - 2
    
    if getF(v0,gamma0,c) <= 0:
        return 
    else:
        ek0 = 0.5*m*v0**2
        work = 0
        print("=====")
        while ek0 >= -work :
            v = v0
            
            for angle in gammaList[gamma0+180:gamma1+180:-1]:
                work += R * getF(v,angle,c)*dgamma*numpy.pi/180
                v = getV1(v,angle,c)
            gamma1 = gamma1 -1
            
    return gamma1

acc = getAcc(5)
# print(len(gammaList))
# print(len(alphaList))
# print(len(acc))
# for spd in VcList:
#     x = [radius*180/numpy.pi for radius in gammaList]
#     y = [getBestSa(spd,i) for i in gammaList]
#     plt.plot(x,y, label = str(spd)+"m/s")

# plt.xlabel('course angle/ degree')
# plt.ylabel('sailangle/ degree')
# plt.legend()
# plt.show() 

# for spd in VcList:
#     x = [radius*180/numpy.pi for radius in gammaList]
#     y = [getF(spd,i,c) for i in gammaList]
#     plt.plot(x,y, label = str(spd)+"m/s")

# plt.xlabel('course angle/ degree')
# plt.ylabel('force/ N')
# plt.legend()
# plt.show() 
frac = []
for n in range(0,len(alphaList)):
    frac.append (ClList[n] / CdList[n])
# plt.plot(alphaList,frac)
#plt.show()


#plot
#print([alphaList[i] for i in numpy.argmax(acc,axis = 1)])
#print([getBestAoa(3,i) for i in gammaList])

# X = numpy.array(alphaList)
# Y = numpy.array(gammaList)
# X,Y = numpy.meshgrid(X,Y)
# Z = numpy.array(acc)

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot_surface(X, Y, Z)

# plt.show()
