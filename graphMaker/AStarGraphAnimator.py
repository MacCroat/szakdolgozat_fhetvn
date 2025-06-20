from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import PriorityQueueRenderer

class AGraphAnimator(GraphAnimator):
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

        self.g_values[start_node] = 0
        self.f_values[start_node] = self.heuristic.get(start_node, 0)

    def _create_collection_renderer(self):
        return PriorityQueueRenderer()

    def _create_and_save_frame(self, frame_id, highlight_line, pq_items=None):
        frame_filename = f"{self.frames_dir}/frame_{frame_id:04d}.png"

        display_items = None
        if pq_items is not None:
            sorted_items = sorted(pq_items)
            display_items = [(f"{node}", i + 1) for i, (f, node) in enumerate(sorted_items)]

            value_info = []
            for f, node in sorted_items:
                g_value = self.g_values[node]
                h_value = self.heuristic.get(node, 0)
                value_info.append(f"{node}: f={f:.1f}, g={g_value:.1f}, h={h_value}")

            memory_state = {"Nyílt": display_items, "Values": value_info}
        else:
            memory_state = None

        self.create_frame(frame_filename, highlight_line, memory_state=memory_state)

    def generate_animation(self):
        pq = [(self.f_values[self.start_node], self.start_node)]
        open_set = {self.start_node}
        closed_set = set()
        frame_id = 0

        self.node_states[self.start_node] = 'blue'

        for i in range(6):
            self._create_and_save_frame(frame_id, highlight_line=i, pq_items=pq)
            frame_id += 1

        while pq:
            self._create_and_save_frame(frame_id, highlight_line=6, pq_items=pq)
            frame_id += 1

            pq.sort()
            current_f, current_node = pq.pop(0)
            open_set.remove(current_node)

            self.node_states[current_node] = 'red'
            self._create_and_save_frame(frame_id, highlight_line=7, pq_items=pq)
            frame_id += 1

            if current_node == self.goal_node:
                self._create_and_save_frame(frame_id, highlight_line=8, pq_items=pq)
                frame_id += 1
                self.node_states[current_node] = 'green'
                self._create_and_save_frame(frame_id, highlight_line=8, pq_items=pq)
                break

            self._create_and_save_frame(frame_id, highlight_line=9, pq_items=pq)
            frame_id += 1

            for child in self.children.get(current_node, []):
                edge_data = self.graph.get_edge_data(current_node, child)
                cost = edge_data['weight'] if edge_data and 'weight' in edge_data else 1
                new_g = self.g_values[current_node] + cost

                self._create_and_save_frame(frame_id, highlight_line=10, pq_items=pq)
                frame_id += 1

                if child not in open_set and child not in closed_set:
                    self._create_and_save_frame(frame_id, highlight_line=11, pq_items=pq)
                    frame_id += 1

                    self.g_values[child] = new_g
                    self._create_and_save_frame(frame_id, highlight_line=12, pq_items=pq)
                    frame_id += 1

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self._create_and_save_frame(frame_id, highlight_line=13, pq_items=pq)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=14, pq_items=pq)
                    frame_id += 1

                    pq.append((self.f_values[child], child))
                    pq.sort()
                    open_set.add(child)
                    self.node_states[child] = 'blue'

                    self._create_and_save_frame(frame_id, highlight_line=15, pq_items=pq)
                    frame_id += 1

                elif child in open_set and self.g_values[child] > new_g:
                    self._create_and_save_frame(frame_id, highlight_line=16, pq_items=pq)
                    frame_id += 1

                    self.g_values[child] = new_g
                    self._create_and_save_frame(frame_id, highlight_line=17, pq_items=pq)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=18, pq_items=pq)
                    frame_id += 1

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self._create_and_save_frame(frame_id, highlight_line=19, pq_items=pq)
                    frame_id += 1

                    for i in range(len(pq)):
                        if pq[i][1] == child:
                            pq[i] = (self.f_values[child], child)
                            break
                    pq.sort()

                elif child in closed_set and self.g_values[child] > new_g:
                    self._create_and_save_frame(frame_id, highlight_line=20, pq_items=pq)
                    frame_id += 1

                    self.g_values[child] = new_g
                    self._create_and_save_frame(frame_id, highlight_line=21, pq_items=pq)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=22, pq_items=pq)
                    frame_id += 1

                    self.f_values[child] = new_g + self.heuristic.get(child, 0)
                    self._create_and_save_frame(frame_id, highlight_line=23, pq_items=pq)
                    frame_id += 1

                    closed_set.remove(child)
                    self._create_and_save_frame(frame_id, highlight_line=24, pq_items=pq)
                    frame_id += 1

                    pq.append((self.f_values[child], child))
                    pq.sort()
                    open_set.add(child)
                    self.node_states[child] = 'blue'

                    self._create_and_save_frame(frame_id, highlight_line=25, pq_items=pq)
                    frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=26, pq_items=pq)
            frame_id += 1

            self.node_states[current_node] = 'gray'
            closed_set.add(current_node)
            self.visited.add(current_node)

            self._create_and_save_frame(frame_id, highlight_line=27, pq_items=pq)
            frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=28, pq_items=pq)
            frame_id += 1

        if not pq and self.goal_node not in closed_set:
            self._create_and_save_frame(frame_id, highlight_line=30, pq_items=[])
            frame_id += 1