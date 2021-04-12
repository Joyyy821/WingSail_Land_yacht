# File: get_c.py
# Parameter function C(gamma, vc)
# Linear model is chosen and functional expression obtained from cftool, Matlab.

def get_c(gamma, vc):
    x = abs(gamma)
    y = vc

    # data from 20-40 course angles
    p00 =      -0.119  #(-0.1599, -0.07817)
    p10 =   -0.005475  #(-0.006649, -0.004302)
    p01 =    -0.01728  #(-0.06081, 0.02624)

    f_xy = p00 + p10*x + p01*y

    return f_xy
