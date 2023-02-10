#################################################

#------------------IMPORTS----------------------#
#-----sys-----#
import sys

#-----PyQt5-----#
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QSize, QPoint
from PyQt5.QtGui import QIcon, QPixmap

#-----Other-----#
from configparser import ConfigParser
import requests

#-----Timezone-----#
from datetime import datetime
from datetime import *
from pytz import timezone
from timezonefinder import TimezoneFinder
#------------------------------------------------

#################################################

#------------------------------------------------
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']
#------------------------------------------------

#################################################

#---------------FULL-PROGRAM--------------------#

class mainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('app_PyQt_v1.ui', self)

#-------Makes window frameless-------#
        self.setWindowTitle('Weather App')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#-------Introduce all UI elements----#

#-------mainFrame---------#
        self.mainFrm = self.mainFrame
        # Does this even do anything?↓
        # self.mainFrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrm.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)

#-------mainFrame->bgLbl--#
        self.bgLbl = QLabel(self)
        # self.movie = QMovie('images/more_weather_icons/bg_portrait.gif')
        # self.bgLbl.setMovie(self.movie)
        # self.movie.setScaledSize(QSize(242, 449))
        # # self.movie.start()
        # self.bgLbl.setGeometry(0, 0, 242, 449)
        # self.bgLbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.bgLbl.setPixmap(QPixmap('images/more_weather_icons/bg_.png'))
        # self.bgLbl.setScaledContents(True)
        # self.bgLbl.setStyleSheet("""
        #     QLabel {
        #         background-color: transparent;
        #         border-radius: 15px;
        #     }
        # """)

#-------#TODO: fix the UI(make it better)-------------#
#-----------→#TODO: add radius to bg pic, add the..
#-----------..rest of the elements, add blur(?), etc.-

        self.mainLbl = QLabel(self)
        self.mainLbl.setGeometry(10, 20, 220, 420)
        self.mainLbl.setAlignment(QtCore.Qt.AlignCenter)
        
        #  # creating a blur effect
        # self.blur_effect = QGraphicsBlurEffect()
        # # adding blur effect to the label
        # self.mainLbl.setGraphicsEffect(self.blur_effect)
        self.mainLbl.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 60);
                border-radius: 15px;
            }
        """)

#-------mainFrame->closebtn--#
        self.closeBtn = QPushButton(self)
        self.closeBtn.setIcon(QIcon('images/test-removebg.png'))
        self.closeBtn.setIconSize(QtCore.QSize(20, 20))
        self.closeBtn.setGeometry(195, -5, 50, 30)
        self.closeBtn.clicked.connect(sys.exit)
        self.closeBtn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
        """)
        
#-------mainFrame->activate_search_button--#
        self.activate_search_button = QPushButton(self)
        self.activate_search_button.setIcon(QIcon('images/up_arrow.png'))
        self.activate_search_button.setGeometry(90, 10, 60, 60)
        self.activate_search_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
        """)
        

        self.cityText = str()
        self.cityEntry = QLineEdit(self, text=self.cityText)
        self.cityEntry.setPlaceholderText("Enter city name")
        self.cityEntry.setGeometry(10, 15, 160, 30)
        self.cityEntry.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 60);
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                padding-left: 5px;
                padding-right: 5px;
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 14px;
            }
            Active {
                background-color: red;
            }
        """)

        self.searchBtn = QPushButton(self)
        self.searchBtn.setIcon(QIcon('images/search-white-removebg.png'))
        self.searchBtn.setIconSize(QtCore.QSize(20, 20))
        self.searchBtn.setGeometry(170, 15, 24, 30)
        self.searchBtn.clicked.connect(self.search)
        # self.searchBtn.setStyleSheet("background-color: rgba(255, 255, 255, 60); border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding-right: 5px;")
        self.searchBtn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 60);
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                padding-right: 5px;
                padding-left: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 80);
            }
        """)
 
        self.locationLbl = QLabel(self, text='')
        self.locationLbl.setGeometry(26, 45, 200, 30)
        self.locationLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 17px;
            }
        """)

        self.tempLbl = QLabel(self, text='')
        self.tempLbl.setGeometry(10, 80, 200, 50)
        self.tempLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 50px;
            }
        """)

        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setScaledContents(True)
        self.image.setGeometry(80, 150, 120, 120)

        self.weatherLbl = QLabel(self, text='')
        self.weatherLbl.setGeometry(10, 340, 200, 30)
        self.weatherLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 17px;
            }
        """)

        self.feelsLikeLbl = QLabel(self, text='')
        self.feelsLikeLbl.setGeometry(10, 370, 200, 30)
        self.feelsLikeLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 17px;
            }
        """)

        self.windLbl = QLabel(self, text='')
        self.windLbl.setGeometry(10, 400, 200, 30)
        self.windLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 17px;
            }
        """)

        self.dragBarLbl = QLabel(self)
        self.dragBarLbl.setMaximumSize(QSize(200, 15))
        self.dragBarLbl.setMinimumSize(QSize(200, 15))
        self.dragBarLbl.setStyleSheet("""
            QLabel {
                background-color: transparent;
            }
        """)

        self.locationIcon = QLabel(self)

        self.drag_start_pos = None

        self.timeLbl = QLabel(self, text='')
        self.timeLbl.setGeometry(10, 220, 200, 30)
        self.timeLbl.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Yu Gothic UI Light;
                font-size: 17px;
            }
        """)

        # self.time.strftime('%H:%M')

#--------------------------------------------

#################################################

#-----------METHODS-----------#

#------This fetches data from the API------#

    def get_weather(self, city):
        result = requests.get(url.format(city, api_key))
        # print(url.format(city, api_key))
        
        if result:
            json = result.json()
        #(City, country, temp_celsius, feels_like, icon, weather, longitude, latitude)
            city = json['name']
            country = json['sys']['country']
            temp_kelvin = json['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            feels_like = json['main']['feels_like'] - 273.15
            wind = json['wind']['speed']
            icon = json['weather'][0]['icon']
            weather = json['weather'][0]['description']
            longitude = json['coord']['lon']
            latitude = json['coord']['lat']

            final = (city, country, temp_celsius, feels_like, wind, icon, weather, longitude, latitude)
            return final
        else:
            print("Error while getting weather data")
            return None
#------------------------------------------------

#################################################

#------Once city has been entered, it takes all data from ↑ and...
#------...distributes it to the UI elements------#

#------#TODO: ↓ ADD IF STATEMENT TO SEE IF FEELS-LIKE IS...
#-------THE SAME AS TEMP, IF YES, THEN DONT SHOW?------#

    def search(self):
        city = self.cityEntry.text()
        weather = self.get_weather(city)
  
        if weather:
            self.locationIcon.setPixmap(QPixmap('images/location_v2_16x.png'))
            self.locationIcon.setGeometry(10, 53, 16, 16)
            self.locationIcon.setScaledContents(True)
            self.locationIcon.setAlignment(QtCore.Qt.AlignCenter)
            self.locationIcon.setStyleSheet("background-color: transparent;")

            self.locationLbl.setText('{}, {}'.format(weather[0], weather[1]))
            
            pixmap = QPixmap('images/more_weather_icons/{}.png'.format(weather[5]))  
            self.image.setPixmap(pixmap)

            self.tempLbl.setText('{:.0f}°'.format(weather[2]))
            
            self.feelsLikeLbl.setText('{:.0f}°'.format(weather[3]))
            
            self.windLbl.setText('{:.0f}km/h'.format(weather[4]))

            self.weatherLbl.setText(weather[6])

            self.time = TimezoneFinder().timezone_at(lng=weather[7], lat=weather[8])
            self.timeLbl.setText(self.time)
            # print(self.time)
            self.timezone = timezone(self.time)
            self.time = datetime.now(self.timezone)
            self.timeLbl.setText(self.time.strftime('%H:%M'))
            # print(self.time.strftime('%H:%M'))

            QtCore.QTimer.singleShot(3000, self.search)
        else:
            QMessageBox.critical(self, 'Error', "Cannot find city {}".format(city))
    
#------------------------------------------------

#################################################

#------This should eventually cause the app...
#------to auto show Raisio when started------#
#------------#TODO: MAKE APP AUTO SHOW RAISIO WHEN STARTED---#
    def autoShowRaisio(self):
        pass
#------------------------------------------------

#################################################

#------These two make the window draggable------#
#-------------#TODO: EXPLAIN HOW THEY WORK-------------#
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         try:
    #             # Check if the mouse press position is within the label's boundaries
    #             if self.dragBarLbl.geometry().contains(event.pos()):
    #                 self.press_pos = event.globalPos()
    #                 self.move_pos = QPoint(0, 0)
    #         except Exception as error:
    #             return None

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         try:
    #             if self.dragBarLbl.geometry().contains(event.pos()):
    #                 self.move_pos = event.globalPos() - self.press_pos
    #                 self.move(self.pos() + self.move_pos)
    #                 self.press_pos = event.globalPos()
    #         except Exception as error:
    #             return None
#------------------------------------------------
    # These, instead of ↑those, make the window draggable from anywhere
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
#################################################

#------This makes the window open on the right side of the screen------#
   
    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width() - 50
        y = 2 * ag.height() - sg.height() - widget.height() + 18
        self.move(x, y)

#------------------------------------------------

#################################################

#------Start app------#
if __name__ == "__main__":
    # Create an application object
    app = QApplication(sys.argv)

    #app.setStyle('Fusion')

    # Create the Main Window object from FormWithTable Class and show it on the screen
    appWindow = mainWindow()
    appWindow.location_on_the_screen()
    appWindow.show()
    sys.exit(app.exec_())
        