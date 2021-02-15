import os
import math
import time
import copy
import sys
from PySide2 import QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from operator import attrgetter
from numba import njit, prange
from functools import partial
import numpy as np


os.environ["QT_MAC_WANTS_LAYER"] = "1"

Queue = []
VisitedStates = []
Directions = ["U", "D", "R", "L"]
Moves = []
cells = [[None for x in range(4)] for y in range(4)]


class AITreeThread(QThread):
    signal_end_process = Signal(object)

    def __init__(self):
        QThread.__init__(self)
        self.signal_end_process.connect(window.solve)

    def run(self):
        global Queue, Directions, VisitedStates

        root = Node()
        root.data = startState

        root.f = heuristic(root)
        Queue.append(root)
        VisitedStates.append(root.data[:])

        thisState = min(Queue, key=attrgetter('f'))

        while isGoal(thisState) != True:
            for direction in Directions:
                if isMovePossible(thisState, direction):
                    makeChild(thisState, direction)
                    
            VisitedStates.append(thisState.data[:])
            Queue.remove(thisState)
            thisState = min(Queue, key = attrgetter('f'))

        print(thisState.moves)
        print(len(Queue))

        root.moves = thisState.moves
        self.signal_end_process.emit(root)


def isGoal(state):
    if state.data == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]:
        return True
    else:
        return False


class Node(object):
    data = [[None for x in range(4)] for y in range(4)]
    f = 0
    moves = []


def inversionCount(data):
    flatBoard = [item for sublist in data for item in sublist]

    count = 0

    for i in range(16):
        for j in range(i + 1, 16):
            if flatBoard[i] > flatBoard[j] and (flatBoard[i] != 0 and flatBoard[j] != 0):
                count = count + 1

    return count


def checkSolvable(data):
    temp = dict((j, [x, y]) for x, i in enumerate(data) for y, j in enumerate(i))

    indexOfZero = temp[0]
    y = indexOfZero[0]
    x = 4 - y

    if (x % 2 == 0 and inversionCount(data) % 2 == 1) or (x % 2 == 1 and inversionCount(data) % 2 == 0):
        return True
    else:
        return False


def isMovePossible(state, direction):
    for i in range(4):
        for j in range(4):
            if state.data[i][j] == 0:
                x, y = i, j
                break

    if direction == "U":
        if x == 0 or x == 1 or x == 2:
            return True
        else:
            return False

    elif direction == "D":
        if x == 1 or x == 2 or x == 3:
            return True
        else:
            return False

    elif direction == "R":
        if y == 1 or y == 2 or y == 3:
            return True
        else:
            return False

    elif direction == "L":
        if y == 0 or y == 1 or y == 2:
            return True
        else:
            return False


def move(state, direction):
    for i in range(4):
        for j in range(4):
            if state.data[i][j] == 0:
                x, y = i, j
                break

    result = copy.deepcopy(state)

    if direction == "U":
        result.data[x][y], result.data[x+1][y] = result.data[x+1][y], result.data[x][y]

    elif direction == "D":
        result.data[x][y], result.data[x-1][y] = result.data[x-1][y], result.data[x][y]

    elif direction == "R":
        result.data[x][y], result.data[x][y-1] = result.data[x][y-1], result.data[x][y]

    elif direction == "L":
        result.data[x][y], result.data[x][y+1] = result.data[x][y+1], result.data[x][y]

    return result.data


@njit(fastmath=True, cache=True)
def correctPosition(number):
    goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    for i in range(4):
        for j in range(4):
            if goal[i][j] == number:
                return i, j


def heuristic(state):
    #ic = inversionCount(state)
    # Manhattan distance
    md = 0

    for i in range(4):
        for j in range(4):
            if state.data[i][j] == 0:
                continue
            row , col = correctPosition(state.data[i][j])
            md = md + abs(i - row) + abs(j - col)

    #return max(ic, md)
    return md


def makeChild(thisState, direction):
    global Queue, VisitedStates

    tempState = copy.deepcopy(thisState)
    tempState.data = move(thisState, direction)[:]

    if tempState.data not in VisitedStates: 
        tempState.f = heuristic(tempState)
        tempState.moves = thisState.moves[:]
        tempState.moves.append(direction)
        Queue.append(tempState)
    else:
        for s in Queue:
            if s.data == tempState.data and s.f > tempState.f:
                s.f = tempState.f + 0
                break


class Window(QWidget):
    def __init__(self):
        global cells

        super(Window, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('main.ui')

        cells[0][0] = self.ui.btn_1
        cells[0][1] = self.ui.btn_2
        cells[0][2] = self.ui.btn_3
        cells[0][3] = self.ui.btn_4
        cells[1][0] = self.ui.btn_5
        cells[1][1] = self.ui.btn_6
        cells[1][2] = self.ui.btn_7
        cells[1][3] = self.ui.btn_8
        cells[2][0] = self.ui.btn_9
        cells[2][1] = self.ui.btn_10
        cells[2][2] = self.ui.btn_11
        cells[2][3] = self.ui.btn_12
        cells[3][0] = self.ui.btn_13
        cells[3][1] = self.ui.btn_14
        cells[3][2] = self.ui.btn_15
        cells[3][3] = self.ui.btn_16

        for i in range(4):
            for j in range(4):
                cells[i][j].setText(str(startState[i][j]))
                if startState[i][j] == 0:
                    cells[i][j].setVisible(False)
                else:
                    cells[i][j].setVisible(True)

        self.ui.btn_start.clicked.connect(self.startGame)
        self.ui.progressBar.setVisible(False)

        self.ui.show()


    def solve(self, state):
        self.ui.progressBar.setVisible(False)
        QWidget.update(self)
        QApplication.processEvents()

        sw = True

        for direction in state.moves:
            temp = dict((j, [x, y]) for x, i in enumerate(state.data) for y, j in enumerate(i))

            indexOfZero = temp[0]
            x = indexOfZero[0]
            y = indexOfZero[1]

            if direction == "U":
                state.data[x][y], state.data[x + 1][y] = state.data[x + 1][y], state.data[x][y]

            elif direction == "D":
                state.data[x][y], state.data[x - 1][y] = state.data[x - 1][y], state.data[x][y]

            elif direction == "R":
                state.data[x][y], state.data[x][y - 1] = state.data[x][y - 1], state.data[x][y]

            elif direction == "L":
                state.data[x][y], state.data[x][y + 1] = state.data[x][y + 1], state.data[x][y]

            for i in range(4):
                for j in range(4):
                    cells[i][j].setText(str(state.data[i][j]))
                    if startState[i][j] == 0:
                        cells[i][j].setVisible(False)
                    else:
                        cells[i][j].setVisible(True)

            # QWidget.repaint(self)
            QWidget.update(self)
            QApplication.processEvents()
            time.sleep(0.1)

    def startGame(self):
        global ai_tree_thread
        self.ui.progressBar.setVisible(True)
        QWidget.update(self)
        
        ai_tree_thread = AITreeThread()
        ai_tree_thread.start()
        

if __name__ == '__main__':
    sw = True
    while sw:
        # startState = [[0, 1, 2, 4], [5, 6, 3, 8], [9, 10, 7, 12], [13, 14, 11, 15]]
        # startState = [[6, 13, 7, 10], [8, 9, 11, 0], [15, 2, 12, 5], [14, 3, 1, 4]]
        startState = np.random.choice(range(16), 16, replace=False).reshape(4, 4).tolist()

        if checkSolvable(startState):
            sw = False

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
