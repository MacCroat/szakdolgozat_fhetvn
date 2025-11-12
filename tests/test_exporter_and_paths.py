import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from graphMaker.Graph import BasicDirectedGraph
from graphMaker.Animators.BreadthFirstGraphAnimator import BreadthFirstGraphAnimator
from graphMaker.GraphAnimator.FrameRenderer import FrameRenderer
from graphMaker.GraphAnimator.FrameExporter import FrameExporter

try:
    from PIL import Image
except Exception:
    Image = None


def _render_stub(self, graph, pos, node_states, pseudocode, frame_id, highlight_line=None, memory_state=None):
    frames_dir = getattr(self, 'frames_dir', 'graph_frames')
    os.makedirs(frames_dir, exist_ok=True)
    fname = os.path.join(frames_dir, f"frame_{frame_id:04d}.png")
    img = Image.new('RGB', (8, 8), color='white')
    img.save(fname, format='PNG')
    return fname


class TestExporterAndPaths(unittest.TestCase):
    def setUp(self):
        self._orig_cwd = os.getcwd()
        self._tmpdir = tempfile.mkdtemp(prefix="graph_anim_test_")
        os.chdir(self._tmpdir)

    def tearDown(self):
        os.chdir(self._orig_cwd)
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _make_animator(self):
        g = BasicDirectedGraph()
        return BreadthFirstGraphAnimator(g, g.get_start_node(), g.get_goal_node(), g.get_children())

    @unittest.skipIf(Image is None, "Pillow not available")
    def test_generate_frame_creates_file_in_graph_frames(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._make_animator()
            path = animator.generate_frame()

            self.assertTrue(os.path.isfile(path))
            self.assertEqual(os.path.normpath(os.path.dirname(path)), os.path.normpath('graph_frames'))
            self.assertTrue(os.path.basename(path).startswith('frame_'))
            self.assertTrue(os.path.basename(path).endswith('.png'))

            norm_path = os.path.normpath(path)
            self.assertTrue(any(os.path.normpath(p) == norm_path for p in animator.frames))
            self.assertTrue(any(os.path.normpath(p) == norm_path for p in animator.exporter.frames))

    @unittest.skipIf(Image is None, "Pillow not available")
    def test_save_gif_creates_gif_in_animated_graphs(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._make_animator()
            for _ in range(3):
                animator.generate_frame()

            gif_path = animator.save_gif('breadth_first_graph_animation')

            expected = os.path.join('animated_graphs', 'breadth_first_graph_animation.gif')
            self.assertEqual(os.path.normpath(gif_path), os.path.normpath(expected))
            self.assertTrue(os.path.isfile(gif_path))

            for f in animator.frames:
                self.assertEqual(os.path.normpath(os.path.dirname(f)), os.path.normpath('graph_frames'))
                self.assertTrue(os.path.isfile(f))

    @unittest.skipIf(Image is None, "Pillow not available")
    def test_save_gif_respects_explicit_extension(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._make_animator()
            for _ in range(2):
                animator.generate_frame()
            gif_path = animator.save_gif('custom.gif')
            expected = os.path.join('animated_graphs', 'custom.gif')
            self.assertEqual(os.path.normpath(gif_path), os.path.normpath(expected))
            self.assertTrue(os.path.isfile(gif_path))

    @unittest.skipIf(Image is None, "Pillow not available")
    def test_save_gif_default_name_when_not_provided(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._make_animator()
            for _ in range(2):
                animator.generate_frame()
            gif_path = animator.save_gif()  # use default
            expected = os.path.join('animated_graphs', 'animation.gif')
            self.assertEqual(os.path.normpath(gif_path), os.path.normpath(expected))
            self.assertTrue(os.path.isfile(gif_path))

    @unittest.skipIf(Image is None, "Pillow not available")
    def test_cleanup_removes_frames_dir_but_keeps_gifs(self):
        with patch.object(FrameRenderer, 'render', new=_render_stub):
            animator = self._make_animator()
            for _ in range(2):
                animator.generate_frame()
            gif_path = animator.save_gif('bfs.gif')
            self.assertTrue(os.path.isfile(gif_path))

            animator.cleanup()
            self.assertFalse(os.path.exists('graph_frames'))
            self.assertTrue(os.path.isdir('animated_graphs'))
            self.assertTrue(os.path.isfile(gif_path))

    def test_frame_exporter_raises_without_frames(self):
        exporter = FrameExporter(frames_dir='tmp_frames', out_dir='tmp_gifs')
        with self.assertRaises(RuntimeError):
            exporter.save_gif('x.gif')


if __name__ == '__main__':
    unittest.main()
