import numpy
from matplotlib import pyplot as plt

m = 0.78                        # total mass of car (kg)
Vt= 2.5                          # true wind speed (m/s)
S = 0.24                        # wing surface (m2)
rho = 1.225                     # air density (kg/m3)


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
    if Vc <= 0.01:
        Vr = Vt
    else:
        Vr = Vc*numpy.sin(gamma)/numpy.sin(theta)
    return Vr   #return relative wind speed

#get best sail angle between sail and car body
def getBestSa(Vc,gamma):
    global alphaList
    global CdList
    global ClList
    global rho
    global S
    gamma0 = gamma
    gamma = abs(gamma) * numpy.pi / 180
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
    alpha = alphaList[numpy.argmax(temp)] * numpy.pi / 180
    bestSa = abs(gamma - alpha - theta) * 180 / numpy.pi
    # bestSa = gamma - alphaList[numpy.argmax(temp)]
    if gamma0 <= 0:
        return -bestSa
    else:
        return bestSa

# print(getBestSa(1, 79.88166227746731))
# print(getBestSa(1, 78.23365868091936))
# print(getBestSa(1, 57.65584916468107))
# print(getBestSa(1, 25.161617650219736))

gammaList = []
sail_pos_list = []
for ang in range(0,180,1):
    gammaList.append(ang*numpy.pi/180)
    sail_pos = getBestSa(0, ang)
    sail_pos_list.append(sail_pos)

# plt.plot(gammaList, sail_pos_list)
# plt.show()
