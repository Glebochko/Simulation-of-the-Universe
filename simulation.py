from graphics import *
from random import randint
from random import randrange
from time import sleep
from math import *
import pdb


class SpaceObject:
    def __init__(self, x, y, mass, radius, speed, speedDirection, *args):
        self.static = False
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.mass = mass
        self.radius = radius

        self.speedDirection = (speedDirection + 90) % 360
        self.speed = speed
        alpha = self.speedDirection
        self.Vx = speed * sin(radians(alpha)) 
        self.Vy = speed * cos(radians(alpha)) 

        self.resForce = []
        for i in range(3):
            self.resForce.append(0)
        self.forceDirection = 0

        if len(args) == 0 :
            self.color = color_rgb(randrange(256), randrange(256), randrange(256))
        elif len(args) == 1 :
            self.color = args[0]



class Universe:
    def __init__(self, *args):
        self.status = 0 # 0 - expectations; 1 - work; 2 - quit
        self.objCount = 0
        self.infoWidth = 30
        self.infoHeight = 16
        self.interation = 0
        self.myobjects = []
        self.ghost = []
        self.bgcolor = 'black'

        self.outputObjectsInteractionInfo = True
        self.drawingTrackPoints = True
        self.trackPointsDistance = 2

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


    def showObjInteractionInfo(self, firstFlag):
        #pdb.set_trace() 
        if self.outputObjectsInteractionInfo :
            for i in range(self.objCount):
                for j in range(i + 1, self.objCount):
                    self.distanceLabel[i][j].setText(str(floor(self.distance[i][j][0])) + '; ' + str(floor(self.force[i][j][0])))
                    anchor = self.distanceLabel[i][j].anchor
                    oldx = anchor.x
                    oldy = anchor.y
                    objA = self.myobjects[i]
                    objB = self.myobjects[j]
                    xDistance = abs(objA.x - objB.x)
                    yDistance = abs(objA.y - objB.y)

                    if objA.x >= objB.x :
                        newx = objA.x - xDistance / 2
                    else :
                        newx = objA.x + xDistance / 2

                    if objA.y >= objB.y :
                        newy = objA.y - yDistance / 2
                    else :
                        newy = objA.y + yDistance / 2

                    dx = newx - oldx
                    dy = newy - oldy

                    if not firstFlag :
                        self.distanceLabel[i][j].move(dx, dy)
                    else :
                        self.distanceLabel[i][j].draw(self.window)
                        #print(i + 1, ' ', j + 1)
                        self.distanceLabel[i][j].setTextColor('green')
                        self.distanceLabel[i][j].move(dx, dy)


    def drawTrackPoints(self, thisObj):
        if self.drawingTrackPoints :
            if self.missingTrackPoints >= self.trackPointsDistance :
                track = Point(thisObj.x, thisObj.y)
                track.setFill(thisObj.color)
                track.draw(self.window)


    def firstShow(self):
        self.missingTrackPoints = self.trackPointsDistance - 1
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            self.ghost.append(Circle(Point(thisObj.x, thisObj.y), thisObj.radius))
            self.ghost[i].setFill(thisObj.color)
            self.ghost[i].setOutline('green')
            self.ghost[i].draw(self.window)
        self.showObjInteractionInfo(True)


    def show(self):
        self.showInfo()
        if self.drawingTrackPoints :
            if self.missingTrackPoints >= self.trackPointsDistance :
                self.missingTrackPoints = 0
            self.missingTrackPoints += 1

        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            dx = thisObj.x - thisObj.oldx
            dy = thisObj.y - thisObj.oldy
            thisObj.oldx = thisObj.x
            thisObj.oldy = thisObj.y
            if (dx != 0) | (dy != 0) :
                self.ghost[i].move(dx, dy)
                self.drawTrackPoints(thisObj)

        self.showObjInteractionInfo(False)   


    def getResultantForceOld(self):
        for i in range(self.objCount):
            thisObj = self.myobjects[i]

            for j in range (self.objCount):
                if i != j :
                    #pdb.set_trace()
                    targetObj = self.myobjects[j]
                    rx = thisObj.x - targetObj.x
                    ry = thisObj.y - targetObj.y
                    beta = atan(radians(floor(rx / ry)))
                    alpha = 0

                    if (rx < 0) & (ry > 0):
                        alpha = 90 - beta
                    elif (rx < 0) & (ry < 0) :
                        alpha = 270 + beta
                    elif (rx > 0) & (ry > 0) :
                        alpha = 180 - beta
                    elif (rx > 0) & (ry < 0) :
                        alpha = 270 - beta

                    #alpha += 90
                    fx = self.force[i][j] * cos(radians(alpha))
                    fy = self.force[i][j] * sin(radians(alpha))

                    resf = thisObj.resForce
                    resAlpha = thisObj.forceDirection - 90
                    resfx = resAlpha * cos(radians(resAlpha))
                    resfy = resAlpha * sin(radians(resAlpha))

                    resfx += fx
                    resfy += fy
                    
                    if resfy != 0 :
                        beta = atan(radians(floor(resfx / resfy)))
                        resAlpha = 0

                        if (resfx < 0) & (resfy > 0):
                            resAlpha = 90 - beta
                        elif (resfx < 0) & (resfy < 0) :
                            resAlpha = 270 + beta
                        elif (resfx > 0) & (resfy > 0) :
                            resAlpha = 180 - beta
                        elif (resfx > 0) & (resfy < 0) :
                            resAlpha = 270 - beta
                    else :
                        resAlpha = 0

                    resAlpha += 90
                    thisObj.forceDirection = resAlpha
                    thisObj.resForce = sqrt(pow(resfx, 2) + pow(resfy, 2))


                    #forceLine = Line(Point(thisObj.x, thisObj.y), Point())
                    #self.drawForceDirection(thisObj)


    def getResultantForce(self):
        for i in range(self.objCount):
            if not self.myobjects[i].static :
                self.myobjects[i].resForce[1] = 0
                self.myobjects[i].resForce[2] = 0

                for j in range(self.objCount):
                    if i != j :
                        fx = self.force[i][j][1]
                        fy = self.force[i][j][2]
                        self.myobjects[i].resForce[1] += fx
                        self.myobjects[i].resForce[2] += fy

                rfx = self.myobjects[i].resForce[1]
                rfy = self.myobjects[i].resForce[2]

                rf = sqrt(pow(abs(rfx), 2) + pow(abs(rfy), 2))
                self.myobjects[i].resForce[0] = rf
                x = 10                 


    def getDistance(self, *args):
        if len(args) == 2 :
            objA = self.myobjects[args[0]]
            objB = self.myobjects[args[1]]
            xDistance = (objB.x - objA.x)
            yDistance = (objB.y - objA.y)
            ABDistance = sqrt(pow(xDistance, 2) + pow(yDistance, 2))
            
            return [ABDistance, xDistance, yDistance]

        elif len(args) == 0 :
            for i in range(self.objCount):
                for j in range(i + 1, self.objCount):
                    self.distance[i][j] = self.getDistance(i, j)
                    self.distance[j][i] = self.distance[i][j]
                self.distance[i][i] = [0, 0, 0]


    def getForce(self, *args):
        if len(args) == 2 :
            objA = self.myobjects[args[0]]
            objB = self.myobjects[args[1]]
            G = 0.3
            ABforce = G * objA.mass * objB.mass 
            ABforce /= pow(self.distance[args[0]][args[1]][0], 2)

            rx = self.distance[args[0]][args[1]][1]
            ry = self.distance[args[0]][args[1]][2]
            tgb = rx / ry
            yForce = ABforce / sqrt(pow(tgb, 2) + 1)
            xForce = tgb * yForce

            if ry < 0 :
                xForce *= -1
            if rx < 0 :
                yForce *= -1

            return [ABforce, xForce, yForce]

        elif len(args) == 0 :
            for i in range(self.objCount):
                for j in range(i + 1, self.objCount):
                    self.force[i][j] = self.getForce(i, j)
                    self.force[j][i] = self.force[i][j]
                self.force[i][i] = [0, 0, 0]


    def calculatePhysics(self):
        for i in range(len(self.myobjects)):
            thisObj = self.myobjects[i]
            if not thisObj.static :
                self.getDistance()
                self.getForce()
                self.getResultantForce()

                Vx = thisObj.Vx
                Vy = thisObj.Vy
                ax = thisObj.resForce[1] / thisObj.mass
                ay = thisObj.resForce[2] / thisObj.mass
                Vx += ax
                Vy += ay

                thisObj.x += Vx
                thisObj.y += Vy
                thisObj.Vx = Vx
                thisObj.Vy = Vy
                thisObj.speed = sqrt(pow(Vx, 2) + pow(Vy, 2))


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
        self.objCount = len(self.myobjects)
        #self.distance = [[0] * self.objCount for i in range(self.objCount)]
        #self.force = [[0] * self.objCount for i in range(self.objCount)]
        #self.distanceLabel = [[Text(Point(10, 10), 'ERROR')] * self.objCount for i in range(self.objCount)]
        
        self.distanceLabel = []
        self.force = []
        self.distance = []
        for i in range(self.objCount):
            self.distanceLabel.append([])
            self.force.append([])
            self.distance.append([])
            for j in range(self.objCount):
                self.distanceLabel[i].append(Text(Point(10, 10), 'ERROR'))
                self.force[i].append([])
                self.distance[i].append([])
                for g in range(3):
                    self.force[i][j].append(0)
                    self.distance[i][j].append(0)


    def preStart(self):
        self.clearWindow()
        message = Text(Point(self.window.getWidth()/2, 30), 'Click on anywhere to start simulation')
        message.setFill('white')
        message.draw(self.window)
        self.window.getMouse()
        self.clearWindow()
        self.clearInfoList()
        self.infoText.draw(self.window)


    def setObjectsConfiguration(self, configNumber):
        if configNumber == 1 :
            self.newObject(400, 350, 1000, 10, -3, 0, 'red')
            self.newObject(400, 400, 1700, 12, 0, 0, 'yellow')
            self.myobjects[1].static = True

        elif configNumber == 2 :
            self.newObject(40, 50, 1000, 10, -3, 0, 'red')
            self.newObject(40, 400, 1700, 12, 0, 0, 'yellow')
            self.newObject(30, 250, 2000, 10, 5, 0, 'blue')

        elif configNumber == 3 :
            pass


    def startSimulation(self):
        self.preStart()

        self.setObjectsConfiguration(1)
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