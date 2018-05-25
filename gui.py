from PyQt5.QtWidgets import *
#QApplication, QWidget, QMainWindow, QLabel, QMouseEventTransition, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QMouseEvent
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, QPoint, QRect

import sys

from FileExplorer import GuiFileExplorer
from File import File
from Folder import Folder

class App(QMainWindow, QObject):
    def __init__(self):
        super().__init__()

        #self.setWindowOpacity(0.5) #opacity



        self.title = "PyQt5 test"
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 768
        self.mouseX = 0
        self.mouseY = 0
        self.mousePos = QPoint(0,0)
        self.qpoint = None


        self.k = 50  # coefficient  eg. length of line, width of icon
        self.namemaxlength = 10  #shorten the long name
        self.folderWidth = 50
        self.folderHeight = 50
        self.fileWidth = 50
        self.fileHeight = 50
        self.detailInfoWidth = 100
        self.detailInfoHeight = 100

        #about FileExplorer
        self.Fe = GuiFileExplorer()
        self.Fe.folderX, self.Fe.folderY = 50, self.height / 2
        self.Fe.setFolder("/Users/huweilun/files/test")
        self.Fe.setFolder("/Users/huweilun/files/2018出国学习")

        #print(len(self.Fe.mainfolder.bfs()))
        #print(self.Fe.getLeavesNumber(self.Fe.mainfolder))




        self.Fe.setAllFoldersContentsCoordinate()
        #######################

        self.searchqle = QLineEdit()
        self.w = QWidget()  # empty widget   to place the search box on the top
        self.keyword = None #save the keyword in searchqle
        self.initUI()


    def initUI(self):
        self.text = "this is a text"

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('status bar')



        self.searchqle.displayText()
        self.searchqle.textChanged.connect(self.searchQleChanged)
        #self.w = QWidget() #empty widget   to place the search box on the top

        grid = QGridLayout()
        grid.addWidget(self.searchqle, 0, 0)
        grid.addWidget(self.w,1,0)


        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)



        self.show()





    def paintEvent(self, event):
        self.qp = QPainter()
        self.qp.begin(self)
        #self.drawText(event, self.qp)
        #self.drawRectangles(self.qp, 200, 30)



        ###test paint###

        #print([str(i) for i in self.Fe.mainfolder.folderSet])

        #draw files and folders
        for f in self.Fe.mainfolder.folderSet:
            self.drawFolder(f)
            if self.mouseInObject(f):
                self.drawDetailInfo(f)

        for f in self.Fe.mainfolder.fileSet:
            self.drawFile(f)
            if self.mouseInObject(f):
                self.drawDetailInfo(f)

        for l in self.Fe.linesSet:
            x1, y1, x2, y2 = l
            self.drawLines(self.qp, x1, y1, x2, y2)
        ######




        #p = self.w.mapToParent(self.mousePos)
        #self.qp.drawText(p,"mousew"+str((p))) #trace the mouse

        self.qp.end()


        return


    def searchQleChanged(self):
        print(self.searchqle.displayText())
        self.keyword = self.searchqle.displayText()
        #self.repaint()
        self.update()

    def mouseInObject(self, f): #to judge whether the mouse in a file or a folder
        '''
        if type(f) == File:
            if (f.x<=self.mouseX<=(f.x+self.fileWidth)) and (f.y<=self.mouseY<=(f.y+self.fileHeight)):
                return True
        if type(f) == Folder:
            if (f.x <= self.mouseX <= (f.x+self.folderWidth)) and (f.y <= self.mouseY <= (f.y+self.folderHeight)):
                return True
        '''
        p = self.w.mapToParent(self.mousePos)
        x, y = p.x(), p.y()
        if f.x<x and x<(f.x+50) and f.y<y and y<(f.y+50):
            return True
        return False


    #draw functions start#################
    def drawDetailInfo(self, f):
        self.qp.setPen(QColor(176,196,222))
        p = self.w.mapToParent(self.mousePos)  # transform coordinate of widget 's' to that of the qmainwindow

        rc = QRect(p.x(),p.y(), 400,300)
        self.qp.drawText(rc,Qt.TextWrapAnywhere, str(f.getDetailInfo()))
        print(f.getDetailInfo())


    def drawFile(self, f):
        self.drawRectangle(f.x, f.y)
        self.drawNames(f.x, f.y, f.filename+str((f.x,f.y)), self.keyword)


    def drawFolder(self, f):
        self.drawRectangle(f.x, f.y)
        self.drawNames(f.x, f.y, f.foldername+str((f.x,f.y)), self.keyword)

    def drawNames(self, x, y, name, keyword=None):
        if keyword:
            p = name.partition(keyword)
            self.qp.setPen(QColor(0,0,0))
            self.qp.drawText(x, y, name)
            p0width = self.qp.fontMetrics().width(p[0])
            self.qp.setPen(QColor(187, 255, 255))
            self.qp.drawText(x+p0width, y, p[1])
            self.qp.setPen(QColor(0,0,0))
            p1width = self.qp.fontMetrics().width(p[1])
            self.qp.drawText(x+p0width+p1width, y, p[2])
        else:
            self.qp.setPen(QColor(0, 0, 0))
            self.qp.drawText(x, y, name)


    def drawText(self, event, qp):
        qp.setPen(QColor(168,34,3))
        qp.setFont(QFont("Decorative", 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)


    def drawRectangle(self, x, y):
        col = QColor(20,20,20)
        col.setNamedColor("#d4d4d4")
        self.qp.setPen(col)
        self.qp.setBrush(QColor(200,0,0))
        self.qp.drawRect(x ,y ,50,50)
        self.qp.setPen(col)
        self.qp.drawText(x+50,y+50,"x")






    def drawLines(self, qp, x1, y1, x2, y2):
        qp.setPen(QColor(0,0,0))
        qp.drawLine(x1, y1, (x1+x2)/2, y1)
        qp.drawLine((x1+x2)/2, y1, (x1+x2)/2, y2)
        qp.drawLine((x1+x2)/2, y2, x2, y2)






    #draw functions end#################

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = event.pos()

                self.statusBar().showMessage('x:%d, y:%d' % (pos.x(), pos.y()))

            else:
                pass  # do other stuff
        return QMainWindow.eventFilter(self, source, event)

    def eventFilter(self, source, event): #mouse event
        if event.type() == QtCore.QEvent.MouseMove:
            pos = event.pos()
            #print(pos,type(pos))
            #print(pos.x(), pos.y())
            self.mouseX, self.mouseY = pos.x(), pos.y()
            self.mousePos = pos
            self.statusBar().showMessage(str(pos))

            #draw detail info
            self.repaint()
        return QMainWindow.eventFilter(self, source ,event)

    def keyPressEvent(self, QKeyEvent):
        print(str(QKeyEvent.key()))
        if 0<=int(QKeyEvent.key())<128:
            print(chr(int(QKeyEvent.key())))


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("left button")
        elif QMouseEvent.button() == Qt.RightButton:
            print("right button")
        elif QMouseEvent.button() == Qt.MidButton:
            print("middle button")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.installEventFilter(ex)

    sys.exit(app.exec_())
