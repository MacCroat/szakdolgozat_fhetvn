import os
from typing import Any, Dict, Iterable, Optional, Sequence
import matplotlib.pyplot as plt
import networkx as nx
from graphMaker.ENodeStateColors import ENodeStateColors

class FrameRenderer:
    def __init__(self, frames_dir: str = 'graph_frames', collection_renderer=None):
        self.frames_dir = frames_dir
        os.makedirs(self.frames_dir, exist_ok=True)
        self.collection_renderer = collection_renderer

    def render(
        self,
        graph,
        pos,
        node_states: Dict[Any, Any],
        pseudocode: Sequence[str],
        frame_id: int,
        highlight_line: Optional[int] = None,
        memory_state: Optional[Dict[str, Any]] = None
    ) -> str:
        fname = os.path.join(self.frames_dir, f"frame_{frame_id:04d}.png")

        fig, ax = plt.subplots(figsize=(18, 12))
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        def _color(val: Any) -> str:
            return val.value if isinstance(val, ENodeStateColors) else str(val)

        nx.draw(
            graph,
            pos,
            ax=ax,
            labels={n: n for n in graph.nodes()},
            node_color=[_color(node_states[n]) for n in graph.nodes()],
            node_size=1000,
            with_labels=True,
            font_color='red',
            font_size=16,
            arrows=True
        )

        weights = nx.get_edge_attributes(graph, 'weight')
        if weights:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, ax=ax, font_color='blue', font_size=14)

        start_y, spacing, fsize = 0.9, 0.04, 10
        for i, line in enumerate(pseudocode):
            color = 'red' if i == (highlight_line or -1) else 'black'
            ax.text(1.3, start_y - i * spacing, line, fontsize=fsize, color=color, family='monospace', va='top',
                    transform=ax.transAxes)

        if memory_state:
            if "Nyílt" in memory_state and self.collection_renderer:
                collection = memory_state["Nyílt"]
                if collection:
                    self.collection_renderer.render(ax, collection)
            if "Zárt" in memory_state:
                ax.text(0.1, 0.3, f"Zárt: {set(memory_state['Zárt'])}", fontsize=10, color='darkblue',
                        transform=ax.transAxes)
            if "Values" in memory_state:
                for i, info in enumerate(memory_state["Values"]):
                    ax.text(0.1, 0.4 - i * 0.05, info, fontsize=10, color='darkblue', transform=ax.transAxes)

        ax.axis("off")
        plt.tight_layout()
        plt.savefig(fname, bbox_inches="tight")
        plt.close(fig)
        return fname