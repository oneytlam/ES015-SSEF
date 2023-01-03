# Reference: https://github.com/calebc2006/KNN/blob/master/KNN.py
# list of lists of [AP1, AP2, x, y]
from .prepareData import getTrainData, getTestData
import math
# import matplotlib.pyplot as plt
from statistics import stdev
from pathlib import Path
NUM_AP = 2
ORDER = 2

PATH = str(Path(__file__).parent.parent) + "\inputs\\rssi"
Train_data, Test_data = getTrainData(PATH + "\\train.csv"), getTestData(PATH + "\\testStrengths.csv")
K_KNN = 9
K_IMU = 9

# CSV_PATH = str(Path(__file__).parent.parent) + "/inputs/testing1.csv"
def euclidean_distance(p1, p2, n=NUM_AP):
    distance = 0.0
    for i in range(n):
        distance += (p1[i] - p2[i])**2
    return math.sqrt(distance)

# Get rssi neighbors
def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

# get imu neighbors
def get_neighbors1(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row[NUM_AP:])
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

# Algo mentioned in research paper
def get_prediction(test_rssi, imu_disp, prevCoords, k_KNN=K_KNN, k_IMU=K_IMU):
    neighbors = get_neighbors(Train_data, test_rssi, k_KNN)
    test_imu = [a + b for a, b in zip(imu_disp, prevCoords)]
    neighbors = get_neighbors1(neighbors, test_imu, k_IMU)
    print(test_rssi)
    print(neighbors)
    x_pred = 0
    y_pred = 0
    total = 0
    inverse_dev = []

    # Should use weights from rssi or imu dist? (Currently uses rssi) 
    for i in range(k_IMU):
        dist = euclidean_distance(test_rssi, neighbors[i][0:NUM_AP])
        if dist == 0:
            inverse_dev.append(1e9)
        else:
            inverse_dev.append(float(1/dist**ORDER))
        total += inverse_dev[i]
    for i in range(k_IMU):
        inverse_dev[i] /= total
        # print(neighbors[i][NUM_AP] * inverse_dev[i], neighbors[i][NUM_AP+1] * inverse_dev[i])
        x_pred += neighbors[i][NUM_AP] * inverse_dev[i]
        y_pred += neighbors[i][NUM_AP+1] * inverse_dev[i]
    print(x_pred, y_pred)
    return [x_pred, y_pred]

def tangent(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)

def check_limit(maxX, maxY, coord):
    if coord[0]<0:
        coord[0]=0
    if coord[1]<0:
        coord[1]=0
    if coord[0]>maxX:
        coord[0]=maxX
    if coord[1]>maxY:
        coord[1]=maxY
    # github copilot is now smart!
    return coord


    
