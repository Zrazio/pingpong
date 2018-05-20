from imports import *

class EndScreen(QtWidgets.QGraphicsScene):
    def __init__(self, size, text):
        super().__init__()
        self.scenesize = size
        self.windowSize = np.array(size)
        #self.scene.setSceneRect(QtCore.QRectF(0, 0, size[0], size[1]))
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(100, 100))
        gradient.setColorAt(0, QtCore.Qt.black)
        painter = QtGui.QPainter()
        self.setBackgroundBrush(QtGui.QBrush(gradient))
        self.drawBackground(painter,QtCore.QRectF())
        self.textItem = TextItem(text,[size[0],size[1]],self)

    def update(self):
        pass

class TextItem(QtWidgets.QGraphicsTextItem):
    def __init__(self,text ,position, scene,
                 font = QtGui.QFont("Times",30)):
        super(TextItem,self).__init__(text)
        self.setFont(font)
        self.setDefaultTextColor(QtCore.Qt.red)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
        scene.addItem(self)
        #self.setPos(QtCore.QPointF(position[0],position[1]))

    def hoverEnterEvent(self):
        self.setDefaultTextColor(QtCore.Qt.blue)





