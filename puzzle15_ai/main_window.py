import os
import time
import sys
from pathlib import Path

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
import numpy as np

from .tree import Tree
from .node import Node


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


class MainWindow(QMainWindow):
    """
    high level support for doing this and that.
    """
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load(os.path.join(Path(__file__).parent.resolve(), 'main.ui'))

        while True:
            self.start_state = np.random.choice(range(16), 16, replace=False).reshape(4, 4).tolist()
            if checkSolvable(self.start_state):
                break
            
        self.cells = [[None for x in range(4)] for y in range(4)]

        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Expanding)

        for i in range(4):
            for j in range(4):
                self.cells[i][j] = QPushButton()
                self.cells[i][j].setSizePolicy(sp)
                self.cells[i][j].setStyleSheet("background-color:rgb(66,133,244); color: rgb(255, 255, 255); font-size: 32px; border-radius: 8px;")
                self.ui.gridLayout.addWidget(self.cells[i][j], i, j)
                self.cells[i][j].setText(str(self.start_state[i][j]))
                if self.start_state[i][j] == 0:
                    self.cells[i][j].setVisible(False)
                else:
                    self.cells[i][j].setVisible(True)

        self.ui.btn_start.clicked.connect(self.startGame)
        self.ui.btn_stop.clicked.connect(self.stopGame)
        self.ui.progressBar.setVisible(False)

        self.ui.show()

    def stopGame(self):
        self.tree.terminate()

    def startGame(self):
        self.ui.progressBar.setVisible(True)
        
        self.tree = Tree(self.start_state)
        self.tree.signal_end_process.connect(self.solve)
        self.tree.start()

    def solve(self, state):
        self.ui.progressBar.setVisible(False)
        QWidget.update(self)
        QApplication.processEvents()

        for direction in state.moves:
            state.zero_pos = Node.findZeroPos(state.data)
            state.move(direction)

            for i in range(4):
                for j in range(4):
                    self.cells[i][j].setText(str(state.data[i][j]))
                    if self.start_state[i][j] == 0:
                        self.cells[i][j].setVisible(False)
                    else:
                        self.cells[i][j].setVisible(True)

            QWidget.update(self)
            QApplication.processEvents()
            time.sleep(0.2)
        

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
