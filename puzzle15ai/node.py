correctPosition = {}
goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
for i in range(4):
    for j in range(4):
        correctPosition[goal[i][j]] = [i, j]


class Node(object):
    """
    high level support for doing this and that.
    """
    def __init__(self, data):
        self.data = data
        self.f = Node.heuristic(data)
        self.moves = []
        self.zero_pos = Node.findZeroPos(data)
    
    def move(self, direction):
        x, y = self.zero_pos

        if direction == "U":
            self.data[x][y], self.data[x+1][y] = self.data[x+1][y], self.data[x][y]

        elif direction == "D":
            self.data[x][y], self.data[x-1][y] = self.data[x-1][y], self.data[x][y]

        elif direction == "R":
            self.data[x][y], self.data[x][y-1] = self.data[x][y-1], self.data[x][y]

        elif direction == "L":
            self.data[x][y], self.data[x][y+1] = self.data[x][y+1], self.data[x][y]

        self.zero_pos = Node.findZeroPos(self.data)

    @staticmethod
    def findZeroPos(data):
        for i in range(4):
            for j in range(4):
                if data[i][j] == 0:
                    return [i, j]

    @staticmethod
    def heuristic(data):
        """
        high level support for doing this and that.
        """
        #ic = inversionCount(state)
        # Manhattan distance
        md = 0
        for i in range(4):
            for j in range(4):
                if data[i][j] == 0:
                    continue
                row , col = correctPosition[data[i][j]]
                md = md + abs(i - row) + abs(j - col)

        #return max(ic, md)
        return md
    