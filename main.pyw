#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import random
import time

class KeyboardKeys:
    KEY_UP = 16777235
    KEY_DOWN = 16777237
    KEY_RIGHT = 16777236
    KEY_LEFT = 16777234

    
class Game(QtGui.QWidget):
    BoxSize = 100
    BtwBox = 10

    # [R, G, B, TextXPos, TextYPos]
    Colors = {
        8 : [242, 177, 121, 40, 60],
        2 : [238, 228, 218, 40, 60],
        4 : [237, 224, 200, 40, 60],
        32 : [246, 124, 95, 33, 60],
        16 : [245, 149, 99, 33, 60],
        64 : [246, 94, 59, 33, 60],
        128 : [237, 207, 114, 25, 60],
        256 : [237, 204, 97, 25, 60],
        512 : [237, 200, 80, 25, 60],
        1024 : [237, 197, 63, 17, 60],
        2048 : [237, 190, 30, 17, 60],
        4096 : [237, 180, 15, 17, 60],
        8192 : [237, 160, 15, 17, 60],
        None : [205, 193, 180]
    }
    
    Boxs = [
        [ None, None, None, None ],
        [ None, None, None, None ],
        [ None, None, None, None ],
        [ None, None, None, None ]
    ]

    GameOver = False

    Score = 0

    TextFont = QtGui.QFont()
    TextFont.setBold(True)
    TextFont.setPointSize(25)
    TextFont.setFamily("Arial")
    
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()

    def initUI(self):      
        self.setGeometry(100, 100, self.BoxSize*4+self.BtwBox*5+150, self.BoxSize*4+self.BtwBox*5)
        self.setWindowTitle('2048 Game')

        self.RestartButton = QtGui.QPushButton('Restart', self)
        self.RestartButton.setGeometry(QtCore.QRect(self.BoxSize*4+self.BtwBox*5+25, (self.BoxSize*4+self.BtwBox*5)//2, 100, 50))
        self.RestartButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RestartButton.clicked.connect(self.RestartGame)

        self.GameInfo = QtGui.QLabel('Score: 0', self)
        self.GameInfo.setGeometry(QtCore.QRect(self.BoxSize*4+self.BtwBox*5+55, (self.BoxSize*4+self.BtwBox*5)//4 + 25, 100, 50))
        self.GameInfo.setFocusPolicy(QtCore.Qt.NoFocus)

        self.GameOverText = QtGui.QLabel('', self)
        self.GameOverText.setGeometry(QtCore.QRect(self.BoxSize*4+self.BtwBox*5+45, (self.BoxSize*4+self.BtwBox*5)//2+75, 100, 50))
        self.GameOverText.setFocusPolicy(QtCore.Qt.NoFocus)

        xy = self.GetRandomXY()
        self.Boxs[xy[1]][xy[0]] = self.GetRandomBoxValue()
        
        xy1 = self.GetRandomXY()
        self.Boxs[xy1[1]][xy1[0]] = self.GetRandomBoxValue()
        
        self.show()

    def keyPressEvent(self, event):
        if self.GameOver == False:
            Moved = False
            if event.key() == KeyboardKeys.KEY_LEFT :
                # Move
                for line in range(4):
                    i = 0
                    while i < 4:
                        if self.Boxs[line][i] == None:
                            i += 1
                        else:
                            if i == 0:
                                i += 1
                                continue
                            else:
                                if self.Boxs[line][i-1] == None:
                                    self.Boxs[line][i-1] = self.Boxs[line][i]
                                    self.Boxs[line][i] = None
                                    Moved = True
                                    i = 0
                                else:
                                    i += 1
                # Sum
                for line in range(4):
                    i = 0
                    while i < 4:
                        if self.Boxs[line][i] == None:
                            i += 1
                        else:
                            if i == 3:
                                i += 1
                                continue
                            else:
                                if self.Boxs[line][i+1] != None:
                                    if self.Boxs[line][i+1] == self.Boxs[line][i]:
                                        self.Boxs[line][i+1] = None
                                        self.Boxs[line][i] = self.Boxs[line][i]+self.Boxs[line][i]
                                        self.Score += self.Boxs[line][i]
                                        Moved = True
                                        i += 2
                                    else:
                                        i += 1
                                    
                                else:
                                    i += 1
                # Move
                for line in range(4):
                    i = 0
                    while i < 4:
                        if self.Boxs[line][i] == None:
                            i += 1
                        else:
                            if i == 0:
                                i += 1
                                continue
                            else:
                                if self.Boxs[line][i-1] == None:
                                    self.Boxs[line][i-1] = self.Boxs[line][i]
                                    self.Boxs[line][i] = None
                                    Moved = True
                                    i = 0
                                else:
                                    i += 1
                                    
                self.update()

            elif event.key() == KeyboardKeys.KEY_RIGHT :
                # Move
                for line in range(4):
                    i = -1
                    while i >= -4:
                        if self.Boxs[line][i] == None:
                            i -= 1
                        else:
                            if i == -1:
                                i -= 1
                                continue
                            else:
                                if self.Boxs[line][i+1] == None:
                                    self.Boxs[line][i+1] = self.Boxs[line][i]
                                    self.Boxs[line][i] = None
                                    Moved = True
                                    i = -1
                                else:
                                    i -= 1

                # Sum
                for line in range(4):
                    i = 3
                    while i >= 0:
                        if self.Boxs[line][i] == None:
                            i -= 1
                        else:
                            if i == 0:
                                i -= 1
                                continue
                            else:
                                if self.Boxs[line][i-1] != None:
                                    if self.Boxs[line][i-1] == self.Boxs[line][i]:
                                        self.Boxs[line][i] = self.Boxs[line][i-1]+self.Boxs[line][i-1]
                                        self.Score += self.Boxs[line][i]
                                        self.Boxs[line][i-1] = None
                                        Moved = True
                                        i -= 2
                                    else:
                                        i -= 1
                                    
                                else:
                                    i -= 1

                # Move
                for line in range(4):
                    i = -1
                    while i >= -4:
                        if self.Boxs[line][i] == None:
                            i -= 1
                        else:
                            if i == -1:
                                i -= 1
                                continue
                            else:
                                if self.Boxs[line][i+1] == None:
                                    self.Boxs[line][i+1] = self.Boxs[line][i]
                                    self.Boxs[line][i] = None
                                    Moved = True
                                    i = -1
                                else:
                                    i -= 1
                        
                self.update()

            elif event.key() == KeyboardKeys.KEY_UP :
                # Move
                for row in range(4):
                    line = 0
                    while line < 4:
                        if self.Boxs[line][row] == None:
                            line += 1
                        else:
                            if line == 0:
                                line += 1
                                continue
                            else:
                                if self.Boxs[line-1][row] == None:
                                    self.Boxs[line-1][row] = self.Boxs[line][row]
                                    self.Boxs[line][row] = None
                                    Moved = True
                                    line = 0
                                else:
                                    line += 1
                # Sum
                for row in range(4):
                    line = 0
                    while line < 4:
                        if self.Boxs[line][row] == None:
                            line += 1
                        else:
                            if line == 3:
                                line += 1
                                continue
                            
                            if self.Boxs[line][row] == self.Boxs[line+1][row]:
                                self.Boxs[line][row] = self.Boxs[line][row] + self.Boxs[line][row]
                                self.Score += self.Boxs[line][row]
                                self.Boxs[line+1][row] = None
                                Moved = True
                                line += 2
                            else:
                                line += 1
                                
            

                # Move
                for row in range(4):
                    line = 0
                    while line < 4:
                        if self.Boxs[line][row] == None:
                            line += 1
                        else:
                            if line == 0:
                                line += 1
                                continue
                            else:
                                if self.Boxs[line-1][row] == None:
                                    self.Boxs[line-1][row] = self.Boxs[line][row]
                                    self.Boxs[line][row] = None
                                    Moved = True
                                    line = 0
                                else:
                                    line += 1

                self.update()

            elif event.key() == KeyboardKeys.KEY_DOWN :
                # Move
                for row in range(4):
                    line = 3
                    while line > -1:
                        if self.Boxs[line][row] == None:
                            line -= 1
                        else:
                            if line == 3:
                                line -= 1
                                continue
                            else:
                                if self.Boxs[line+1][row] == None:
                                    self.Boxs[line+1][row] = self.Boxs[line][row]
                                    self.Boxs[line][row] = None
                                    Moved = True
                                    line = 3
                                else:
                                    line -= 1

                # Sum
                for row in range(4):
                    line = 3
                    while line >= 0:
                        if self.Boxs[line][row] == None:
                            line -= 1
                        else:
                            if line == 0:
                                line -= 1
                                continue
                            
                            if self.Boxs[line][row] == self.Boxs[line-1][row]:
                                self.Boxs[line][row] = self.Boxs[line][row] + self.Boxs[line][row]
                                self.Score += self.Boxs[line][row]
                                self.Boxs[line-1][row] = None
                                Moved = True
                                line -= 2
                            else:
                                line -= 1
                                
                # Move
                for row in range(4):
                    line = 3
                    while line > -1:
                        if self.Boxs[line][row] == None:
                            line -= 1
                        else:
                            if line == 3:
                                line -= 1
                                continue
                            else:
                                if self.Boxs[line+1][row] == None:
                                    self.Boxs[line+1][row] = self.Boxs[line][row]
                                    self.Boxs[line][row] = None
                                    Moved = True
                                    line = 3
                                else:
                                    line -= 1
                                    
                self.update()

            if Moved:
                xy = self.GetRandomXY()
                self.Boxs[xy[1]][xy[0]] = self.GetRandomBoxValue()
            else:
                if self.CheckGame():
                    self.GameOverText.setText('Game Over!')

    def CheckGame(self):
        # Sum UP & DOWN Check
        for row in range(4):
            line = 0
            while line < 4:
                if self.Boxs[line][row] == None:
                    return False # Empty Box
                else:
                    if line == 3:
                        line += 1
                        continue
                    
                    if self.Boxs[line+1][row] == None:
                        return False # Empty Box
                    
                    if self.Boxs[line][row] == self.Boxs[line+1][row]:
                        return False # A mouvement found
                    else:
                        line += 1

        # Sum Left & Right Check
        for line in range(4):
            i = 0
            while i < 4:
                if self.Boxs[line][i] == None:
                    return False # Empty Box
                else:
                    if i == 3:
                        i += 1
                        continue
                    
                    if self.Boxs[line][i+1] == None:
                        return False # Empty Box
                    
                    if self.Boxs[line][i+1] == self.Boxs[line][i]:
                        return False # A mouvement found
                    else:
                        i += 1

        self.GameOver = True
        return True

    def RestartGame(self):
        self.Score = 0
        for line in range(4):
            for row in range(4):
                self.Boxs[line][row] = None

        xy = self.GetRandomXY()
        xy1 = self.GetRandomXY()

        self.GameOver = False
        self.GameOverText.setText('')

        self.Boxs[xy[1]][xy[0]] = self.GetRandomBoxValue()
        self.Boxs[xy1[1]][xy1[0]] = self.GetRandomBoxValue()
        self.update()
        return True

    def GetRandomXY(self):
        xy = (random.randint(0, 3), random.randint(0, 3))
        while self.Boxs[xy[1]][xy[0]] != None:
            xy = (random.randint(0, 3), random.randint(0, 3))
        return xy

    def GetRandomBoxValue(self):
        p = random.randint(1, 100)
        # 25 Per. ==> 4
        # 75 Per. ==> 2
        return 4 if p <= 25 else 2

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawSquares(qp)
        qp.end()

    def drawSquares(self, qp):
        self.GameInfo.setText('Score: '+str(self.Score))
        qp.setBrush(QtGui.QColor(187, 173, 160))
        qp.drawRect(0, 0, self.BoxSize*4+self.BtwBox*5, self.BoxSize*4+self.BtwBox*5)

        qp.setFont(self.TextFont)
        
        for line in range(4):
            for row in range(4):
                x = ( self.BtwBox * (row+1) ) + ( self.BoxSize * row )
                y = ( self.BtwBox * (line+1) ) + ( self.BoxSize * line )
                qp.setBrush(QtGui.QColor(self.Colors[self.Boxs[line][row]][0], self.Colors[self.Boxs[line][row]][1], self.Colors[self.Boxs[line][row]][2]))
                qp.setPen(QtGui.QColor(self.Colors[self.Boxs[line][row]][0], self.Colors[self.Boxs[line][row]][1], self.Colors[self.Boxs[line][row]][2]))
                qp.drawRect(x, y, self.BoxSize, self.BoxSize)

                if self.Boxs[line][row] != None:
                    qp.setPen(QtGui.QColor(255, 255, 255))
                    qp.drawText(x+self.Colors[self.Boxs[line][row]][3], y+self.Colors[self.Boxs[line][row]][4], str(self.Boxs[line][row]))
            


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Game()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
