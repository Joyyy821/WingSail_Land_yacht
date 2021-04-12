import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

m = 0.05                        #total mass of car (kg)
v = 2                           #wind speed (m/s)
S = 0.24                        #wing surface (m2)
rho = 1.225                     #air density (kg/m3)

alphaList = []
ClList = []
CdList = []
gammaList = []
accList = [[]]

for ang in range(0,180,5):
    gammaList.append(ang*numpy.pi/180)
#gammaList= [0,30]

f = open("foilData.txt","r")
for line in f:
    alphaList.append(line[1:8])
    ClList.append(line[10:17])
    CdList.append(line[20:27])
f.close()

for i in range(2,len(alphaList)):
    alphaList[i] = float(alphaList[i])
for j in range(2,len(ClList)):
    ClList[j] = float(ClList[j])
for k in range(2,len(CdList)):
    CdList[k] = float(CdList[k])

for course in gammaList:
    temp = []
    for aoa in range(2,len(alphaList)):
        
        D = 0.5 * rho * v**2 * S * CdList[aoa]    #drag
        L = 0.5 * rho * v**2 * S * ClList[aoa]    #lift
        beta = numpy.arctan(L / D)
        # print(beta)
        R = numpy.sqrt(L**2 + D**2)
        Fh = R * numpy.cos(numpy.pi - course - beta) #total force along course
        a = Fh / m
        temp.append(a)
     
    accList.append(temp)

del alphaList[:2]
del accList[0]

X = numpy.array(alphaList)
Y = numpy.array(gammaList)
X,Y = numpy.meshgrid(X,Y)
Z = numpy.array(accList)
# print("x", len(X))
# print("Y", len(Y))
# print("Z", len(Z))
# print(Z)
# X = [1, 2, 3]
# Y = [10, 11, 12]
# Z = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# Z = numpy.array(Z)
fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis)
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
#print(X)
plt.show()

#fig = plt.figure()
#ax = Axes3D(fig)
#ax.plot_surface(numpy.array(gammaList),numpy.array(alphaList), numpy.array(accList), rstride=1, cstride=1, cmap=cm.viridis)

#plt.show()

#
#
#
