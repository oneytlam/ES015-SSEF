from pprint import pprint
import csv
from pathlib import Path

# Room 1
ROOM = 1
x_ref = [[0, 1, 2, 3, 4],
         [0, 1, 2, 3, 4],
         [0, 1, 2, 3, 4],
         [0, 1, 2, 3, 4],
         [0, 1, 2],
         [0, 1, 2, 3, 4],
         [0, 1, 2, 3, 4]]
y_ref = [[0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1],
         [2, 2, 2, 2, 2],
         [3, 3, 3, 3, 3],
         [4, 4, 4],
         [5, 5, 5, 5, 5],
         [6, 6, 6, 6, 6]]


# AP1 = "1A:27:F5:62:A3:F4"
# AP2 = "1E:EB:B6:71:6F:24"
# AP3 = "0E:EB:B6:71:6A:D7"
# APList = [AP1, AP2, AP3]

AP1 = "B4:B0:24:47:FF:8E"
APList = [AP1]

PATH = str(Path(__file__).parent.parent) + "/inputs/testing1.csv"

def getStrength(AP, x_ref, room, test=False):
    AP_data = []
    for row in x_ref:
        AP_data.append([0] * len(row))
    with open(PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            # Break when next room is reached
            if int(row[0]) == room + 1:
                break
            
            mac = row[4]
            if mac == AP:
                iteration = int(row[3])
                x, y = map(int, (row[1], row[2]))
                strength = int(row[5])
                # Need to settle average iterations issue, but some iterations are keyed wrongly (not keyed in)
                if test:
                    AP_data[y][x] = strength
                else:
                    AP_data[y][x] = round((AP_data[y][x] * (iteration - 1) + strength) / iteration, 4)
                
    return AP_data


# Get AP data from last n rows of csv 
# Assume data is stored in 3 row csv - time, AP, strength
def getLast(APList, n):
    strengths = [-1] * len(APList)  # Store time and strength, by default set to -1
    with open(PATH, "r") as csv_file:
        reader = list(csv.reader(csv_file))
        reader = reader[-n:]
        for row in reader:
            mac = row[1]
            for i, AP in enumerate(APList):
                if mac == AP:
                    strength = int(row[2])
                    # Store into AP
                    strengths[i] = strength
        
    return strengths

                    
AP1_data = getStrength(AP1, x_ref, ROOM)
# AP2_data = getStrength(AP2, x_ref, ROOM)
# AP3_data = getStrength(AP3, x_ref, ROOM)

Train_data = []
for i, row in enumerate(AP1_data):
    for j in range(len(row)):
        # x = [AP1_data[i][j], AP2_data[i][j], AP3_data[i][j], x_ref[i][j], y_ref[i][j]]
        x = [AP1_data[i][j]]
        Train_data.append(x)

print("Train Data:")
pprint(Train_data)

AP1_test = getStrength(AP1, x_ref, ROOM, test=True)
# AP2_test = getStrength(AP2, x_ref, ROOM, test=True)
# AP3_test = getStrength(AP3, x_ref, ROOM, test=True)

Test_data = []
for i, row in enumerate(AP1_test):
    for j in range(len(row)):
        # x = [AP1_test[i][j], AP2_test[i][j], AP3_test[i][j], x_ref[i][j], y_ref[i][j]]
        x = [AP1_test[i][j]]
        Test_data.append(x)

print("Test Data:")
pprint(Test_data)
    