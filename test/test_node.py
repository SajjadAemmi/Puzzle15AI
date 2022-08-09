import unittest
from puzzle15_ai.node import Node
from puzzle15_ai.tree import Tree


class TestNode(unittest.TestCase):
    """
    high level support for doing this and that.
    """
    def test_heuristic(self):
        data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        node = Node(data=data)
        self.assertEqual(node.heuristic(data), 0, "Should be 0")

    def test_is_goal(self):
        data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        node = Node(data=data)
        tree = Tree(start_state=data)
        self.assertEqual(tree.isGoal(node), True, "Should be True")


if __name__ == '__main__':
    unittest.main()
