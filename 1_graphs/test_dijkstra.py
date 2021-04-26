import unittest
from classes_and_functions import DiGraph, UndirectedGraph, dijkstra

class DijkstraTests(unittest.TestCase):

    def test_basic_undirected(self):
        g = UndirectedGraph()

        g.add_node('a')
        g.add_node('b')
        g.add_node('c')
        g.add_node('d')
        g.add_distance('a','b',4)
        g.add_distance('a','c',3)
        g.add_distance('d','c',7)
        g.add_distance('b','d',5)
        best = dijkstra(g, 'a', 'd')
        self.assertEqual(best[0], ['a', 'b', 'd'])
        self.assertEqual(best[1]['d'], 9)

    def test_basic_directed(self):
        g = DiGraph()
        g.add_node('a')
        g.add_node('b')
        g.add_node('c')
        g.add_node('d')
        g.add_distance('b','a',4)
        g.add_distance('a','c',3)
        g.add_distance('c','d',7)
        g.add_distance('b','d',5)

        best = dijkstra(g, 'a', 'd')
        self.assertEqual(best[0], ['a', 'c', 'd'])
        self.assertEqual(best[1]['d'], 10)

    def test_not_connected_directed(self):
        g = DiGraph()
        g.add_node('a')
        g.add_node('b')
        best = dijkstra(g, 'a', 'b')
        self.assertEqual(best, 'origin and destiny not connected')
       

    def test_diff_order_directed(self):
        g = DiGraph()
        g.add_node('a')
        g.add_node('b')
        g.add_distance('b','a',4)
        best = dijkstra(g, 'a', 'b')
        self.assertEqual(best, 'origin and destiny not connected')




if __name__ == '__main__':
    unittest.main()

