from abc import ABC, abstractmethod
import os
from typing import Any, Dict, Optional
from graphMaker.ENodeStateColors import ENodeStateColors
from graphMaker.GraphAnimator.FrameRenderer import FrameRenderer
from graphMaker.GraphAnimator.FrameExporter import FrameExporter

class GraphAnimator(ABC):
    def __init__(self, graph, pseudocode, start_node, goal_node, children):
        self.graph_provider = graph
        self.graph = graph.create_graph()
        self.pos = graph.get_pos()

        self.pseudocode = pseudocode
        self.start_node = start_node
        self.goal_node = goal_node
        self.children = children

        self.frames_dir = 'graph_frames'
        os.makedirs(self.frames_dir, exist_ok=True)

        self.frames = []
        self.node_states = {node: ENodeStateColors.UNVISITED for node in self.graph.nodes()}
        self.visited = set()
        self.frame_id = 0

        self.closed_set = set()

        self.collection_renderer = self.create_collection_renderer()
        self.renderer = FrameRenderer(frames_dir=self.frames_dir, collection_renderer=self.collection_renderer)
        self.exporter = FrameExporter(frames_dir=self.frames_dir)

    @abstractmethod
    def create_collection_renderer(self):
        pass

    @abstractmethod
    def generate_animation(self):
        pass

    def highlight_pseudocode_lines(self, lines):
        for line in lines:
            self.generate_frame(line)

    def generate_frame(self, highlight_line: Optional[int] = None, collection_items: Optional[Any] = None):
        frame_filename = f"{self.frames_dir}/frame_{self.frame_id:04d}.png"
        memory_state = self.prepare_memory_state(collection_items)
        self.create_frame(frame_filename, highlight_line, memory_state)
        self.frame_id += 1
        return frame_filename

    def prepare_memory_state(self, collection_items: Optional[Any]) -> Optional[Dict[str, Any]]:
        if collection_items is None:
            return None
        return {"Nyílt": collection_items}

    def create_frame(self, filename, highlight_line=None, memory_state=None):
        path = self.renderer.render(
            graph=self.graph,
            pos=self.pos,
            node_states=self.node_states,
            pseudocode=self.pseudocode,
            frame_id=self.frame_id,
            highlight_line=highlight_line,
            memory_state=memory_state
        )
        self.frames.append(path)
        self.exporter.add_frame(path)

    def save_gif(self, search_type: str = ''):
        if not self.exporter.frames and self.frames:
            for f in self.frames:
                self.exporter.add_frame(f)

        base = (search_type or "animation").strip()
        gif_name = base if base.lower().endswith(".gif") else f"{base}.gif"
        return self.exporter.save_gif(gif_name)

    def cleanup(self):
        try:
            self.exporter.cleanup()
        except Exception as e:
            print(f"Failed to remove directory. Reason: {e}")