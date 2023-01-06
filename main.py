from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from processing.prepareData import getTestData
from processing.knn_imu import get_prediction
from processing.createWalls import WALLS, Point, RIGHT_X_metres, BOTTOM_Y_metres, ORIGIN_X, ORIGIN_Y, dx, dy
from processing.rulechecking import validCoords
from processing.imu import imuChange
import time
import csv
import cv2

# PATH = r'./images/original.png'
PATH = r'./images/yt house.png'
PATHA = r'./images/1start.png'
PATHB = r'./images/2inputrssi.png'
PATHC = r'./images/3inputrssi.png'
PATHD = r'./images/4kvalue.png'
PATHE = r'./images/5kvalue.png'
IMU_PATH = r'./inputs/imu/2jan_U6.csv'
ACTION = 0

RADIUS = 20
RED = (0, 0, 255)
PINK = (100, 100, 255)
WHITE = (255, 255, 255)

THICKNESS = -1 
original_img = cv2.imread(PATH)
height, width, _ = original_img.shape
# coords = [200, 100]

with open("coordinates.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Time", "X", "Y"])

def draw(coords, prevCoords):
    new_img = original_img.copy()
    x1, y1 = coords
    center_coordinates1 = tuple(map(int, [ORIGIN_X + dx * (x1 / RIGHT_X_metres * width), ORIGIN_Y + dy * (y1 / BOTTOM_Y_metres * height)]))
    new_img = cv2.circle(new_img, center_coordinates1, RADIUS, RED, THICKNESS)  # Draw new points
    if prevCoords != None and coords != prevCoords:
        x2, y2 = prevCoords
        center_coordinates2 = tuple(map(int, [ORIGIN_X + dx * (x2 / RIGHT_X_metres * width), ORIGIN_Y + dy * (y2 / BOTTOM_Y_metres * height)]))
        
        new_img = cv2.circle(new_img, center_coordinates2, int(RADIUS / 1.5), PINK, THICKNESS)
        new_img = cv2.arrowedLine(new_img, center_coordinates2, center_coordinates1, WHITE, 2)
    cv2.imwrite(r'./images/new.png', new_img)
    return

sm = ScreenManager()
strengths = []

index = 0
velocityX, velocityY, angleX, angleY = 0, 0, 0, 0

prevCoords = [3, 0]
file_path = ""

class WelcomeScreen(Screen):
    def build_app(self):
        return FloatLayout()
    pass

class ChooseFile(Screen):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

class FileChoose(ChooseFile):
    def load(self, selection):
        global file_path, strengths
        file_path = str(selection[0])
        self.the_popup.dismiss()
        strengths = getTestData(file_path)

class FileConfirm(Screen):
    def build_app(self):
        global file_path
        print(file_path)
        # check for non-empty list i.e. file selected
        if file_path:
            self.ids.inputCSV.text = file_path

# class AdditionalInput(Screen):
#     def saveValues(self):
#         global k
#         k = int(self.ids.value_k.text)


class Display(Screen):
    pass

class OutputScreen(Screen):
    coordinates = StringProperty('No coordinates yet...')
    def update_coords(self):
        global coords, index, prevCoords
        global velocityX, velocityY, angleX, angleY
        
        endTime = strengths[index][2]
        
        
        if index > 0 and endTime != 0:
            startTime = strengths[index-1][2]
        else:
            startTime = 0
        # print(startTime, endTime)    
        if endTime == 0:
            imuX, imuY, velocityX, velocityY, angleX, angleY = 0, 0, 0, 0, 0, 0
        else:
            # print(velocityX, velocityY, angleX, angleY)
            imuX, imuY, velocityX, velocityY, angleX, angleY = imuChange(IMU_PATH, startTime, endTime, velocityX, velocityY, angleX, angleY)
        coords = [coords[0] + 20, coords[1] + 20]

        coords = get_prediction(strengths[index], [imuX*0.4, imuY*0.4], prevCoords)
        print(coords)
        coords = validCoords(Point(coords[0], coords[1]), Point(prevCoords[0], prevCoords[1]), WALLS, endTime - startTime)
        coords = [round(x, 2) for x in coords]
        with open("coordinates.csv", 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([endTime] + coords)
        draw(coords, prevCoords)
        coords_str = f"Current coordinates: ({coords[0]}, {coords[1]})"
        self.coords.text = coords_str
        self.ids.visual_output.source = 'images/new.png'
        self.ids.visual_output.reload()
        index += 1
        prevCoords = coords
        time.sleep(endTime - startTime)
        # time.sleep(1)
    
    def load(self):
        Clock.schedule_interval(lambda dt: self.update_coords(), 0.001)
        

class FileChoosePopup(Popup):
    load = ObjectProperty(None)

kv = Builder.load_file("main.kv")

class GUI(App):
    def build(self):
        return kv

if __name__ == '__main__':
    GUI().run()

