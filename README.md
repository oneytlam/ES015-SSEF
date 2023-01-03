# ES999: Navigating Indoor Small-Scaled Worlds: Exploring Intersections Between RSSI and IMU for Indoor Localisation
## SSEF 2023. Goh Ying En Ian, Heng Yi Wang, Lam Yik Ting

# Directory
(Below is taken from guide.txt)  
There are 2 main folders:  
Processing - where the code is  
Inputs - datastorage.txt and processed csv file  

When running the code, either change the path yourself or make it such that there is the folder called inputs in the parent parent folder of the code.

# Functionality of Each Code File:
1. website.py
During data collection for training and testing, data is sent to a website where we host our txt file of data. This code loads the data off the main website.

2. arduino1
The Arduino code runs the ESP8266 microcontroller, connects to a WiFi sensor, prompts you to enter coordinates for data collection purposes and collects 5 iterations of data. This is then sent as a HTTP request to the website.

3. txt_to_csv1.py
Convert datastorage.txt to csv format
The uploaded code doesn’t take into account the iteration from the website (because some of them were recorded wrongly at the start), so what it does is that it just checks for coordinate and adds one for each duplicate coordinate reading
change line 30 to: noIteration = False if want to use iteration number from website

4. readData.py
Actl i'm not done with the code yet cuz i forgot to change it but i’ll do next time so can ignore the entire function on top
Currently what it does is read data from CSV file concerning the target APs that we specified (i.e. AP1, AP2)
Then it saves it into TrainData and TestData (similar to KNN_data.py in caleb’s github).
This code performs data processing on our training data. Since we took 5 iterations of data at every RP, we take the average strength of all iterations and TestData to be just the last iteration recorded when running the data into our algorithm.

5. knn.py
With reference from https://github.com/calebc2006/KNN, we implemented our KNN algorithm to predict RSSI data values.
The get_prediction function retrieves a row of data in TestData to see what the predicted coordinate is. 

6. imu.py

7. arduino2
This code provides live data from the ESP8266 sensor for quasi-real time implementation. Run this Arduino first before running quasi.py, since quasi.py simply reads off the serial data.

8. quasi.py
Obtaining quasi-real time data import from the device for testing purposes, which reads live testing data off the serial module.

9. main.py
Running the Graphical User Interface, built with Kivy, for data import and simulation of reports for testing.
