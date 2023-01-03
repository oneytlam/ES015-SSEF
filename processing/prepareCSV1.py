import csv
from pathlib import Path
from datetime import datetime

def getMacStrength(s):
    _, s = s.split("[")
    mac, strength = s.split("]")
    return mac, int(strength[:-1])

def timeDiff(start_time, end_time):
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    return int(delta.total_seconds())

def getTrainCSV():
    # Get path of inputs folder
    path = str(Path(__file__).parent.parent) + "\inputs\\rssi"

    # Get rooms
    rooms = {}  # id: [name, min, max]
    with open(path + "\\rooms1.csv", "r") as room_file:
        reader = csv.reader(room_file)
        header = next(reader)
        for row in reader:
            roomID, name, minX, maxX, minY, maxY = [(row[i] if i == 1 else int(row[i])) for i in range(len(row))]
            rooms[roomID] = [name, minX, maxX, minY, maxY]
        # print(rooms)
    
    headers = ["room", "x", "y", "MAC", "strength"]
    data = []
    with open(path + "\\yiy5-0.txt", "r") as txt_file:
        txt_file = txt_file.readlines()
        for i in range(0, len(txt_file), 5):
            row = txt_file[i].split(" ")
            data_row = [1] * 3
            mac_data = {"E4:6F:13:45:AB:A0": 0, "E4:6F:13:45:AB:A1": 0}
            x, y = map(int, [row[-2].split(",")[0][1:], row[-2].split(",")[1][:-1]])
            data_row[1], data_row[2] = x, y
            for j in range(5):
                row = txt_file[i+j].split(" ")
                mac1, strength1 = getMacStrength(row[-4])
                mac_data[mac1] += strength1 / 5
                mac2, strength2 = getMacStrength(row[-5])
                mac_data[mac2] += strength2 / 5
            data.append(data_row + [mac1, round(mac_data[mac1], 1)])
            data.append(data_row + [mac2, round(mac_data[mac2], 1)])
    
    # For reference: headers = ["room", "x", "y", "MAC", "strength"]
    with open(path + "\\train.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
            
    return rooms                

def getTestCSV():
    path = str(Path(__file__).parent.parent) + "\inputs\\rssi"
    start = True
    headers = ["E4:6F:13:45:AB:A0", "E4:6F:13:45:AB:A1", "Action", "Time"]
    action = 0
    data = []
    with open(path + "\\yiy7.txt", "r") as txt_file:
        for row in txt_file:
            row = row.strip()
            row = row.strip("\n")
            row = row.split(" ")
            if row[0] == '':
                pass
            else:
                if start:
                    start_time = row[2][:-2]
                    start = False
                cur_time = timeDiff(start_time, row[2][:-2])
                mac1, strength1 = getMacStrength(row[-1])
                mac2, strength2 = getMacStrength(row[-2])
                data_row = [None, None, action, cur_time]
                data_row[headers.index(mac1)] = strength1
                data_row[headers.index(mac2)] = strength2
                data.append(data_row)
                     
            
            # elif row[0][0] == "^":
            #     action += 1
            #     start = True
    
    with open(path + "\\testStrengths.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
            
if __name__ == '__main__':
    getTrainCSV()
    getTestCSV()