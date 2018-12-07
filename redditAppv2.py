import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread
import os as os
import urllib as urllib
import praw as praw
import shutil as shutil

application = QApplication(sys.argv)

screen = application.primaryScreen()

class reddit():
    reddit_bot = praw.Reddit(user_agent = 'katznbot', client_id = '_CIuAjxI8TaKvg', client_secret = 'HnpYVUD2jouM--6OdFzdFNJ_g2E', username = 'katznbot', password = '') #this can be public, its just a reddit bot.
    subreddit = 'all'

class app():
    applicationRunning = True
    loadedImageURLs = []
    previousLoadCounts = {}
    windowState = 'min'

if ('tmp' not in os.listdir('.')):
    os.mkdir('tmp')

for file in os.listdir('./tmp'):
    os.remove('./tmp/' + file)

def event(e):
    e = str(e)
    if (e == 'exit'):
        app.applicationRunning = False
        exit()
    elif (e == 'minimizeWindow'):
        window.showMinimized()
    elif (e == 'toggleWindowSizeState'):
        if (app.windowState == 'min'):
            window.showMaximized()
            app.windowState = 'max'
        else:
            window.showNormal()
            app.windowState = 'min'
    elif (e.split('\u2588')[0] == 'setWindowTitle'):
        windowTitle.setText(e.split('\u2588')[1])

class headerMonitoring():
    offset = None
    def windowDrag(e):
        headerMonitoring.offset = e.pos()
    def windowMove(e):
        x = e.globalX()
        y = e.globalY()
        x_w = headerMonitoring.offset.x()
        y_w = headerMonitoring.offset.y()
        window.move((x - x_w), (y - y_w))

def getImage(url):
    url = str(url)
    imagefilename = str(url).split('/')[(url.count('/'))]
    imagefilename = imagefilename.split(':')[(imagefilename.count(':'))]
    fp = './tmp/' + imagefilename
    imageContents = urllib.request.urlopen(url)
    image = open(('./tmp/' + imagefilename), 'wb')
    image.write(imageContents.read())
    image.close()
    return fp

print (getImage('http://www.katznboyz.com/images/favicon.ico'))

window = QWidget()
window.setWindowTitle('Reddit App V2')
window.setStyleSheet('QWidget{background-color:#2b2b2b;}')
window.setWindowIcon(PyQt5.QtGui.QIcon('paint_application_icon.png'))
window.resize((screen.size().width() / 2), (screen.size().height() / 2))
window.setWindowFlags(PyQt5.QtCore.Qt.CustomizeWindowHint) 

windowTopBorder = QWidget(window)
windowTopBorder.resize(window.width(), 20)
windowTopBorder.move(0, 0)
windowTopBorder.setStyleSheet('QWidget{background-color:black;}')
windowTopBorder.mousePressEvent = lambda e: headerMonitoring.windowDrag(e)
windowTopBorder.mouseMoveEvent = lambda e: headerMonitoring.windowMove(e)

windowTitle = QLabel(window)
windowTitle.move(10, 0)
windowTitle.setFixedHeight(20)
windowTitle.setStyleSheet('QLabel{color:white;font-family:Calibri;background-color:transparent;}')

exitButton = QPushButton(window)
exitButton.move((window.width() - exitButton.width()), 0)
exitButton.setText('X')
exitButton.resize(40, 20)
exitButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:red;color:white;font-family:Courier;}
''')
exitButton.clicked.connect(lambda: event('exit'))

toggleWindowStateButton = QPushButton(window)
toggleWindowStateButton.move((exitButton.x() - exitButton.width()), 0)
toggleWindowStateButton.setText('[]')
toggleWindowStateButton.resize(40, 20)
toggleWindowStateButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:#6b6a6a;color:white;font-family:Courier;}
''')
toggleWindowStateButton.clicked.connect(lambda: event('toggleWindowSizeState'))

minimizeButton = QPushButton(window)
minimizeButton.move((toggleWindowStateButton.x() - toggleWindowStateButton.width()), 0)
minimizeButton.setText('-')
minimizeButton.resize(40, 20)
minimizeButton.setStyleSheet('''
QPushButton{background-color:transparent;color:white;font-family:Courier;}
QPushButton:hover{background-color:#6b6a6a;color:white;font-family:Courier;}
''')
minimizeButton.clicked.connect(lambda: event('minimizeWindow'))

contentFeedArea = QWidget(window)
contentFeedArea.move(0, windowTopBorder.height())
contentFeedArea.resize(500, (window.height() - windowTopBorder.height()))
contentFeedArea.setStyleSheet('QWidget{background-color:transparent;border-right:2px solid black;}')
#contentFeedArea.setLayout(layout)

def resizeThread():
    while (app.applicationRunning):
        exitButton.move((window.width() - exitButton.width()), 0)
        toggleWindowStateButton.move((exitButton.x() - exitButton.width()), 0)
        minimizeButton.move((toggleWindowStateButton.x() - toggleWindowStateButton.width()), 0)
        windowTopBorder.resize(window.width(), 20)
        contentFeedArea.resize(500, (window.height() - windowTopBorder.height()))

event('setWindowTitle\u2588Reddit App V2')

window.setMinimumSize(contentFeedArea.width(), 300)

thread.start_new_thread(resizeThread, ())

window.show()

application.exec_()

applicationRunning = False

for file in os.listdir('./tmp'):
    os.remove('./tmp/' + file)
