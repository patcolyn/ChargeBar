import sys
import win32con, win32gui
import imagesearch
import winsound

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import *


class TrackerWindow(object):

    def setupUi(self, TrackerWindow, app):
        TrackerWindow.setObjectName("MainWindow")

        # Position
        screen_resolution = app.desktop().screenGeometry()
        TrackerWindow.setGeometry((screen_resolution.width() / 2) - 250 / 2, 600, 250, 40)

        # Transparency
        TrackerWindow.setWindowOpacity(0.8)

        # Window Colour
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        TrackerWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(TrackerWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Timer
        self.counterLabel = QtWidgets.QLabel(self.centralwidget)
        self.counterLabel.setGeometry(QtCore.QRect(40, 0, 40, 40))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(13)
        font.setKerning(True)
        self.counterLabel.setFont(font)
        self.counterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.counterLabel.setObjectName("counterLabel")
        self.counterLabel.setText("0.0")

        # Text Colour
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.counterLabel.setPalette(palette)

        # Icon
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(0, 0, 40, 40))
        self.imgLabel.setScaledContents(True)
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setPixmap(QtGui.QPixmap("resources/EndIcon.png"))

        TrackerWindow.setPalette(palette)
        TrackerWindow.setCentralWidget(self.centralwidget)


class RunGUI(Thread):
    def run(self):
        print("Thread 1 running")

        # GUI setup
        app = QtWidgets.QApplication(sys.argv)
        GUI = QtWidgets.QMainWindow()
        GUI.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                           QtCore.Qt.FramelessWindowHint |
                           QtCore.Qt.WA_TransparentForMouseEvents)
        ui = TrackerWindow()
        ui.setupUi(GUI, app)
        GUI.setWindowTitle("Tracker")
        GUI.show()

        # Widget click through
        hwnd = win32gui.FindWindow(None, "Tracker")
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        lExStyle |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, lExStyle)

        # Run Widget
        sys.exit(app.exec_())


class ImageProcessor(Thread):
    def run(self):
        print("Thread 2 running")

        # Image recognition
        while True:
            imagesearch.imagesearch_region_loop("resources/End12.png", 0.5, 5, 25, 400, 140)
            # Placeholder, play sound on recognition
            winsound.PlaySound('resources/sounds/click.wav', winsound.SND_FILENAME)


if __name__ == "__main__":

    t1 = RunGUI()
    t2 = ImageProcessor()

    t1.start()
    t2.start()
