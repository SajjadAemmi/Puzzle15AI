import time
import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
import numpy as np

from .ui_mainwindow import Ui_MainWindow
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


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window class of the app
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

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
                self.gridLayout.addWidget(self.cells[i][j], i, j)
                self.cells[i][j].setText(str(self.start_state[i][j]))
                if self.start_state[i][j] == 0:
                    self.cells[i][j].setVisible(False)
                else:
                    self.cells[i][j].setVisible(True)

        self.btn_start.clicked.connect(self.startGame)        
        self.btn_stop.clicked.connect(self.stopGame)
        self.progressBar.setVisible(False)

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        event.accept()

    def stopGame(self):
        self.tree.terminate()

    def startGame(self):
        self.progressBar.setVisible(True)
        self.tree = Tree(self.start_state)
        self.tree.signal_end_process.connect(self.solve)
        self.tree.start()

    def solve(self, state):
        self.progressBar.setVisible(False)
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
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
