from abc import ABC, abstractmethod
import networkx as nx
import matplotlib.pyplot as plt
import os
from PIL import Image


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
        self.frames = []
        self.node_states = {node: 'yellow' for node in self.graph.nodes()}
        self.visited = set()
        self.frame_id = 0

        self.open_collection = []
        self.open_set = set()
        self.closed_set = set()

        self.distances = {node: float('inf') for node in self.graph.nodes()}
        self.g_values = {node: float('inf') for node in self.graph.nodes()}
        self.f_values = {node: float('inf') for node in self.graph.nodes()}
        self.predecessors = {node: None for node in self.graph.nodes()}
        self.heuristic = self.initialize_heuristic()

        self.g_values[start_node] = 0
        self.distances[start_node] = 0
        self.f_values[start_node] = self.heuristic.get(start_node, 0)

        self.collection_renderer = self.create_collection_renderer()

        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)

    def initialize_heuristic(self):
        if hasattr(self.graph_provider, 'get_heuristic'):
            return self.graph_provider.get_heuristic()
        return {node: 0 for node in self.graph.nodes()}

    @abstractmethod
    def create_collection_renderer(self):
        pass

    @abstractmethod
    def generate_animation(self):
        pass

    def highlight_pseudocode_lines(self, lines):
        for line in lines:
            self.generate_frame(line)
            self.frame_id += 1

    def generate_frame(self, highlight_line=None, collection_items=None):
        frame_filename = f"{self.frames_dir}/frame_{self.frame_id:04d}.png"
        memory_state = self.prepare_memory_state(collection_items)
        self.create_frame(frame_filename, highlight_line, memory_state)
        return frame_filename

    def prepare_memory_state(self, collection_items):
        if collection_items is None:
            return None

        return {"Nyílt": collection_items}

    def create_frame(self, filename, highlight_line=None, memory_state=None):
        fig, ax = plt.subplots(figsize=(18, 12))

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        nx.draw(
            self.graph,
            self.pos,
            ax=ax,
            labels={n: n for n in self.graph.nodes()},
            node_color=[self.node_states[node] for node in self.graph.nodes()],
            node_size=1000,
            with_labels=True,
            font_color='red',
            font_size=16,
            arrows=True
        )

        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(
            self.graph,
            self.pos,
            edge_labels=edge_labels,
            ax=ax,
            font_color='blue',
            font_size=14
        )

        start_y = 0.9
        line_spacing = 0.04
        font_size = 10

        for i, line in enumerate(self.pseudocode):
            color = 'red' if i == highlight_line else 'black'
            ax.text(
                1.3, start_y - i * line_spacing,
                line,
                fontsize=font_size,
                color=color,
                family='monospace',
                va='top',
                transform=ax.transAxes
            )

        if memory_state:
            if "Nyílt" in memory_state:
                collection = memory_state["Nyílt"]
                if collection:
                    self.collection_renderer.render(ax, collection)

            if "Zárt" in memory_state:
                closed_set = memory_state["Zárt"]
                ax.text(
                    0.1, 0.3,
                    f"Zárt: {set(closed_set)}",
                    fontsize=10,
                    color='darkblue',
                    transform=ax.transAxes
                )

            if "Values" in memory_state:
                values = memory_state["Values"]
                for i, info in enumerate(values):
                    ax.text(
                        0.1, 0.4 - i * 0.05,
                        info,
                        fontsize=10,
                        color='darkblue',
                        transform=ax.transAxes
                    )

        ax.axis("off")
        plt.tight_layout()
        plt.savefig(filename, bbox_inches="tight")
        plt.close(fig)
        self.frames.append(filename)

    def save_gif(self, search_type=''):
        base_dir = 'animated_graphs'
        os.makedirs(base_dir, exist_ok=True)

        gif_filename = f'{search_type}_graph_animation.gif' if search_type else 'graph_animation.gif'
        gif_path = os.path.join(base_dir, gif_filename)

        images = [Image.open(frame) for frame in self.frames]
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=1000,
            loop=0
        )
        print(f"GIF created: {gif_path}")

    def cleanup(self):
        for file in os.listdir(self.frames_dir):
            file_path = os.path.join(self.frames_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        try:
            os.rmdir(self.frames_dir)
        except Exception as e:
            print(f"Failed to remove directory. Reason: {e}")