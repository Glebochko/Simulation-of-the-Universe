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
        self.clearInfoList()
        info = Text(Point(self.width - self.infoWidth / 2, self.infoHeight / 2), self.interation)
        info.setFill('white')
        info.draw(self.window)

    def show(self):
        self.showInfo()

    def universeLoop(self):

        while True :
            self.interation += 1
            self.show()
            time.sleep(0.5)

    def startSimulation(self):
        self.status = 1
        self.universeLoop()

    def __del__(self):
        if self.status == 1 :
            self.window.close()



def main():
    print('-- Simulation of the Universe! --')
    unv = Universe(600, 400)
    unv.startSimulation()



main()