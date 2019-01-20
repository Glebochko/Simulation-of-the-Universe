from graphics import *
from random import randint
from random import randrange
from time import sleep
from math import *



class SpaceObject:
    def __init__(self, x, y, mass, radius, speed, speedDirection, *args):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.mass = mass
        self.radius = radius
        self.speedDirection = speedDirection + 90
        self.speed = speed

        if len(args) == 0 :
            self.color = color_rgb(randrange(256), randrange(256), randrange(256))
        elif len(args) == 1 :
            self.color = args[0]



class Universe:
    def __init__(self, *args):
        self.status = 0 # 0 - expectations; 1 - work; 2 - quit
        self.infoWidth = 30
        self.infoHeight = 16
        self.trackPointsDistance = 5
        self.interation = 0
        self.myobjects = []
        self.ghost = []
        self.bgcolor = 'black'
        if len(args) == 2 :
            self.createWindow(args[0], args[1])
        elif len(args) == 0 :
            self.createWindow(1000, 700)


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

    def newObject(self, x, y, mass, radius, speed, speedDirection, *args):
        if len(args) == 0 :
            self.myobjects.append(SpaceObject(x, y, mass, radius, speed, speedDirection))
        elif len(args) == 1 :
            self.myobjects.append(SpaceObject(x, y, mass, radius, speed, speedDirection, args[0]))

    def firstShow(self):
        self.missingTrackPoints = self.trackPointsDistance - 1
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            self.ghost.append(Circle(Point(thisObj.x, thisObj.y), thisObj.radius))
            self.ghost[i].setFill(thisObj.color)
            self.ghost[i].setOutline('green')
            self.ghost[i].draw(self.window)

    def show(self):
        self.showInfo()
        self.missingTrackPoints += 1
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            dx = thisObj.x - thisObj.oldx
            dy = thisObj.y - thisObj.oldy
            thisObj.oldx = thisObj.x
            thisObj.oldy = thisObj.y
            if (dx != 0) | (dy != 0) :
                self.ghost[i].move(dx, dy)
                if self.missingTrackPoints >= self.trackPointsDistance :
                    track = Point(thisObj.x, thisObj.y)
                    track.setFill(thisObj.color)
                    track.draw(self.window)
                
        if self.missingTrackPoints >= self.trackPointsDistance :
            self.missingTrackPoints = 0

    def calculatePhysics(self):
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            V = thisObj.speed
            thisObj.speedDirection %= 360
            alpha = thisObj.speedDirection
            Vx = V * sin(radians(alpha)) 
            Vy = V * cos(radians(alpha)) 
            thisObj.x += Vx #floor(Vx)
            thisObj.y += Vy #floor(Vy)


    def quit(self):
        self.status = 2
        self.__del__()
        print('-- Exit! --')
        raise SystemExit(0)

    def universeLoop(self):
        while True :
            self.interation += 1
            self.calculatePhysics()
            
            self.show()
            #time.sleep(0.1)

            if self.interation == 200:
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

        self.newObject(20, 20, 20, 15, 3, -45, 'red')
        self.newObject(20, 200, 50, 10, 1, 0, 'blue')

        self.recordingInformation()
        self.status = 1
        self.firstShow()
        self.universeLoop()

    def __del__(self):
        if self.status == 2 :
            self.window.close()
            



def main():
    print('-- Simulation of the Universe! --')
    print('-- Swipe right! --')
    unv = Universe(1100, 750)
    unv.startSimulation()



main()