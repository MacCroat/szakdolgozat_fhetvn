from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import PriorityQueueRenderer


class DijkstraGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := k",
            "D(Startcsúcs) := 0",
            "D(v) := ∞ for all v ≠ Startcsúcs",
            "Sz(Startcsúcs) := nincs",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. D(C) = Min{D(D) | D eleme Nyílt}",
            "   if C eleme V then return C",
            "   for C minden D gyermekére do",
            "       if D nem eleme Nyílt és D nem eleme Zárt then",
            "           D(D) := D(C) + w(C,D)",
            "           Sz(D) := C",
            "           Nyílt := Nyílt U {D}",
            "       fi",
            "       if D eleme Nyílt és D(D) > D(C) + w(C,D) then",
            "           D(D) := D(C) + w(C,D)",
            "           Sz(D) := C",
            "       fi",
            "   od",
            "   Nyílt := Nyílt \\ {C}",
            "   Zárt := Zárt U {C}",
            "od",
            "return „Nincs megoldás"
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)

        self.distances = {node: float('inf') for node in self.graph.nodes()}
        self.distances[start_node] = 0
        self.predecessors = {node: None for node in self.graph.nodes()}
        self.closed_set = set()

    def _create_collection_renderer(self):
        return PriorityQueueRenderer()

    def _prepare_memory_state(self, collection_items=None):
        if collection_items is None or not collection_items:
            return {"Nyílt": [], "Zárt": self.closed_set}

        if isinstance(collection_items[0], tuple):
            sorted_items = sorted(collection_items)
            display_items = [(f"{node}", i + 1) for i, (d, node) in enumerate(sorted_items)]

            value_info = []
            for d, node in sorted_items:
                distance = self.distances[node]
                dist_display = int(distance) if distance.is_integer() else f"{distance:.1f}"
                value_info.append(f"{node}:d={dist_display}")

            return {"Nyílt": display_items, "Values": value_info, "Zárt": self.closed_set}
        else:
            return {"Nyílt": collection_items, "Zárt": self.closed_set}

    def generate_animation(self):
        pq = [(self.distances[self.start_node], self.start_node)]
        open_set = {self.start_node}
        self.closed_set = set()
        self.frame_id = 0

        self.node_states[self.start_node] = 'blue'

        self._highlight_pseudocode_lines(range(6))

        while pq:
            self._create_frame(highlight_line=6, collection_items=pq)
            self.frame_id += 1

            pq.sort()
            current_dist, current_node = pq.pop(0)
            open_set.remove(current_node)

            self.node_states[current_node] = 'red'
            self._create_frame(highlight_line=7, collection_items=pq)
            self.frame_id += 1

            if current_node == self.goal_node:
                self._create_frame(highlight_line=8, collection_items=pq)
                self.frame_id += 1
                self.node_states[current_node] = 'green'
                self._create_frame(highlight_line=8, collection_items=pq)
                break

            self._create_frame(highlight_line=9, collection_items=pq)
            self.frame_id += 1

            for child in self.children.get(current_node, []):
                edge_data = self.graph.get_edge_data(current_node, child)
                weight = edge_data['weight'] if edge_data and 'weight' in edge_data else 1
                new_distance = self.distances[current_node] + weight

                self._create_frame(highlight_line=10, collection_items=pq)
                self.frame_id += 1

                if child not in open_set and child not in self.closed_set:
                    self._create_frame(highlight_line=11, collection_items=pq)
                    self.frame_id += 1

                    self.distances[child] = new_distance
                    self.predecessors[child] = current_node
                    self._create_frame(highlight_line=12, collection_items=pq)
                    self.frame_id += 1

                    self._create_frame(highlight_line=13, collection_items=pq)
                    self.frame_id += 1

                    pq.append((self.distances[child], child))
                    open_set.add(child)
                    self.node_states[child] = 'blue'

                    self._create_frame(highlight_line=14, collection_items=pq)
                    self.frame_id += 1

                elif child in open_set and self.distances[child] > new_distance:
                    self._create_frame(highlight_line=15, collection_items=pq)
                    self.frame_id += 1

                    self.distances[child] = new_distance
                    self.predecessors[child] = current_node
                    self._create_frame(highlight_line=16, collection_items=pq)
                    self.frame_id += 1

                    for i in range(len(pq)):
                        if pq[i][1] == child:
                            pq[i] = (self.distances[child], child)
                            break

                    self._create_frame(highlight_line=17, collection_items=pq)
                    self.frame_id += 1

            self._create_frame(highlight_line=19, collection_items=pq)
            self.frame_id += 1

            self.node_states[current_node] = 'gray'
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self._create_frame(highlight_line=20, collection_items=pq)
            self.frame_id += 1

        if not pq and self.goal_node not in self.closed_set:
            self._create_frame(highlight_line=22, collection_items=[])
            self.frame_id += 1