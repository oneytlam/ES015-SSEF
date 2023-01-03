import time
import math
import csv
from pandas import *
THRESHOLD = 0.06

def check(val, threshold):
    if abs(val) < threshold:
        return 0
    return val

def imuChange(path, startTime, endTime, velocityX=0, velocityY=0, angleX=0, angleY=0, angleZ=0):
    timeStamp = []
    accelDataX = []
    accelDataY = []
    accelDataZ = []
    gyroDataX = []
    gyroDataY = []
    gyroDataZ = []
    accX = 0
    accY = 0
    x_coordinate = 7
    y_coordinate = 0

    # open the file in read mode
    file = open(path, 'r')
    # creating dictreader object
    file = csv.DictReader(file)
    for col in file:
        firstTime = float(col["timestamp"])
        break

    for col in file:
        curTime = float(col["timestamp"]) - firstTime
        if not (startTime <= curTime <= endTime):
            continue
        timeStamp.append(curTime)
        if col['lacc'] != None and col['lacc'] == '82':
            accelX = float(col['laccX']) if col['laccX'] != None else 0
            accelDataX.append(check(accelX, THRESHOLD))
            
            accelY = float(col['laccY']) if col['laccY'] != None else 0
            accelDataY.append(check(accelY, THRESHOLD))
            
            accelZ = float(col['laccZ']) if col['laccZ'] != None else 0
            accelDataZ.append(check(accelZ, THRESHOLD))
        else:
            accelDataX.append(check(0, THRESHOLD))
            accelDataY.append(check(0, THRESHOLD))
            accelDataZ.append(check(0, THRESHOLD))
            
        
        if col['gyro'] != None and col['gyro'] == '4':
            gyroDataX.append(float(col['gyroX']) if col['gyroX'] != None else 0)
            gyroDataY.append(float(col['gyroY']) if col['gyroY'] != None else 0)
            gyroDataZ.append(float(col['gyroZ']) if col['gyroZ'] != None else 0)
        else:
            gyroDataX.append(0)
            gyroDataY.append(0)
            gyroDataZ.append(0)
            
            

    prevTime = math.floor(float(timeStamp[0]))
    curTime = 0

    interval = 10.0
    start_t = 0
    for i in range(len(accelDataX)):
        curTime = float(timeStamp[i])
        """angleX += gyroDataX[i] * (curTime - prevTime)
        angleX %= (2*math.pi) 
        angleY += gyroDataY[i] * (curTime - prevTime)
        angleY %= (2*math.pi)
        accX = accelDataX[i] * math.cos(angleX) + accelDataX[i] * math.sin(angleY)
        accY = accelDataY[i] * math.sin(angleX) + accelDataY[i] * math.cos(angleY)"""
        angleZ += gyroDataZ[i] * (curTime - prevTime)
        angleZ %= (2 * math.pi)
        accX = accelDataX[i] * math.cos(angleZ) - accelDataY[i] * math.sin(angleZ)
        accY = accelDataX[i] * math.sin(angleZ) + accelDataY[i] * math.cos(angleZ)
        #assume uniform acceleration
        velocityX = check(velocityX, THRESHOLD)
        velocityY = check(velocityY, THRESHOLD)
        x_coordinate += velocityX * (curTime - prevTime) + 0.5 * accX * ((curTime - prevTime) ** 2)
        y_coordinate += velocityY * (curTime - prevTime) + 0.5 * accY * ((curTime - prevTime) ** 2)
        velocityX += accX * (curTime - prevTime)
        velocityY += accY * (curTime - prevTime)
        # print(curTime, accX, accY, velocityX, velocityY)
        prevTime = curTime
        # print(angleX - 2*math.pi, angleY)
        if round(curTime, 1) == start_t:
            print(f"time: {curTime}, x: {x_coordinate}, y: {y_coordinate}")
            start_t += interval

    return x_coordinate, y_coordinate, velocityX, velocityY, angleX, angleY
    

if __name__ == '__main__':
    print(imuChange('C:/Users/gohyi/OneDrive/Documents/GitHub/yiy_astarIHPC/inputs/imu/2jan_U6.csv', 0, 300))