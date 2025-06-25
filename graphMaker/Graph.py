from abc import ABC, abstractmethod

import networkx as nx


class Graph(ABC):

    @abstractmethod
    def create_graph(self):
        pass

    @abstractmethod
    def get_pos(self):
        pass

    @abstractmethod
    def get_children(self):
        pass

    @property
    def graph_type(self):
        return self.__class__.__name__


class BasicDirectedGraph(Graph):
    def __init__(self):
        self.pos = {
            'A': (0.5, 1),
            'B': (0.4, 0.7),
            'C': (0.6, 0.7),
            'D': (0.3, 0.4),
            'E': (0.5, 0.4),
            'F': (0.4, 0.2),
            'T': (0.4, 0)
        }

        self.children = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': ['T'],
            'T': []
        }

        self.start_node = 'A'
        self.goal_node = 'T'

    def create_graph(self):
        G = nx.DiGraph()

        for node in self.pos:
            G.add_node(node)

        edges = [
            ('A', 'B'), ('A', 'C'),
            ('B', 'D'), ('B', 'E'),
            ('B', 'C'),
            ('D', 'F'), ('E', 'F'),
            ('F', 'T')
        ]
        for u, v in edges:
            G.add_edge(u, v)

        return G

    def get_pos(self):
        return self.pos

    def get_children(self):
        return self.children

    def get_start_node(self):
        return self.start_node

    def get_goal_node(self):
        return self.goal_node



class WeightedGraph(Graph):
    def __init__(self):
        self.pos = {
            'A': (0.5, 1),
            'B': (0.4, 0.7),
            'C': (0.6, 0.7),
            'D': (0.3, 0.4),
            'E': (0.5, 0.4),
            'F': (0.4, 0.2),
            'T': (0.4, 0)
        }

        self.children = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': ['T'],
            'T': []
        }

        self.start_node = 'A'
        self.goal_node = 'T'

    def create_graph(self):
        G = nx.DiGraph()

        for node in self.pos:
            G.add_node(node)

        edges = [
            ('A', 'B', 1), ('A', 'C', 2),
            ('B', 'D', 2), ('B', 'E', 4),
            ('B', 'C', 3),
            ('D', 'F', 8), ('E', 'F', 4),
            ('F', 'T', 1)
        ]

        for u, v, w in edges:
            G.add_edge(u, v, weight=w)

        return G

    def get_pos(self):
        return self.pos

    def get_children(self):
        return self.children

    def get_start_node(self):
        return self.start_node

    def get_goal_node(self):
        return self.goal_node


class AGraph(WeightedGraph):
    def __init__(self):
        self.pos = {
            'A': (0.5, 1),
            'B': (0.4, 0.7),
            'C': (0.6, 0.7),
            'D': (0.3, 0.4),
            'E': (0.5, 0.4),
            'F': (0.4, 0.3),
            'G': (0.3, 0.2),
            'H': (0.5, 0.2),
            'T': (0.4, 0.1)
        }

        self.children = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['A'],
            'D': ['F', 'G'],
            'E': [],
            'F': ['G', 'H'],
            'G': ['T'],
            'H': ['T'],
            'T': []
        }

        self.start_node = 'A'
        self.goal_node = 'T'

        self.heuristic = {
            'A': 6,
            'B': 5,
            'C': 6,
            'D': 3,
            'E': 7,
            'F': 2,
            'G': 1,
            'H': 2,
            'T': 0
        }

    def create_graph(self):
        G = nx.DiGraph()

        for node in self.pos:
            G.add_node(node)

        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 2),
            ('B', 'D', 3), ('B', 'E', 2),
            ('D', 'F', 4), ('D', 'G', 2), ('E', 'F', 6),
            ('F', 'G', 1), ('F', 'H', 1),
            ('G', 'T', 1), ('H', 'T', 2)
        ]

        for u, v, w in edges:
            G.add_edge(u, v, weight=w)

        return G

    def get_pos(self):
        return self.pos

    def get_children(self):
        return self.children

    def get_start_node(self):
        return self.start_node

    def get_goal_node(self):
        return self.goal_node

    def get_heuristic(self):
        return self.heuristic


class BestFirstGraph(Graph):
    def __init__(self):
        self.pos = {
            'A': (0.5, 1),
            'B': (0.4, 0.7),
            'C': (0.6, 0.7),
            'D': (0.3, 0.4),
            'E': (0.5, 0.4),
            'F': (0.4, 0.2),
            'T': (0.4, 0)
        }

        self.children = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': ['T'],
            'T': []
        }

        self.start_node = 'A'
        self.goal_node = 'T'

        self.heuristic = {
            'A': 4,
            'B': 3,
            'C': 2,
            'D': 2,
            'E': 1,
            'F': 1,
            'T': 0
        }

    def create_graph(self):
        G = nx.DiGraph()

        for node in self.pos:
            G.add_node(node)

        edges = [
            ('A', 'B'), ('A', 'C'),
            ('B', 'D'), ('B', 'E'),
            ('C', 'E'),
            ('D', 'F'), ('E', 'F'),
            ('F', 'T')
        ]
        for u, v in edges:
            G.add_edge(u, v)

        return G

    def get_pos(self):
        return self.pos

    def get_children(self):
        return self.children

    def get_start_node(self):
        return self.start_node

    def get_goal_node(self):
        return self.goal_node

    def get_heuristic(self):
        return self.heuristic


class OperatorGraph(Graph):
    def __init__(self):
        self.pos = {
            'A': (0.5, 1),
            'B': (0.4, 0.7),
            'C': (0.6, 0.7),
            'D': (0.3, 0.4),
            'E': (0.5, 0.4),
            'F': (0.4, 0.2),
            'T': (0.4, 0)
        }

        self.children = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': ['T'],
            'T': []
        }

        self.edge_operators = {
            ('A', 'B'): 'o1',
            ('B', 'C'): 'o1',
            ('C', 'A'): 'o2',
            ('B', 'D'): 'o3',
            ('B', 'E'): 'o2',
            ('D', 'F'): 'o2',
            ('E', 'F'): 'o1',
            ('F', 'T'): 'o3',
        }

        self.start_node = 'A'
        self.goal_node = 'T'

    def create_graph(self):
        G = nx.DiGraph()

        for node in self.pos:
            G.add_node(node)

        for edge, operator in self.edge_operators.items():
            u, v = edge
            G.add_edge(u, v, operator=operator)

        return G

    def get_pos(self):
        return self.pos

    def get_children(self):
        return self.children

    def get_start_node(self):
        return self.start_node

    def get_goal_node(self):
        return self.goal_node

    def get_edge_operators(self):
        return self.edge_operators