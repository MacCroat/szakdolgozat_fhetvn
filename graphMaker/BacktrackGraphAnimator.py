from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import StackRenderer
import matplotlib.pyplot as plt
import networkx as nx


class BacktrackGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := A",
            "AKT := A",
            "Operátorok := {o1, o2, o3}",
            "Szülőcsúcs := NULL",
            "While AKT != T do",
            "   if AKT.OPS nem üres then",
            "      válassz tetszőleges operátort AKT.OPS-ból",
            "      alkalmazd az AKT-ra",
            "      AKT := új csúcs",
            "      töröld az alkalmazott operátort AKT.OPS-ból",
            "   else if AKT == S then",
            "      \"Nincs megoldás\"",
            "      break",
            "   else",
            "      BackTrack",
            "Return \"Megoldás: S → T-be vezetőút\""
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)

        self.edge_operators = {}
        if hasattr(self.graph_provider, 'get_edge_operators'):
            self.edge_operators = self.graph_provider.get_edge_operators()

        self.children = {node: [] for node in self.graph.nodes()}
        for (u, v) in self.edge_operators:
            self.children[u].append(v)

        self.current_node = start_node
        self.path = [start_node]
        self.node_states[start_node] = 'blue'
        self.visited_children = {self.current_node: []}

    def _create_collection_renderer(self):
        return StackRenderer()

    def _prepare_memory_state(self, path=None, closed=None):
        state = {}
        if path:
            state["Nyílt"] = path
        if closed is not None:
            state["Zárt"] = closed
        return state

    def create_frame(self, filename, highlight_line=None, memory_state=None):
        fig, ax = plt.subplots(figsize=(18, 12))

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        path_edges = set()
        if hasattr(self, 'path') and len(self.path) > 1:
            path_edges = set(zip(self.path[:-1], self.path[1:]))

        edge_colors = []
        for edge in self.graph.edges():
            if edge in path_edges:
                edge_colors.append('red')
            else:
                edge_colors.append('black')

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
            arrows=True,
            edge_color=edge_colors,
            width=2
        )

        edge_labels = {}
        for edge in self.graph.edges():
            if edge in self.edge_operators:
                edge_labels[edge] = self.edge_operators[edge]

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

        if memory_state and "Nyílt" in memory_state:
            collection = memory_state["Nyílt"]
            if collection:
                self.collection_renderer.render(ax, collection)
        if memory_state and "Zárt" in memory_state:
            closed_set = memory_state["Zárt"]
            ax.text(
                0.1, 0.3,
                f"Zárt: {set(closed_set)}",
                fontsize=10,
                color='darkblue',
                transform=ax.transAxes
            )

        ax.axis("off")
        plt.tight_layout()
        plt.savefig(filename, bbox_inches="tight")
        plt.close(fig)
        self.frames.append(filename)

    def generate_animation(self):
        self.frame_id = 0
        for i in range(4):
            self._create_frame(i, self.path, closed=set())

        stack = [(self.start_node, iter(self.children.get(self.start_node, [])))]
        self.path = [self.start_node]
        closed = set()
        found = False

        while stack:
            current_node, children_iter = stack[-1]
            self.current_node = current_node
            self.node_states = {node: 'gray' if node in closed else 'yellow' for node in self.graph.nodes()}
            for n in self.path:
                if n not in closed:
                    self.node_states[n] = 'blue'
            self.node_states[current_node] = 'blue'
            self._create_frame(4, list(self.path), closed=closed)

            if current_node == self.goal_node:
                found = True
                break

            try:
                child = next(children_iter)
                if (child == self.start_node and current_node == 'C') or (child not in self.path and child not in closed):
                    self._create_frame(5, list(self.path), closed=closed)
                    self._create_frame(6, list(self.path), closed=closed)
                    self._create_frame(7, list(self.path), closed=closed)
                    self.path.append(child)
                    stack.append((child, iter(self.children.get(child, []))))
                    self.node_states[child] = 'blue'
                    self._create_frame(8, list(self.path), closed=closed)
                    self._create_frame(9, list(self.path), closed=closed)
            except StopIteration:
                closed.add(current_node)
                self.node_states[current_node] = 'gray'
                self._create_frame(13, list(self.path), closed=closed)
                self._create_frame(14, list(self.path), closed=closed)
                stack.pop()
                if self.path:
                    self.path.pop()

        if found:
            self.node_states[self.current_node] = 'green'
            self._create_frame(15, list(self.path), closed=closed)

    def _create_frame(self, highlight_line, path, closed=None):
        frame_filename = f"{self.frames_dir}/frame_{self.frame_id:04d}.png"
        memory_state = self._prepare_memory_state(path, closed)
        self.create_frame(frame_filename, highlight_line, memory_state)
        self.frame_id += 1
