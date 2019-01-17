from graphics import *
from random import randint
from random import randrange



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
        if len(args) == 2 :
            self.createWindow(args[0], args[1])


    def createWindow(self, width, height):
        self.width = width
        self.height = height
        self.window = GraphWin('Simulation of the Universe!', width + 1 + self.infoWidth, height)

    def startSimulation(self):
        self.showInfo()
        pass

    def __del__(self):
        if self.status == 1 :
            self.window.close()



def main():
    print('-- Simulation of the Universe! --')
    unv = Universe(600, 400)
    unv.startSimulation()



main()