from DepthFirstGraphAnimator import DepthFirstGraphAnimator
from BreadthFirstGraphAnimator import BreadthFirstGraphAnimator

if __name__ == "__main__":
    start_node = '0'
    goal_node = 'T'
    children = {
        '0': ['1', '2a'],
        '1': ['2b', '2c'],
        '2a': ['2c'],
        '2b': ['3'],
        '2c': ['3'],
        '3': ['T'],
        'T': []
    }

    dfs_animator = DepthFirstGraphAnimator(start_node, goal_node, children)
    dfs_animator.generate_animation()
    dfs_animator.save_gif(search_type='depth_first')
    dfs_animator.cleanup()

    bfs_animator = BreadthFirstGraphAnimator(start_node, goal_node, children)
    bfs_animator.generate_animation()
    bfs_animator.save_gif(search_type='breadth_first')
    bfs_animator.cleanup()
