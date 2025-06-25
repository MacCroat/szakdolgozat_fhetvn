from graphMaker.DepthFirstGraphAnimator import DepthFirstGraphAnimator
from graphMaker.BreadthFirstGraphAnimator import BreadthFirstGraphAnimator
from graphMaker.OptimalGraphAnimator import OptimalGraphAnimator
from graphMaker.DijkstraGraphAnimator import DijkstraGraphAnimator
from graphMaker.AStarGraphAnimator import AGraphAnimator
from graphMaker.BestFirstGraphAnimator import BestFirstGraphAnimator
from graphMaker.BacktrackGraphAnimator import BacktrackGraphAnimator
from graphMaker.Graph import BasicDirectedGraph, WeightedGraph, AGraph, BestFirstGraph, OperatorGraph


def run_search(graph, animator_class, search_type):
    animator = animator_class(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    animator.generate_animation()
    animator.save_gif(search_type=search_type)
    animator.cleanup()


if __name__ == "__main__":
    basic_graph = BasicDirectedGraph()
    weighted_graph = WeightedGraph()
    a_graph = AGraph()
    best_first_graph = BestFirstGraph()
    operator_graph = OperatorGraph()

    search_algorithms = {
        'depth_first': (DepthFirstGraphAnimator, basic_graph, 'depth_first'),
        'breadth_first': (BreadthFirstGraphAnimator, basic_graph, 'breadth_first'),
        'optimal': (OptimalGraphAnimator, weighted_graph, 'optimal'),
        'dijkstra': (DijkstraGraphAnimator, a_graph, 'dijkstra_algorithm'),
        'a_star': (AGraphAnimator, a_graph, 'a_star_algorithm'),
        'best_first': (BestFirstGraphAnimator, best_first_graph, 'best_first'),
        'backtrack': (BacktrackGraphAnimator, operator_graph, 'backtrack')
    }

    #active_search = 'depth_first'
    #active_search = 'breadth_first'
    #active_search = 'optimal'
    #active_search = 'dijkstra'
    #active_search = 'a_star'
    #active_search = 'best_first'
    active_search = 'backtrack'

    if active_search in search_algorithms:
        animator_class, graph, search_type = search_algorithms[active_search]
        run_search(graph, animator_class, search_type)