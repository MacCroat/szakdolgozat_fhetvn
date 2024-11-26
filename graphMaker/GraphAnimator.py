import networkx as nx
import matplotlib.pyplot as plt
import os
from PIL import Image
from abc import ABC, abstractmethod
import shutil

class GraphAnimator(ABC):
    def __init__(self, pseudocode, start_node, goal_node, children):
        self.graph = nx.DiGraph()
        self.pos = {
            '0': (0.5, 1),
            '1': (0.4, 0.7),
            '2a': (0.6, 0.7),
            '2b': (0.3, 0.4),
            '2c': (0.5, 0.4),
            '3': (0.4, 0.2),
            'T': (0.4, 0)
        }
        self.edges = [
            ('0', '1'), ('0', '2a'),
            ('1', '2b'), ('1', '2c'),
            ('1', '2a'),
            ('2b', '3'), ('2c', '3'),
            ('3', 'T')
        ]
        self.graph.add_edges_from(self.edges)

        self.pseudocode = pseudocode
        self.start_node = start_node
        self.goal_node = goal_node
        self.children = children

        self.frames_dir = 'graph_frames'
        self.frames = []
        self.node_states = {node: 'yellow' for node in self.graph.nodes()}
        self.visited = set()

        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)

    @abstractmethod
    def generate_animation(self):
        pass

    def create_frame(self, filename, highlight_line=None):
        # Create a new figure with explicit axes
        fig, ax = plt.subplots(figsize=(8, 10))

        # Draw the graph
        nx.draw(
            self.graph,
            self.pos,
            ax=ax,
            labels={n: n for n in self.graph.nodes()},
            node_color=[self.node_states[node] for node in self.graph.nodes()],
            node_size=1000,
            with_labels=True,
            font_color='white',
            font_size=16,
            arrows=True
        )

        # Add pseudocode
        for i, line in enumerate(self.pseudocode):
            color = 'red' if i == highlight_line else 'black'
            ax.text(1.1, 1 - i * 0.08, line, fontsize=12, color=color, family='monospace', va='top', transform=ax.transAxes)

        # Remove axis
        ax.axis("off")

        # Save the figure
        plt.tight_layout()
        plt.savefig(filename, bbox_inches="tight")
        plt.close(fig)  # Close the figure to free up memory
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
