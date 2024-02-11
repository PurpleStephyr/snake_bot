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

from PyQt4 import QtGui
from PyQt4 import QtCore

import window

class Dot(QtGui.QWidget):
    def __init__(self,parent, position):
        QtGui.QWidget.__init__(self,parent)
        self.position = position
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.setGeometry(self.position[0]*window.PIXELS_PER_SQUARE,
                         self.position[1]*window.PIXELS_PER_SQUARE,
                         window.PIXELS_PER_SQUARE,
                         window.PIXELS_PER_SQUARE)
        self.show()
