import os
import tempfile
import shutil
import unittest
from unittest.mock import patch

from graphMaker.Graph import BasicDirectedGraph
from graphMaker.Animators.BreadthFirstGraphAnimator import BreadthFirstGraphAnimator
from graphMaker.GraphAnimator.FrameRenderer import FrameRenderer

try:
    from PIL import Image
except Exception:
    Image = None


def _render_stub(self, graph, pos, node_states, pseudocode, frame_id, highlight_line=None, memory_state=None):
    frames_dir = getattr(self, 'frames_dir', 'graph_frames')
    os.makedirs(frames_dir, exist_ok=True)
    path = os.path.join(frames_dir, f"frame_{frame_id:04d}.png")
    Image.new('RGB', (4, 4), 'white').save(path, 'PNG')
    return path


@unittest.skipIf(Image is None, 'Pillow not available')
class TestAnimatorGifEdgeCases(unittest.TestCase):
    def setUp(self):
        self._orig_cwd = os.getcwd()
        self._tmpdir = tempfile.mkdtemp(prefix='graph_anim_edge_')
        os.chdir(self._tmpdir)

    def tearDown(self):
        os.chdir(self._orig_cwd)
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _animator(self):
        g = BasicDirectedGraph()
        return BreadthFirstGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())

    def test_save_gif_raises_when_no_frames_anywhere(self):
        animator = self._animator()
        with self.assertRaises(RuntimeError):
            animator.save_gif('empty.gif')

    def test_save_gif_populates_exporter_when_only_animator_frames_have_entries(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._animator()
            animator.generate_frame()
            animator.exporter.frames.clear()
            self.assertEqual(len(animator.exporter.frames), 0)
            gif_path = animator.save_gif('recover.gif')
            self.assertTrue(os.path.isfile(gif_path))
            self.assertGreater(len(animator.exporter.frames), 0)

    def test_save_gif_strips_and_adds_extension(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._animator()
            for _ in range(2):
                animator.generate_frame()
            gif_path = animator.save_gif('  spaced_name  ')
            expected = os.path.join('animated_graphs', 'spaced_name.gif')
            self.assertEqual(os.path.normpath(gif_path), os.path.normpath(expected))
            self.assertTrue(os.path.isfile(gif_path))

    def test_highlight_pseudocode_lines_generates_frames(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._animator()
            initial_id = animator.frame_id
            animator.highlight_pseudocode_lines(range(3))
            self.assertEqual(animator.frame_id, initial_id + 3)
            self.assertEqual(len(animator.frames), 3)

if __name__ == '__main__':
    unittest.main()

