from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import PriorityQueueRenderer


class BestFirstGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := k",
            "Sz(Startcsúcs) := nincs",
            "H(C) := heurisztika(D)",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. H(C) = Min{H(D) | D eleme Nyílt}",
            "   if C eleme V then return C",
            "   for C minden D gyermekére do",
            "       if D nem eleme Nyílt és D nem eleme Zárt then",
            "           H(D) := heurisztika(C)",
            "           Sz(D) := C",
            "           Nyílt := Nyílt U {D}",
            "   Nyílt := Nyílt \\ {C}",
            "   Zárt := Zárt U {C}",
            "od",
            "return „Nincs megoldás"
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)

        self.heuristic = graph.get_heuristic() if hasattr(graph, 'get_heuristic') else {node: 0 for node in self.graph.nodes()}
        self.closed_set = set()

    def create_collection_renderer(self):
        return PriorityQueueRenderer()

    def prepare_memory_state(self, collection_items=None):
        if collection_items is None or not collection_items:
            return {"Nyílt": [], "Zárt": self.closed_set}

        if isinstance(collection_items[0], tuple):
            sorted_items = sorted(collection_items)
            display_items = [(f"{node}", i + 1) for i, (h, node) in enumerate(sorted_items)]

            value_info = []
            for h, node in sorted_items:
                h_value = self.heuristic.get(node, 0)
                h_display = int(h_value) if h_value == int(h_value) else f"{h_value:.1f}"
                value_info.append(f"{node}: h={h_display}")

            return {"Nyílt": display_items, "Values": value_info, "Zárt": self.closed_set}
        else:
            return {"Nyílt": collection_items, "Zárt": self.closed_set}

    def generate_animation(self):
        pq = [(self.heuristic.get(self.start_node, 0), self.start_node)]
        open_set = {self.start_node}
        self.closed_set = set()
        self.frame_id = 0

        self.node_states[self.start_node] = 'blue'

        self.highlight_pseudocode_lines(range(5))

        while pq:
            self.generate_frame(highlight_line=5, collection_items=pq)
            self.frame_id += 1

            pq.sort()
            current_h, current_node = pq.pop(0)
            open_set.remove(current_node)

            self.node_states[current_node] = 'red'
            self.generate_frame(highlight_line=6, collection_items=pq)
            self.frame_id += 1

            if current_node == self.goal_node:
                self.generate_frame(highlight_line=7, collection_items=pq)
                self.frame_id += 1
                self.node_states[current_node] = 'green'
                self.generate_frame(highlight_line=7, collection_items=pq)
                break

            self.generate_frame(highlight_line=8, collection_items=pq)
            self.frame_id += 1

            for child in self.children.get(current_node, []):
                self.generate_frame(highlight_line=9, collection_items=pq)
                self.frame_id += 1

                if child not in open_set and child not in self.closed_set:
                    self.generate_frame(highlight_line=10, collection_items=pq)
                    self.frame_id += 1

                    self.generate_frame(highlight_line=11, collection_items=pq)
                    self.frame_id += 1

                    self.generate_frame(highlight_line=12, collection_items=pq)
                    self.frame_id += 1

                    pq.append((self.heuristic.get(child, 0), child))
                    open_set.add(child)
                    self.node_states[child] = 'blue'

                    self.generate_frame(highlight_line=13, collection_items=pq)
                    self.frame_id += 1

            self.generate_frame(highlight_line=14, collection_items=pq)
            self.frame_id += 1

            self.node_states[current_node] = 'gray'
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self.generate_frame(highlight_line=15, collection_items=pq)
            self.frame_id += 1

        if not pq and self.goal_node not in self.closed_set:
            self.generate_frame(highlight_line=17, collection_items=[])
            self.frame_id += 1