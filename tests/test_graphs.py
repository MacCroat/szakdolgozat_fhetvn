import unittest

from graphMaker.Graph import (
    BasicDirectedGraph,
    WeightedGraph,
    AGraph,
    BestFirstGraph,
    OperatorGraph,
)


class TestGraphs(unittest.TestCase):
    def test_basic_directed_graph_nodes_and_edges(self):
        g = BasicDirectedGraph()
        G = g.create_graph()

        self.assertEqual(set(G.nodes()), set(g.get_pos().keys()))

        expected_edges = {('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('B', 'C'), ('D', 'F'), ('E', 'F'), ('F', 'T')}
        self.assertTrue(expected_edges.issubset(set(G.edges())))

        self.assertEqual(g.get_start_node(), 'A')
        self.assertEqual(g.get_goal_node(), 'T')

    def test_weighted_graph_weights(self):
        g = WeightedGraph()
        G = g.create_graph()

        self.assertEqual(G.get_edge_data('A', 'B').get('weight'), 1)
        self.assertEqual(G.get_edge_data('A', 'C').get('weight'), 2)
        self.assertEqual(G.get_edge_data('B', 'D').get('weight'), 2)
        self.assertEqual(G.get_edge_data('D', 'F').get('weight'), 8)
        self.assertEqual(G.get_edge_data('F', 'T').get('weight'), 1)

    def test_a_graph_heuristic_and_edges(self):
        g = AGraph()
        G = g.create_graph()
        h = g.get_heuristic()

        self.assertIn('A', h)
        self.assertIn('T', h)
        self.assertEqual(h['A'], 6)
        self.assertEqual(h['T'], 0)

        self.assertEqual(G.get_edge_data('A', 'B').get('weight'), 1)
        self.assertEqual(G.get_edge_data('G', 'T').get('weight'), 1)

    def test_best_first_graph_has_heuristic(self):
        g = BestFirstGraph()
        h = g.get_heuristic()
        self.assertIsInstance(h, dict)
        self.assertIn('A', h)
        self.assertIn('T', h)

    def test_operator_graph_edge_operators(self):
        g = OperatorGraph()
        G = g.create_graph()
        ops = g.get_edge_operators()

        for (u, v), op in ops.items():
            self.assertIn((u, v), G.edges())
            self.assertEqual(G.get_edge_data(u, v).get('operator'), op)


if __name__ == '__main__':
    unittest.main()

