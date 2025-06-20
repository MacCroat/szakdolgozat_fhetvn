from graphMaker.DepthFirstGraphAnimator import DepthFirstGraphAnimator
from graphMaker.BreadthFirstGraphAnimator import BreadthFirstGraphAnimator
from graphMaker.OptimalGraphAnimator import OptimalGraphAnimator
from graphMaker.DijkstraGraphAnimator import DijkstraGraphAnimator
from graphMaker.AStarGraphAnimator import AGraphAnimator
from graphMaker.BestFirstGraphAnimator import BestFirstGraphAnimator
from graphMaker.Graph import BasicDirectedGraph, WeightedGraph, AGraph, BestFirstGraph


def run_depth_first_search(graph):
    dfs_animator = DepthFirstGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    dfs_animator.generate_animation()
    dfs_animator.save_gif(search_type='depth_first')
    dfs_animator.cleanup()


def run_breadth_first_search(graph):
    bfs_animator = BreadthFirstGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    bfs_animator.generate_animation()
    bfs_animator.save_gif(search_type='breadth_first')
    bfs_animator.cleanup()


def run_optimal_search(graph):
    optimal_animator = OptimalGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    optimal_animator.generate_animation()
    optimal_animator.save_gif(search_type='optimal')
    optimal_animator.cleanup()


def run_dijkstra_search(graph):
    dijkstra_animator = DijkstraGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    dijkstra_animator.generate_animation()
    dijkstra_animator.save_gif(search_type='dijkstra_algorithm')
    dijkstra_animator.cleanup()


def run_a_star_search(graph):
    a_star_animator = AGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    a_star_animator.generate_animation()
    a_star_animator.save_gif(search_type='a_star_algorithm')
    a_star_animator.cleanup()

def run_best_first_search(graph):
    best_first_animator = BestFirstGraphAnimator(
        graph,
        graph.get_start_node(),
        graph.get_goal_node(),
        graph.get_children()
    )
    best_first_animator.generate_animation()
    best_first_animator.save_gif(search_type='best_first')
    best_first_animator.cleanup()


if __name__ == "__main__":
    basic_graph = BasicDirectedGraph()
    weighted_graph = WeightedGraph()
    best_first_graph = BestFirstGraph()

    #run_depth_first_search(basic_graph)
    #run_breadth_first_search(basic_graph)
    #run_optimal_search(weighted_graph)
    #run_dijkstra_search(a_graph)
    #run_a_star_search(a_graph)
    run_best_first_search(best_first_graph)