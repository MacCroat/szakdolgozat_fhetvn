from graphMaker.GraphAnimator.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import QueueRenderer
from graphMaker.ENodeStateColors import ENodeStateColors

class OptimalGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children, heuristic=None):
        pseudocode = [
            "Startcsúcs := k",
            "G(Startcsúcs) := 0",
            "Sz(Startcsúcs) := nincs",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. G(C) = Min{G(D) | D eleme Nyílt}",
            "   if C eleme V then return C",
            "   for C minden D gyermekére do",
            "       if D nem eleme Nyílt és D nem eleme Zárt then",
            "           G(D) := G(C) + R(o)",
            "           Sz(D) := C",
            "           Nyílt := Nyílt U {D}",
            "       fi",
            "       if D eleme Nyílt és G(D) < G(C) then",
            "           G(D) := G(C) + R(o)",
            "           Sz(D) := C",
            "       fi",
            "   Nyílt := Nyílt \\ {C}",
            "   Zárt := Zárt U {C}",
            "od",
            "return „Nincs megoldás"
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)
        self.g_values = {node: float('inf') for node in self.graph.nodes()}
        self.g_values[start_node] = 0

    def create_collection_renderer(self):
        return QueueRenderer()

    def prepare_memory_state(self, open_items=None, values=None, closed=None):
        return {"Nyílt": (open_items or []), "Zárt": (closed or self.closed_set)}

    def generate_animation(self):
        open_list = [(self.g_values[self.start_node], self.start_node)]
        open_set = {self.start_node}
        self.closed_set = set()

        self.node_states[self.start_node] = ENodeStateColors.OPEN
        self.highlight_pseudocode_lines(range(5))

        while open_list:
            open_nodes = [n for _, n in open_list]
            self.generate_frame(highlight_line=5, open_items=open_nodes, closed=self.closed_set)

            open_list.sort(key=lambda x: x[0])
            g_value, current_node = open_list.pop(0)
            open_set.remove(current_node)
            self.node_states[current_node] = ENodeStateColors.CURRENT

            open_nodes = [n for _, n in open_list]
            self.generate_frame(highlight_line=6, open_items=open_nodes, closed=self.closed_set)

            if current_node == self.goal_node:
                self.generate_frame(highlight_line=7, open_items=open_nodes, closed=self.closed_set)
                self.node_states[current_node] = ENodeStateColors.GOAL
                self.generate_frame(highlight_line=7, open_items=open_nodes, closed=self.closed_set)
                break

            self.generate_frame(highlight_line=8, open_items=open_nodes, closed=self.closed_set)

            for child in self.children.get(current_node, []):
                edge_data = self.graph.get_edge_data(current_node, child)
                cost = edge_data['weight'] if edge_data and 'weight' in edge_data else 1
                new_g = self.g_values[current_node] + cost

                self.generate_frame(highlight_line=9, open_items=open_nodes, closed=self.closed_set)

                if child not in open_set and child not in self.closed_set:
                    self.generate_frame(highlight_line=10, open_items=open_nodes, closed=self.closed_set)

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=11, open_items=open_nodes, closed=self.closed_set)

                    open_list.append((new_g, child))
                    open_set.add(child)
                    self.node_states[child] = ENodeStateColors.OPEN
                    open_nodes = [n for _, n in open_list]

                    self.generate_frame(highlight_line=12, open_items=open_nodes, closed=self.closed_set)

                self.generate_frame(highlight_line=13, open_items=open_nodes, closed=self.closed_set)
                self.generate_frame(highlight_line=14, open_items=open_nodes, closed=self.closed_set)

                if child in open_set and self.g_values[child] > new_g:
                    self.generate_frame(highlight_line=15, open_items=open_nodes, closed=self.closed_set)

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=16, open_items=open_nodes, closed=self.closed_set)

                    for i, (old_g, node) in enumerate(open_list):
                        if node == child:
                            open_list[i] = (new_g, child)
                            break
                    open_nodes = [n for _, n in open_list]

                self.generate_frame(highlight_line=17, open_items=open_nodes, closed=self.closed_set)

            self.node_states[current_node] = ENodeStateColors.CLOSED
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self.generate_frame(highlight_line=18, open_items=open_nodes, closed=self.closed_set)
            self.generate_frame(highlight_line=19, open_items=open_nodes, closed=self.closed_set)

        if not open_list and self.goal_node not in self.closed_set:
            self.generate_frame(highlight_line=21, open_items=[], closed=self.closed_set)