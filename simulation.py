from graphics import *
from random import randint
from random import randrange
from time import sleep



class SpaceObject:
    def __init__(self, x, y, mass, radius, *args):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.mass = mass
        self.radius = radius

        if len(args) == 0 :
            self.color = color_rgb(randrange(256), randrange(256), randrange(256))
        elif len(args) == 1 :
            self.color = args[0]




class Universe:
    def __init__(self, *args):
        self.status = 0 # 0 - expectations; 1 - work; 2 - quit
        self.infoWidth = 30
        self.infoHeight = 16
        self.interation = 0
        self.myobjects = []
        self.ghost = []
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
        self.infoText.setText(self.interation)

    def newObject(self, x, y, mass, radius, *args):
        if len(args) == 0 :
            self.myobjects.append(SpaceObject(x, y, mass, radius))
        elif len(args) == 1 :
            self.myobjects.append(SpaceObject(x, y, mass, radius, args[0]))

    def firstShow(self):
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            self.ghost.append(Circle(Point(thisObj.x, thisObj.y), thisObj.radius))
            self.ghost[i].setFill(thisObj.color)
            self.ghost[i].setOutline('green')
            self.ghost[i].draw(self.window)

    def show(self):
        self.showInfo()
        for i in range(len(self.myobjects) - 1):
            thisObj = self.myobjects[i]
            if thisObj.oldx != thisObj.x | thisObj.oldy != thisObj.y :
                self.ghost[i].move(thisObj.x - thisObj.oldx, thisObj.y - thisObj.oldy)

    def calculatePhysics(self):
        for i in range(len(self.myobjects)):
            pass

    def quit(self):
        self.status = 2
        self.__del__()
        print('-- Exit! --')
        raise SystemExit(0)

    def universeLoop(self):
        self.firstShow()
        while True :
            self.myobjects[0].x += 10
            self.myobjects[0].y += 10


            self.interation += 1
            self.calculatePhysics()
            self.show()
            time.sleep(0.5)

            if self.interation == 5:
                self.quit()

    def recordingInformation(self):
        objCount = len(self.myobjects)
        self.distance = [[0] * objCount for i in range(objCount)]
        self.influence = [[0] * objCount for i in range(objCount)]

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

        self.newObject(300, 300, 20, 15, 'red')
        self.newObject(400, 200, 50, 10, 'blue')

        self.recordingInformation()
        self.universeLoop()

    def __del__(self):
        if self.status == 2 :
            self.window.close()
            



def main():
    print('-- Simulation of the Universe! --')
    unv = Universe(900, 600)
    unv.startSimulation()



main()