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
import random

import window
from dot import Dot

class Direction:
    Up = (0,-1)
    Down = (0,1)
    Left = (-1,0)
    Right = (1,0)
    List = [Up, Down, Left, Right]


def addDirections(d1, d2):
    return (d1[0] + d2[0], d1[1] + d2[1])

class Snake(QtCore.QObject):
    def __init__(self, snakeWindow):
        QtCore.QObject.__init__(self, snakeWindow)
        self.window = snakeWindow
        self.length = 1
        self.direction = Direction.Down
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move)
        self.timer.start(200)

        self.occupiedSpaces = [[False for j in xrange(0, self.window.size[1])]
                               for i in xrange(0, self.window.size[1])]
        self.nodes = deque()
        self.nodes.appendleft(Dot(self.window, (self.window.size[0]/2, self.window.size[1]/2)))

        self.occupiedSpaces[self.nodes[0].position[0]][self.nodes[0].position[1]] = True

        for x in xrange(len(self.occupiedSpaces)):
            for y in xrange(len(self.occupiedSpaces[0])):
                if(self.occupiedSpaces[x][y]):
                    print(x,y)
                

    def __del__(self):
        for node in self.nodes:
            node.deleteLater()

    def validPosition(self, position):
        if(position[0] >= self.window.size[0] or
           position[1] >= self.window.size[1] or
           position[0] < 0 or
           position[1] < 0):
            return False

        return not self.occupiedSpaces[position[0]][position[1]]

    def move(self):
        position = addDirections(self.nodes[0].position, self.direction)
        if(not self.validPosition(position)):
            self.window.killSnake()
        else:
            if(position == self.window.dot.position):
                self.length += 1
                self.window.createDot()

            self.nodes.appendleft(Dot(self.window, position))
            self.occupiedSpaces[self.nodes[0].position[0]][self.nodes[0].position[1]] = True

            if(len(self.nodes) > self.length):
                lastNode = self.nodes.pop()
                self.occupiedSpaces[lastNode.position[0]][lastNode.position[1]] = False
                lastNode.deleteLater()

        if(window.KEYBOARD == False):
            self.computeNextDirection()

    def setDirection(self, direction):
        if(direction == Direction.Up or
           direction == Direction.Down or
           direction == Direction.Left or
           direction == Direction.Right):
            self.direction = direction

    def computeNextDirection(self):
        validDirections = []
        for direction in Direction.List:
            if(self.validPosition(addDirections(self.nodes[0].position, direction))):
                validDirections.append(direction)

        minDistance = float("inf")
        shortestDirection = None
        for direction in validDirections:
            position = addDirections(self.nodes[0].position, direction)
            distance = abs(position[0] - self.window.dot.position[0]) + \
                abs(position[1] - self.window.dot.position[1])
            if(distance < minDistance):
                minDistance = distance
                shortestDirection = direction
        self.setDirection(shortestDirection)
