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

from PyQt4 import QtCore
from PyQt4 import QtGui

from collections import deque

import window
from dot import Dot

class Direction:
    Up = (0,-1)
    Down = (0,1)
    Left = (-1,0)
    Right = (1,0)

class Snake(QtCore.QObject):
    def __init__(self, snakeWindow):
        QtCore.QObject.__init__(self, snakeWindow)
        self.window = snakeWindow
        self.length = 1
        self.direction = Direction.Down
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move)
        self.timer.start(200)

        self.nodes = deque()
        self.nodes.appendleft(Dot(self.window, (self.window.size[0]/2, self.window.size[1]/2)))

    def __del__(self):
        for node in self.nodes:
            node.deleteLater()

    def occupiesPosition(self, position):
        for node in self.nodes:
            if(node.position == position):
                return True
        return False

    def move(self):
        position = (self.nodes[0].position[0] + self.direction[0],
                    self.nodes[0].position[1] + self.direction[1])
        if(position[0] > self.window.size[0] or
           position[1] > self.window.size[1] or
           position[0] < 0 or
           position[1] < 0 or
           self.occupiesPosition(position)):
            self.window.killSnake()
        else:
            if(position == self.window.dot.position):
                self.length += 1
                self.window.createDot()
            self.nodes.appendleft(Dot(self.window, position))
            if(len(self.nodes) > self.length):
                self.nodes.pop().deleteLater()

    def setDirection(self, direction):
        if(direction != None):
            self.direction = direction
