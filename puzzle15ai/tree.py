import copy
from operator import attrgetter
from PySide6.QtCore import QThread, Signal
from .node import Node


class Tree(QThread):
    """
    high level support for doing this and that.
    """
    signal_end_process = Signal(object)
    
    def __init__(self, start_state):
        QThread.__init__(self)
        self.VisitedStates = []
        self.root = Node(start_state)
        self.Queue = [self.root]

    def run(self):
        self.VisitedStates.append(self.root.data[:])

        this_state = self.root
        while not self.isGoal(this_state):
            for direction in ["U", "D", "R", "L"]:
                if self.isMovePossible(this_state, direction):
                    child_state = self.makeChild(this_state, direction)
                    if child_state:
                        self.Queue.append(child_state)

            self.VisitedStates.append(this_state.data[:])
            self.Queue.remove(this_state)
            this_state = min(self.Queue, key = attrgetter('f'))

        print(this_state.moves)
        print(len(self.Queue))
        self.root.moves = this_state.moves
        self.signal_end_process.emit(self.root)

    def makeChild(self, parent_state, direction):
        child_state = Node(copy.deepcopy(parent_state.data))
        child_state.move(direction)

        if child_state.data not in self.VisitedStates:
            child_state.moves = parent_state.moves[:]
            child_state.moves.append(direction)
            return child_state
        else:
            for s in self.Queue:
                if s.data == child_state.data and s.f > child_state.f:
                    s.f = child_state.f
                    return None

    def isGoal(self, state):
        if state.data == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]:
            return True
        else:
            return False

    def isMovePossible(self, state, direction):
        x, y = state.zero_pos

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
