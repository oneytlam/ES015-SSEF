from pprint import pprint
import csv
from pathlib import Path

PATH = str(Path(__file__).parent.parent) + "\inputs\\rssi" 
NUM_AP = 2

mac_idx = {"E4:6F:13:45:AB:A0": 0, "E4:6F:13:45:AB:A1": 1}
    
def getTrainData(path):    
    Train_data = []
    
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)  
        header = next(reader)
        
        for i, row in enumerate(reader): 
            room, x, y, MAC, strength = int(row[0]), int(row[1]), int(row[2]), row[3], float(row[4])
            
            if i % 2 == 0:  # First mac
                data_row = [None, None, x, y, room]
                data_row[mac_idx[MAC]] = strength
            else:  # Second mac
                data_row[mac_idx[MAC]] = strength
                Train_data.append(data_row) 
                
                
    return Train_data

def getTestData(path):
    Test_data = []
    
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            data_row = list(map(float, row))
            Test_data.append(data_row)
    return Test_data
        

if __name__ == '__main__':
    train_data = getTrainData(PATH + "\\train.csv")
    pprint(train_data)
    
    test_data = getTestData(PATH + "\\testStrengths.csv")
    pprint(test_data)