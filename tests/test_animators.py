import unittest
from unittest.mock import patch

from graphMaker.Graph import BasicDirectedGraph, WeightedGraph, AGraph, BestFirstGraph
from graphMaker.Animators.BreadthFirstGraphAnimator import BreadthFirstGraphAnimator
from graphMaker.Animators.DepthFirstGraphAnimator import DepthFirstGraphAnimator
from graphMaker.Animators.DijkstraGraphAnimator import DijkstraGraphAnimator
from graphMaker.Animators.AStarGraphAnimator import AStarGraphAnimator
from graphMaker.Animators.BestFirstGraphAnimator import BestFirstGraphAnimator
from graphMaker.Animators.OptimalGraphAnimator import OptimalGraphAnimator
from graphMaker.ENodeStateColors import ENodeStateColors


class AnimatorTestMixin:
    def patch_renderer(self):
        # Patch GraphAnimator.create_frame to avoid matplotlib/PIL work during tests
        patcher = patch('graphMaker.GraphAnimator.GraphAnimator.GraphAnimator.create_frame', autospec=True)
        mocked = patcher.start()
        # Register cleanup only if self has addCleanup (i.e., is a TestCase instance)
        if hasattr(self, 'addCleanup'):
            self.addCleanup(patcher.stop)
        mocked.side_effect = lambda self_ref, filename, highlight_line=None, memory_state=None: self_ref.frames.append(
            filename or f"frame_{self_ref.frame_id:04d}.png"
        )


class TestBreadthFirstAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_bfs_reaches_goal_and_closes_some_nodes(self):
        g = BasicDirectedGraph()
        animator = BreadthFirstGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()

        # Goal should be marked as GOAL
        self.assertEqual(animator.node_states[g.get_goal_node()], ENodeStateColors.GOAL)
        # Start should be processed and placed into closed set
        self.assertIn(g.get_start_node(), animator.closed_set)
        # Some path node should also be closed (F is on all paths to T)
        self.assertIn('F', animator.closed_set)


class TestDepthFirstAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_dfs_marks_closed_or_goal(self):
        g = BasicDirectedGraph()
        animator = DepthFirstGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()
        # At least one node should be CLOSED or GOAL
        any_closed_or_goal = any(state in (ENodeStateColors.CLOSED, ENodeStateColors.GOAL) for state in animator.node_states.values())
        self.assertTrue(any_closed_or_goal)


class TestDijkstraAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_dijkstra_finds_finite_distance_to_goal(self):
        g = WeightedGraph()
        animator = DijkstraGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()
        self.assertLess(animator.distances[g.get_goal_node()], float('inf'))
        self.assertGreaterEqual(len(animator.closed_set), 1)


class TestAStarAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_astar_reaches_goal(self):
        g = AGraph()
        animator = AStarGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()
        self.assertEqual(animator.node_states[g.get_goal_node()], ENodeStateColors.GOAL)


class TestBestFirstAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_best_first_visits_nodes(self):
        g = BestFirstGraph()
        animator = BestFirstGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()
        self.assertGreaterEqual(len(animator.visited), 1)


class TestOptimalAnimator(unittest.TestCase, AnimatorTestMixin):
    def setUp(self):
        self.patch_renderer()

    def test_optimal_progresses_and_sets_closed(self):
        g = WeightedGraph()
        animator = OptimalGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())
        animator.generate_animation()
        self.assertGreaterEqual(len(animator.visited), 1)
        self.assertTrue(any(state == ENodeStateColors.CLOSED for state in animator.node_states.values()))


if __name__ == '__main__':
    unittest.main()