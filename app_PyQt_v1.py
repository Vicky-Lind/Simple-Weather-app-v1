import sys
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
from datetime import date
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QMovie, QIcon
from configparser import ConfigParser
import requests

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

class mainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('app_PyQt_v1.ui', self)

        self.setWindowTitle('Weather App')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.mainFrm = self.mainFrame
        # Does this even do anything?↓
        #self.mainFrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrm.setStyleSheet("background-image: url('./weather_icons/weather_test.png');")

        self.closeBtn = QPushButton(self)
        self.closeBtn.setIcon(QIcon('test-removebg.png'))
        self.closeBtn.setIconSize(QtCore.QSize(20, 20))
        self.closeBtn.setStyleSheet("background-color: transparent;")
        self.closeBtn.setGeometry(195, -5, 50, 30)
        self.closeBtn.clicked.connect(sys.exit)


    def get_weather(self, city):
        result = requests.get(url.format(city, api_key))
        if result:
            json = result.json()
            # (City, country, temp_celsius, icon, weather)
            city = json['name']
            country = json['sys']['country']
            temp_kelvin = json['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            feels_like = json['main']['feels_like'] - 273.15
            wind = json['wind']['speed']
            icon = json['weather'][0]['icon']
            weather = json['weather'][0]['main']
            final = (city, country, temp_celsius, feels_like, wind, icon, weather)
            return final
        else:
            print("Error while getting weather data")
            return None
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width() - 50
        y = 2 * ag.height() - sg.height() - widget.height() + 18
        self.move(x, y)

if __name__ == "__main__":
    # Create an application object
    app = QApplication(sys.argv)

    #app.setStyle('Fusion')

    # Create the Main Window object from FormWithTable Class and show it on the screen
    appWindow = mainWindow()
    appWindow.location_on_the_screen()
    appWindow.show()  # This can also be included in the FormWithTable class
    sys.exit(app.exec_())
        