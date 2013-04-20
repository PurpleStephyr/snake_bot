# Copyright 2013 Steph Kraemer.
# This file is part of SnakeBot.

# SnakeBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SnakeBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SnakeBot.  If not, see <http://www.gnu.org/licenses/>.

import random

from PyQt4 import QtGui
from PyQt4 import QtCore

import snake
from dot import Dot

PIXELS_PER_SQUARE = 12

class SnakeWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.size = (25,25)
        self.resize(self.size[0]*PIXELS_PER_SQUARE,self.size[1]*PIXELS_PER_SQUARE)
        self.startButton = QtGui.QPushButton('Start', self)
        self.startButton.clicked.connect(self.startGame)
        self.startButton.move(self.width()/2 - self.startButton.width()/2,
                              self.height()/2 - self.startButton.height()/2)
        self.show()

    def startGame(self):
        self.startButton.hide()
        self.grabKeyboard()
        self.snake = snake.Snake(self)
        self.dot = None
        self.createDot()

    def killSnake(self):
        self.snake.deleteLater()
        self.snake = None
        self.dot.deleteLater()
        self.dot = None
        self.startButton.show()

    def keyPressEvent(self, keyEvent):
        if(self.snake != None and keyEvent.type() == QtCore.QEvent.KeyPress):
            self.snake.setDirection( {
                    QtCore.Qt.Key_Up : snake.Direction.Up,
                    QtCore.Qt.Key_Down : snake.Direction.Down,
                    QtCore.Qt.Key_Left : snake.Direction.Left,
                    QtCore.Qt.Key_Right : snake.Direction.Right }.get(keyEvent.key(), None) )

    def createDot(self):
        unoccupiedSpaces = []
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if(not self.snake.occupiesPosition((x,y))):
                    unoccupiedSpaces.append((x,y))

        if(self.dot != None):
            self.dot.deleteLater()
        if(len(unoccupiedSpaces) == 0):
            self.dot = None
        else:
            self.dot = Dot(self, unoccupiedSpaces[random.randint(0, len(unoccupiedSpaces)-1)])
