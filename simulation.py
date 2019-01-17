from graphics import *
from random import randint
from random import randrange
from time import sleep



class SpaseObject:
    def __init__(self, x, y, mass, *args):
        self.x = x
        self.y = y
        self.mass = mass

        if len(args) == 0 :
            self.color = color_rbg(randrange(256), randrange(256), randrange(256))

        if len(args) == 1 :
            self.color = args[0]




class Universe:
    def __init__(self, *args):
        self.status = 0
        self.infoWidth = 30
        self.infoHeight = 16
        self.interation = 0
        self.bgcolor = 'black'
        if len(args) == 2 :
            self.createWindow(args[0], args[1])


    def createWindow(self, width, height):
        self.width = width
        self.height = height
        self.infoText = Text(Point(self.width - self.infoWidth / 2, self.infoHeight / 2), self.interation)
        self.infoText.setFill('white')
        self.window = GraphWin('Simulation of the Universe!', width, height)

    def clearWindow(self):
        p1 = Point(0, 0)
        p2 = Point(self.width, 0)
        p3 = Point(self.width, self.height)
        p4 = Point(0, self.height)

        vertices = [p1, p2, p3, p4]

        cleanWindow = Polygon(vertices)
        cleanWindow.setOutline(self.bgcolor)
        cleanWindow.setFill(self.bgcolor)

        cleanWindow.draw(self.window)

    def clearInfoList(self):
        p1 = Point(self.width - self.infoWidth - 1, 0)
        p2 = Point(self.width - 1, 0)
        p3 = Point(self.width - 1, self.infoHeight)
        p4 = Point(self.width - self.infoWidth - 1, self.infoHeight)

        vertices = [p1, p2, p3, p4]

        cleanInfoList = Polygon(vertices)
        cleanInfoList.setOutline('green')
        cleanInfoList.setFill(self.bgcolor)

        cleanInfoList.draw(self.window)

    def showInfo(self):
        #self.clearInfoList()
        #infoText = Text(Point(self.width - self.infoWidth / 2, self.infoHeight / 2), self.interation)
        #infoText.setFill('white')
        #infoText.draw(self.window)
        self.infoText.setText(self.interation)

    def show(self):
        self.showInfo()

    def universeLoop(self):
        while True :
            self.interation += 1
            self.show()
            time.sleep(0.5)

    def preStart(self):
        self.clearWindow()
        message = Text(Point(self.window.getWidth()/2, 30), 'Click on anywhere to start simulation')
        message.setFill('white')
        message.draw(self.window)
        self.window.getMouse()
        self.clearWindow()
        self.clearInfoList()
        self.infoText.draw(self.window)

    def startSimulation(self):
        self.preStart()
        self.status = 1
        self.universeLoop()
'''
    def __del__(self):
        if self.status == 1 :
            self.window.close()
            '''



def main():
    print('-- Simulation of the Universe! --')
    unv = Universe(900, 600)
    unv.startSimulation()



main()