from imports import *
from endscreen import *


def magicPerspectiveProjector(points, distanceFromPlane = 200):  # points -> ndarray with shape [x, 3]
    try:
        pointsPrim = points * distanceFromPlane / points[:, 2]
    except ValueError:
        pointsPrim = points * distanceFromPlane / points[:, 2, np.newaxis]
    # return pointsPrim.astype(int)
    return pointsPrim


class AThread(QtCore.QThread):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.scene = view.graphicsscene
        self.ingame = True
        self.endscene = EndScreen(self.view.scenesize,"pupcia")



    def run(self):
        while 1:
            if self.scene.myPoint == True:
                self.scene.ball.color = QtCore.Qt.red
                self.view.setScene(EndScreen(self.view.scenesize,"pupcia"))
                self.ingame = False
            elif self.scene.enemyPoint == True:
               # print("pupcia")
                #self.scene.ball.color = QtCore.Qt.blue
                #self.scene.invisible()
                self.view.setScene(self.endscene)
                #self.ingame = False
                #self.scene.enemyPoint = False;
                #del self.scene

            if self.ingame:
                self.scene.update()
                self.scene.moveBall()
                self.scene.checkCollision()
            time.sleep(1./120)



class Racket(QtWidgets.QGraphicsItem):

    def __init__(self, windowSize, zPosition,scene, color, width=300, height=200):
        super().__init__()
        self.xLimit = windowSize[0] / 2 - width / 2
        self.yLimit = windowSize[1] / 2 - height / 2
        self.origin = windowSize/2
        self.width = width
        self.height = height
        self.nodes = None
        self.position = np.array([0, 0, zPosition])
        self.createNodes()
        self.color = color
        scene.addItem(self)

    def getRacketRect(self):
        return [self.position[0]-(self.width/2),self.position[1] - (self.height/2), self.width, self.height]

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
                               [x + self.position[0], y + self.position[1], z],
                               [x + self.position[0], -y + self.position[1], z]])
        self.projectedNodes = magicPerspectiveProjector(self.nodes)

    def boundingRect(self):
        return QtCore.QRectF(self.origin[0] + self.projectedNodes[0][0],self.origin[1] + self.projectedNodes[0][1],
                            abs(self.projectedNodes[0][0])+abs(self.projectedNodes[2][0]),
                             abs(self.projectedNodes[0][1]) + abs(self.projectedNodes[2][1]))

    def paint(self, qp, o, widgets=None):
        pen = QtGui.QPen(self.color, 2, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 100))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(self.origin[0] + self.projectedNodes[0][0], self.origin[1] + self.projectedNodes[0][1],
                    abs(self.projectedNodes[0][0] - self.projectedNodes[2][0]), abs(self.projectedNodes[0][1] - self.projectedNodes[2][1]))

        qp.drawLine(self.origin[0] + self.projectedNodes[0][0], self.origin[1] + (self.projectedNodes[0][1] + self.projectedNodes[2][1]) / 2,
                    self.origin[0] + self.projectedNodes[2][0], self.origin[1] + (self.projectedNodes[0][1] + self.projectedNodes[2][1]) / 2)

        qp.drawLine(self.origin[0] + (self.projectedNodes[0][0] + self.projectedNodes[2][0]) / 2, self.origin[1] + self.projectedNodes[0][1],
                    self.origin[0] + (self.projectedNodes[0][0] + self.projectedNodes[2][0]) / 2, self.origin[1] + self.projectedNodes[1][1])


class BackgroundRect(QtWidgets.QGraphicsItem):

    def __init__(self, windowSize, zPosition,scene,color = QtCore.Qt.green,style=QtCore.Qt.SolidLine):
        super().__init__()
        self.width = windowSize[0]
        self.height = windowSize[1]
        self.position = np.array([0, 0, zPosition])
        self.zPosition = zPosition
        self.origin = windowSize/2
        self.nodes = None
        self.color = color
        self.style = style
        self.penWidth = 1
        self.createNodes()
        scene.addItem(self)

    def moveRect(self,z):
        self.zPosition = z
        self.createNodes()

    def createNodes(self):
        h = self.height
        w = self.width
        self.nodes = np.array([[-w // 2, -h // 2, self.zPosition],
                               [-w // 2, h // 2, self.zPosition],
                               [w // 2, h // 2, self.zPosition],
                               [w // 2, -h // 2, self.zPosition]])
        self.projectedNodes = magicPerspectiveProjector(self.nodes)

    def boundingRect(self):
        return QtCore.QRectF(self.origin[0] + self.projectedNodes[0][0],self.origin[1] + self.projectedNodes[0][1],
                            abs(self.projectedNodes[0][0])+abs(self.projectedNodes[2][0]),
                             abs(self.projectedNodes[0][1]) + abs(self.projectedNodes[2][1]))

    def paint(self,p ,o ,widgets=None):
        pen = QtGui.QPen(self.style)
        pen.setColor(self.color)
        pen.setWidth(self.penWidth)
        p.setPen(pen)

        p.drawLine(self.origin[0] + self.projectedNodes[0][0], self.origin[1] + self.projectedNodes[0][1],
                    self.origin[0] + self.projectedNodes[1][0], self.origin[1] + self.projectedNodes[1][1])
        p.drawLine(self.origin[0] + self.projectedNodes[1][0], self.origin[1] + self.projectedNodes[1][1],
                    self.origin[0] + self.projectedNodes[2][0], self.origin[1] + self.projectedNodes[2][1])
        p.drawLine(self.origin[0] + self.projectedNodes[2][0], self.origin[1] + self.projectedNodes[2][1],
                    self.origin[0] + self.projectedNodes[3][0], self.origin[1] + self.projectedNodes[3][1])
        p.drawLine(self.origin[0] + self.projectedNodes[3][0], self.origin[1] + self.projectedNodes[3][1],
                    self.origin[0] + self.projectedNodes[0][0], self.origin[1] + self.projectedNodes[0][1])


class Ball(QtWidgets.QGraphicsItem):
    def __init__(self, windowSize, radius, scene, color=QtCore.Qt.yellow):
        super().__init__()
        self.origin = windowSize/2
        self.velocityVector = np.array([-2.5, 5.0, 3.])
        self.position = np.array([5, 5, 280])
        self.radius = radius
        self.color = color
        self.nodes = None
        self.createNodes()
        scene.addItem(self)

    def move(self):
        self.position = self.position + self.velocityVector
        self.createNodes()
        return self.position

    def boundingRect(self):
        projectedRadius = np.linalg.norm(self.projectedNodes[0] - self.projectedNodes[1])
        return QtCore.QRectF(self.projectedNodes[0][0] + self.origin[0] - projectedRadius, self.projectedNodes[0][1] + self.origin[1] - projectedRadius,
                       projectedRadius * 2, projectedRadius * 2)

    def paint(self,p ,o ,widgets=None):
        pen = QtGui.QPen(self.color, 2, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(self.color)
        p.setPen(pen)
        p.setBrush(brush)
        projectedRadius = np.linalg.norm(self.projectedNodes[0] - self.projectedNodes[1])
        # print(projectedRadius)
        p.drawEllipse(self.projectedNodes[0][0] + self.origin[0] - projectedRadius, self.projectedNodes[0][1] + self.origin[1] - projectedRadius,
                       projectedRadius * 2, projectedRadius * 2)

    def createNodes(self):
        self.nodes = np.array([self.position, [self.position[0] + self.radius, self.position[1], self.position[2]]])
        self.projectedNodes = magicPerspectiveProjector(self.nodes)
        # print(self.projectedNodes)


class Game(QtWidgets.QGraphicsView):
    def __init__(self,parent = None):
        QtWidgets.QGraphicsView.__init__(self)
        self.resize(1500,1000)
        self.setMouseTracking(True)
        self.scenesize = (1400,950)
        self.graphicsscene = Scene(self.scenesize)
        self.moveracket = False
        self.setScene(self.graphicsscene)


    def mouseMoveEvent(self,e):
        if self.moveracket :
            self.graphicsscene.moveRacket(e)

    def mousePressEvent(self,e):
        if self.moveracket:
            self.moveracket = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.moveracket = True
            self.setCursor(QtCore.Qt.BlankCursor)


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        self.setWindowTitle("pong")
        self.resize(1500,1000)
        self.graphicsView = Game()
        self.setCentralWidget(self.graphicsView)
        self.show()


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self,size):
        super().__init__()
        self.scenesize = size
        self.startDistance = 220
        self.endDistance = 700
        self.perspectiveRects = []
        self.windowSize = np.array(size)
        self.origin = self.windowSize/2
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(100, 100))
        gradient.setColorAt(0, QtCore.Qt.black)
        painter = QtGui.QPainter()
        self.setBackgroundBrush(QtGui.QBrush(gradient))
        self.drawBackground(painter,QtCore.QRectF())
        self.createPerspectiveRects()
        self.enemyRacket = Racket(self.windowSize, self.endDistance, self, QtCore.Qt.blue)
        self.ball = Ball(self.windowSize, 60, self)
        self.ballRect = BackgroundRect(self.windowSize, 60,self, color=QtCore.Qt.white)
        self.myRacket = Racket(self.windowSize,self.startDistance,self,QtCore.Qt.red)
        self.myPoint = False
        self.enemyPoint = False
        #self.objects = [self.enemyRacket,self.ball]
        #self.objects = list(zip(self.objects,self.perspectiveRects))

    def createPerspectiveRects(self):
        N = 8
        for dist in np.linspace(self.startDistance, self.endDistance, N):
            self.perspectiveRects.append(BackgroundRect(self.windowSize, dist,self))

    def moveRacket(self,event):
        self.myRacket.move(np.array([event.x() - self.origin[0], event.y() - self.origin[1]], dtype=int))
        #self.update()

    def moveBall(self):
        z = self.ball.move()
        self.ballRect.moveRect(z[2])
        self.enemyRacket.move([z[0],z[1]])

    def invisible(self):
        for i in self.perspectiveRects:
            i.setVisible(False)
        self.ball.setVisible(False)
        self.enemyRacket.setVisible(False)
        self.myRacket.setVisible(False)

    def checkCollision(self):
        rad = self.ball.radius
        ballX = self.ball.position[0]
        ballY = self.ball.position[1]
        ballZ = self.ball.position[2]
        start = self.startDistance
        meta = self.endDistance
        width = self.perspectiveRects[0].width
        height = self.perspectiveRects[0].height

        #print('ballZ', ballZ)

        if ballX - rad < -width/2 or ballX + rad > width/2:
            self.ball.velocityVector[0] *= -1

        if ballY - rad < -height/2 or ballY + rad > height/2:
            self.ball.velocityVector[1] *= -1

        if ballZ  < start:
            rect = self.myRacket.getRacketRect()
            if ballX > rect[0] and ballX < rect[0]+rect[2] and ballY > rect[1] and ballY < rect[1]+rect[3]:
                self.ball.velocityVector[2] *= -1
            else:
                self.ball.velocityVector[2] *= 0
                self.enemyPoint = True

        elif ballZ  > meta:
            rect = self.enemyRacket.getRacketRect()
            if ballX > rect[0] and ballX < rect[0]+rect[2] and ballY > rect[1] and ballY < rect[1]+rect[3]:
                self.ball.velocityVector[2] *= -1
            else:
                self.ball.velocityVector[2] *= -1
                self.myPoint = True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    gameLoop = AThread(ex.graphicsView)
    gameLoop.start()
    sys.exit(app.exec_())
