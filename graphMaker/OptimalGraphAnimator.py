from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import QueueRenderer


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

    def _create_collection_renderer(self):
        return QueueRenderer()

    def _prepare_memory_state(self, collection_items=None):
        if collection_items is None:
            return None

        return {"Nyílt": collection_items, "Zárt": self.closed_set}

    def generate_animation(self):
        open_list = [(self.g_values[self.start_node], self.start_node)]
        open_set = {self.start_node}
        self.closed_set = set()
        self.frame_id = 0

        self.node_states[self.start_node] = 'blue'

        self._highlight_pseudocode_lines(range(5))

        while open_list:
            open_nodes = [n for _, n in open_list]
            self.generate_frame(highlight_line=5, collection_items=open_nodes)
            self.frame_id += 1

            open_list.sort(key=lambda x: x[0])
            g_value, current_node = open_list.pop(0)
            open_set.remove(current_node)
            self.node_states[current_node] = 'red'

            open_nodes = [n for _, n in open_list]
            self.generate_frame(highlight_line=6, collection_items=open_nodes)
            self.frame_id += 1

            if current_node == self.goal_node:
                self.generate_frame(highlight_line=7, collection_items=open_nodes)
                self.frame_id += 1
                self.node_states[current_node] = 'green'
                self.generate_frame(highlight_line=7, collection_items=open_nodes)
                break

            self.generate_frame(highlight_line=8, collection_items=open_nodes)
            self.frame_id += 1

            for child in self.children.get(current_node, []):
                edge_data = self.graph.get_edge_data(current_node, child)
                cost = edge_data['weight'] if edge_data and 'weight' in edge_data else 1
                new_g = self.g_values[current_node] + cost

                self.generate_frame(highlight_line=9, collection_items=open_nodes)
                self.frame_id += 1

                if child not in open_set and child not in self.closed_set:
                    self.generate_frame(highlight_line=10, collection_items=open_nodes)
                    self.frame_id += 1

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=11, collection_items=open_nodes)
                    self.frame_id += 1

                    open_list.append((new_g, child))
                    open_set.add(child)
                    self.node_states[child] = 'blue'
                    open_nodes = [n for _, n in open_list]

                    self.generate_frame(highlight_line=12, collection_items=open_nodes)
                    self.frame_id += 1

                self.generate_frame(highlight_line=13, collection_items=open_nodes)
                self.frame_id += 1

                self.generate_frame(highlight_line=14, collection_items=open_nodes)
                self.frame_id += 1

                if child in open_set and self.g_values[child] > new_g:
                    self.generate_frame(highlight_line=15, collection_items=open_nodes)
                    self.frame_id += 1

                    self.g_values[child] = new_g
                    self.generate_frame(highlight_line=16, collection_items=open_nodes)
                    self.frame_id += 1

                    for i, (old_g, node) in enumerate(open_list):
                        if node == child:
                            open_list[i] = (new_g, child)
                            break
                    open_nodes = [n for _, n in open_list]

                self.generate_frame(highlight_line=17, collection_items=open_nodes)
                self.frame_id += 1

            self.node_states[current_node] = 'gray'
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self.generate_frame(highlight_line=18, collection_items=open_nodes)
            self.frame_id += 1

            self.generate_frame(highlight_line=19, collection_items=open_nodes)
            self.frame_id += 1

        if not open_list and self.goal_node not in self.closed_set:
            self.generate_frame(highlight_line=21, collection_items=[])
            self.frame_id += 1