# ES015: Navigating Indoor Small-Scaled Worlds: Exploring Intersections Between RSSI and IMU for Indoor Localisation
## SSEF 2023. Goh Ying En Ian, Heng Yi Wang, Lam Yik Ting

# Directory 
There are 2 main folders:  
Processing - where the code is  
Inputs - datastorage.txt and processed csv file  

When running the code, either change the path yourself or make it such that there is the folder called inputs in the parent parent folder of the code.

# Functionality of Each Code File:
1. website.py
During data collection for training and testing, data is sent to a website where we host our txt file of data. This code loads the data off the main website.

2. arduino1
The Arduino code runs the ESP8266 microcontroller, connects to a WiFi sensor, prompts you to enter coordinates for data collection purposes and collects 5 iterations of data. This is then sent as a HTTP request to the website.

3. prepareCSV1.py
Convert txt to csv format to process data in other files. (generates 1 csv for training and testing each)

4. prepareData.py
Processes both training and testing csv file and converts it to a python list that can be used in other files.

5. imu.py
Runs dead reckoning and ZUPT algorithms on IMU data.

6. knn_imu.py
With reference from https://github.com/calebc2006/KNN, we implemented our KNN algorithm to predict RSSI data values. Furthermore, to combine IMU, it runs another KNN algorithm on filtered K_KNN number of RPs.
The get_prediction function retrieves a row of data in TestData to see what the predicted coordinate is. 

7. arduino2
This code provides live data from the ESP8266 sensor for quasi-real time implementation. Run this Arduino first before running quasi.py, since quasi.py simply reads off the serial data.

8. quasi.py
Obtaining quasi-real time data import from the device for testing purposes, which reads live testing data off the serial module.

9. main.py
Running the Graphical User Interface, built with Kivy, for data import and simulation of reports for testing.
