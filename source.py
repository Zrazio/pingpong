#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example we draw 6 lines using
different pen styles.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
import numpy as np
import sys


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.windowSize = [1000, 700]
        self.initUI()
        self.game = Game(np.array(self.windowSize), 10)
        self.setMouseTracking(True)
        self.setCursor(Qt.BlankCursor)

    def initUI(self):
        self.setGeometry(100, 100, self.windowSize[0], self.windowSize[1])
        self.setWindowTitle('Pen styles')
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()


    def draw(self, qp):
        planePosition = self.game.gamerPlaneDistanceFromOrigin
        rects = self.game.perspectiveRects

        #################       RECTANGLES       #################
        for rectangle in rects:
            rectangle.draw(qp, self.game.origin, planePosition)

        #################         RACKETS        #################
        for racket in self.game.rackets:
            racket.draw(qp, self.game.origin, planePosition)


        #################    STATIC BACKGROUND    #################
        pen = QPen(Qt.green, 2, Qt.SolidLine)
        qp.setPen(pen)
        Ox = self.game.origin[0]
        Oy = self.game.origin[1]

        firsRectPrim = rects[0].nodes * planePosition / rects[0].nodes[:, 2, np.newaxis]
        lastRectPrim = rects[-1].nodes * planePosition / rects[-1].nodes[:, 2, np.newaxis]

        qp.drawLine(firsRectPrim[0][0] + Ox, firsRectPrim[0][1] + Oy, lastRectPrim[0][0] + Ox, lastRectPrim[0][1] + Oy)
        qp.drawLine(firsRectPrim[1][0] + Ox, firsRectPrim[1][1] + Oy, lastRectPrim[1][0] + Ox, lastRectPrim[1][1] + Oy)
        qp.drawLine(firsRectPrim[2][0] + Ox, firsRectPrim[2][1] + Oy, lastRectPrim[2][0] + Ox, lastRectPrim[2][1] + Oy)
        qp.drawLine(firsRectPrim[3][0] + Ox, firsRectPrim[3][1] + Oy, lastRectPrim[3][0] + Ox, lastRectPrim[3][1] + Oy)

    def mouseMoveEvent(self, event):
        self.game.rackets[1].move(np.array([event.x() - self.game.origin[0], event.y() - self.game.origin[1]], dtype=int))
        # print(self.game.rackets[1].)
        self.repaint()


        
class object3D():
    def magicPerspectiveProjector(self, points, distanceFromPlane):  # points -> ndarray with shape [x, 3]
        try:
            pointsPrim = points * distanceFromPlane / points[:, 2]
        except ValueError:
            pointsPrim = points * distanceFromPlane / points[:, 2, np.newaxis]

        return pointsPrim.astype(int)

class Rectangle(object3D):
    def __init__(self, windowSize, zPosition):
        self.width = windowSize[0]
        self.height = windowSize[1]
        self.position = np.array([0, 0, zPosition])
        self.zPosition = zPosition
        self.nodes = None
        self.createNodes()

    def createNodes(self):
        h = self.height
        w = self.width
        self.nodes = np.array([[-w // 2, -h // 2, self.zPosition],
                  [-w // 2, h // 2, self.zPosition],
                  [w // 2, h // 2, self.zPosition],
                  [w // 2, -h // 2, self.zPosition]])

    def draw(self, qp, origin, positionOfPlane):
        projectedNodes = self.magicPerspectiveProjector(self.nodes, positionOfPlane)
        pen = QPen(Qt.green, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(origin[0] + projectedNodes[0][0], origin[1] + projectedNodes[0][1], origin[0] + projectedNodes[1][0], origin[1] + projectedNodes[1][1])
        qp.drawLine(origin[0] + projectedNodes[1][0], origin[1] + projectedNodes[1][1], origin[0] + projectedNodes[2][0], origin[1] + projectedNodes[2][1])
        qp.drawLine(origin[0] + projectedNodes[2][0], origin[1] + projectedNodes[2][1], origin[0] + projectedNodes[3][0], origin[1] + projectedNodes[3][1])
        qp.drawLine(origin[0] + projectedNodes[3][0], origin[1] + projectedNodes[3][1], origin[0] + projectedNodes[0][0], origin[1] + projectedNodes[0][1])



class Racket(object3D):
    def __init__(self, windowSize, zPosition, color, width=300, height=200):
        self.xLimit = windowSize[0] / 2 - width / 2
        self.yLimit = windowSize[1] / 2 - height / 2

        self.width = width
        self.height = height
        self.nodes = None
        self.position = np.array([0, 0, zPosition])
        self.createNodes()
        self.color = color

    def move(self, newPosition):
        if newPosition[0] > self.xLimit:
            newPosition[0] = self.xLimit
        elif newPosition[0] < -self.xLimit:
            newPosition[0] = -self.xLimit

        if newPosition[1] > self.yLimit:
            newPosition[1] = self.yLimit
        elif newPosition[1] < -self.yLimit:
            newPosition[1] = -self.yLimit

        self.position = np.array([newPosition[0], newPosition[1], self.position[2]])
        self.createNodes()

    def createNodes(self):
        x = self.width // 2
        y = self.height // 2
        z = self.position[2]
        self.nodes = np.array([[-x + self.position[0], -y + self.position[1], z],
                               [-x + self.position[0], y + self.position[1], z],
                               [x + self.position[0], y + self.position[1] , z],
                               [x + self.position[0], -y + self.position[1] , z]])

    def draw(self, qp, origin, positionOfPlane):
        projectedNodes = self.magicPerspectiveProjector(self.nodes, positionOfPlane)
        pen = QPen(self.color, 2, Qt.SolidLine)
        brush = QBrush(QColor(255, 255, 255, 100))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(origin[0] + projectedNodes[0][0], origin[1] + projectedNodes[0][1],
                    abs(projectedNodes[0][0] - projectedNodes[2][0]), abs(projectedNodes[0][1] - projectedNodes[2][1]))

        qp.drawLine(origin[0] + projectedNodes[0][0], origin[1] + (projectedNodes[0][1] + projectedNodes[2][1])/2,
                    origin[0] + projectedNodes[2][0], origin[1] + (projectedNodes[0][1] + projectedNodes[2][1])/2)

        qp.drawLine( origin[0] + (projectedNodes[0][0] + projectedNodes[2][0])/2,  origin[1] + projectedNodes[0][1],
                     origin[0] + (projectedNodes[0][0] + projectedNodes[2][0])/2, origin[1] + projectedNodes[1][1])


class Game():
    def __init__(self, windowSize, gamerPosition):
        self.origin = windowSize / 2
        self.gamerPlaneDistanceFromOrigin = gamerPosition
        self.windowSize = windowSize
        self.rackets = None
        self.endDistance = 35   #  distance at which room ends
        self.startDistance = 11    # distance at which room starts
        self.perspectiveRects = []
        self.createRackets()
        self.createPerspectiveRects()
        self.createBall()

    def createRackets(self):
        myRacket1 = Racket(self.windowSize, self.endDistance, Qt.blue)
        myRacket2 = Racket(self.windowSize, self.startDistance, Qt.red)
        self.rackets = [myRacket1, myRacket2]

    def createPerspectiveRects(self):
        N = 8
        for dist in np.linspace(self.startDistance, self.endDistance, N):
            self.perspectiveRects.append(Rectangle(self.windowSize, dist))

    def createBall(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())