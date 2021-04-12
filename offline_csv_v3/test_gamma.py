# Theoretical acc value (with parameter ID) under different gamma and vc

from get_const2 import acc_theory
from calculate_V0 import get_c

from matplotlib import pyplot as plt


# print(acc_theory(1, 2.6, 0))
gammaList = list(range(-30, 80))
vc1 = 0.2
vc2 = 0.6
vc3 = 1.0
vc4 = 1.4

vt = 2.6

acc_lst1 = []
acc_lst2 = []
acc_lst3 = []
acc_lst4 = []

for gamma in gammaList:
    a1 = acc_theory(vc1, vt, gamma)
    a2 = acc_theory(vc2, vt, gamma)
    a3 = acc_theory(vc3, vt, gamma)
    a4 = acc_theory(vc4, vt, gamma)

    c1 = get_c(gamma, vc1)
    c2 = get_c(gamma, vc2)
    c3 = get_c(gamma, vc3)
    c4 = get_c(gamma, vc4)

    # c1, c2, c3, c4 = 0, 0, 0, 0

    acc_lst1.append(a1 + c1)
    acc_lst2.append(a2 + c2)
    acc_lst3.append(a3 + c3)
    acc_lst4.append(a4 + c4)

plt.plot(gammaList, acc_lst1, label="vc = 0.2")
plt.plot(gammaList, acc_lst2, label="vc = 0.6")
plt.plot(gammaList, acc_lst3, label="vc = 1.0")
plt.plot(gammaList, acc_lst4, label="vc = 1.4")

plt.xlabel("gamma")
plt.ylabel("acc")
plt.legend()
# plt.scatter(gammaList, acc_lst1)
plt.show()
