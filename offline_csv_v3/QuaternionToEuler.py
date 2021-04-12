# Quaternion transform to Euler angle
import math

# def EulerAndQuaternionTransform( intput_data):
# 	data_len = len(intput_data)
# 	angle_is_not_rad = False
 
# 	if data_len == 3:
# 		r = 0
# 		p = 0
# 		y = 0
# 		if angle_is_not_rad: # 180 ->pi
# 			r = math.radians(intput_data[0]) 
# 			p = math.radians(intput_data[1])
# 			y = math.radians(intput_data[2])
# 		else:
# 			r = intput_data[0] 
# 			p = intput_data[1]
# 			y = intput_data[2]
 
# 		sinp = math.sin(p/2)
# 		siny = math.sin(y/2)
# 		sinr = math.sin(r/2)
 
# 		cosp = math.cos(p/2)
# 		cosy = math.cos(y/2)
# 		cosr = math.cos(r/2)
 
# 		w = cosr*cosp*cosy + sinr*sinp*siny
# 		x = sinr*cosp*cosy - cosr*sinp*siny
# 		y = cosr*sinp*cosy + sinr*cosp*siny
# 		z = cosr*cosp*siny - sinr*sinp*cosy
 
# 		return {w,x,y,z}
 
# 	elif data_len == 4:
 
# 		w = intput_data[0] 
# 		x = intput_data[1]
# 		y = intput_data[2]
# 		z = intput_data[2]
 
# 		r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
# 		p = math.asin(2 * (w * y - z * x))
# 		y = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
 
# 		if angle_is_not_rad ==False: # 180 ->pi
 
# 			r = r / math.pi * 180
# 			p = p / math.pi * 180
# 			y = y / math.pi * 180
 
# 		return {r,p,y}

def QuaternionToEuler(intput_data):
    angle_is_not_rad = False   # return angle value in radian

    w = intput_data[0] 
    y = intput_data[1]    # x
    z = intput_data[2]    # y
    x = intput_data[3]    # z

    r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    # p = math.asin(2 * (w * y - z * x))
    p = 0
    y = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))

    if angle_is_not_rad == False: # 180 ->pi

        r = r / math.pi * 180
        p = p / math.pi * 180
        y = y / math.pi * 180

    return [r,p,y]


# (-2.8077266216278076, -0.5340821743011475, 1.3219726085662842)
# quaternion = (0.17943014204502106, 0.025522729381918907, -0.198374405503273, -0.9632242918014526)
# euler = QuaternionToEuler(quaternion)
# print(euler)
