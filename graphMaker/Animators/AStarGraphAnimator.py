from graphMaker.GraphAnimator.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import PriorityQueueRenderer
from graphMaker.ENodeStateColors import ENodeStateColors

class AStarGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := k",
            "G(Startcsúcs) := 0",
            "F(Startcsúcs) := G(Startcsúcs) + H(Startcsúcs)",
            "Sz(Startcsúcs) := nincs",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. F(C) = Min{F(D) | D eleme Nyílt}",
            "   if C eleme V then return C",
            "   for C minden D gyermekére do",
            "       if D nem eleme Nyílt és D nem eleme Zárt then",
            "           G(D) := G(C) + R(o)",
            "           F(D) := G(D) + H(D)",
            "           Sz(D) := C",
            "           Nyílt := Nyílt U {D}",
            "       fi",
            "       if D eleme Nyílt és G(D) > G(C) + R(o) then",
            "           G(D) := G(C) + R(o)",
            "           Sz(D) := C",
            "           F(D) := G(D) + H(D)",
            "       fi",
            "       if D eleme Zárt és G(D) > G(C) + R(o) then",
            "           G(D) := G(C) + R(o)",
            "           Sz(D) := C",
            "           F(D) := G(D) + H(D)",
            "           Zárt := Zárt \\ {D}",
            "           Nyílt := Nyílt U {D}",
            "       fi",
            "   od",
            "   Nyílt := Nyílt \\ {C}",
            "   Zárt := Zárt U {C}",
            "od",
            "return „Nincs megoldás"
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)

        self.heuristic = graph.get_heuristic() if hasattr(graph, 'get_heuristic') else {node: 0 for node in self.graph.nodes()}
        self.g_values = {node: float('inf') for node in self.graph.nodes()}
        self.f_values = {node: float('inf') for node in self.graph.nodes()}
        self.closed_set = set()

        self.g_values[start_node] = 0
        self.f_values[start_node] = self.heuristic.get(start_node, 0)

    def create_collection_renderer(self):
        return PriorityQueueRenderer()

    def prepare_memory_state(self, open_items=None, values=None, closed=None):
        open_items = open_items or []
        if open_items and isinstance(open_items[0], tuple):
            sorted_items = sorted(open_items)
            display_items = [(f"{node}", i + 1) for i, (f, node) in enumerate(sorted_items)]
            value_info = []
            for f, node in sorted_items:
                g_value = self.g_values[node]
                h_value = self.heuristic.get(node, 0)
                value_info.append(f"{node}: f={f:.1f}, g={g_value:.1f}, h={h_value}")
            return {"Nyílt": display_items, "Values": value_info, "Zárt": (closed or self.closed_set)}
        return {"Nyílt": open_items, "Zárt": (closed or self.closed_set)}

    def generate_animation(self):
        pq = [(self.f_values[self.start_node], self.start_node)]
        open_set = {self.start_node}
        self.closed_set = set()

        self.node_states[self.start_node] = ENodeStateColors.OPEN
        self.highlight_pseudocode_lines(range(6))

        while pq:
            self.generate_frame(highlight_line=6, open_items=pq, closed=self.closed_set)

            pq.sort()
            current_f, current_node = pq.pop(0)
            open_set.remove(current_node)

            self.node_states[current_node] = ENodeStateColors.CURRENT
            self.generate_frame(highlight_line=7, open_items=pq, closed=self.closed_set)

            if current_node == self.goal_node:
                self.generate_frame(highlight_line=8, open_items=pq, closed=self.closed_set)
                self.node_states[current_node] = ENodeStateColors.GOAL
                self.generate_frame(highlight_line=8, open_items=pq, closed=self.closed_set)
                break

            self.generate_frame(highlight_line=9, open_items=pq, closed=self.closed_set)

            for child in self.children.get(current_node, []):
                edge_data = self.graph.get_edge_data(current_node, child)
                cost = edge_data['weight'] if edge_data and 'weight' in edge_data else 1
                new_g = self.g_values[current_node] + cost

                self.generate_frame(highlight_line=10, open_items=pq, closed=self.closed_set)

                if child not in open_set and child not in self.closed_set:
                    self.generate_frame(highlight_line=11, open_items=pq, closed=self.closed_set)

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=12, open_items=pq, closed=self.closed_set)

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self.generate_frame(highlight_line=13, open_items=pq, closed=self.closed_set)

                    self.generate_frame(highlight_line=14, open_items=pq, closed=self.closed_set)

                    pq.append((self.f_values[child], child))
                    open_set.add(child)
                    self.node_states[child] = ENodeStateColors.OPEN

                    self.generate_frame(highlight_line=15, open_items=pq, closed=self.closed_set)

                elif child in open_set and self.g_values[child] > new_g:
                    self.generate_frame(highlight_line=16, open_items=pq, closed=self.closed_set)

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=17, open_items=pq, closed=self.closed_set)

                    self.generate_frame(highlight_line=18, open_items=pq, closed=self.closed_set)

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self.generate_frame(highlight_line=19, open_items=pq, closed=self.closed_set)

                    for i in range(len(pq)):
                        if pq[i][1] == child:
                            pq[i] = (self.f_values[child], child)
                            break

                elif child in self.closed_set and self.g_values[child] > new_g:
                    self.generate_frame(highlight_line=20, open_items=pq, closed=self.closed_set)

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=21, open_items=pq, closed=self.closed_set)

                    self.generate_frame(highlight_line=22, open_items=pq, closed=self.closed_set)

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self.generate_frame(highlight_line=23, open_items=pq, closed=self.closed_set)

                    self.closed_set.remove(child)
                    self.generate_frame(highlight_line=24, open_items=pq, closed=self.closed_set)

                    pq.append((self.f_values[child], child))
                    open_set.add(child)
                    self.node_states[child] = ENodeStateColors.OPEN

                    self.generate_frame(highlight_line=25, open_items=pq, closed=self.closed_set)

            self.generate_frame(highlight_line=27, open_items=pq, closed=self.closed_set)

            self.node_states[current_node] = ENodeStateColors.CLOSED
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self.generate_frame(highlight_line=28, open_items=pq, closed=self.closed_set)

        if not pq and self.goal_node not in self.closed_set:
            self.generate_frame(highlight_line=30, open_items=[], closed=self.closed_set)