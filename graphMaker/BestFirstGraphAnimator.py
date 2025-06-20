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
            "           H(D) := heurisztika érték",
            "           Sz(D) := C",
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
        self.predecessors = {node: None for node in self.graph.nodes()}

    def _create_collection_renderer(self):
        return PriorityQueueRenderer()

    def _create_and_save_frame(self, frame_id, highlight_line, pq_items=None):
        frame_filename = f"{self.frames_dir}/frame_{frame_id:04d}.png"

        display_items = None
        if pq_items is not None:
            sorted_items = sorted(pq_items)
            display_items = [(f"{node}", i + 1) for i, (h, node) in enumerate(sorted_items)]

            value_info = []
            for h, node in sorted_items:
                value_info.append(f"{node}: h={self.heuristic.get(node, 0)}")

            memory_state = {"Nyílt": display_items, "Values": value_info}
        else:
            memory_state = None

        self.create_frame(frame_filename, highlight_line, memory_state=memory_state)

    def generate_animation(self):
        pq = [(self.heuristic.get(self.start_node, 0), self.start_node)]
        open_set = {self.start_node}
        closed_set = set()
        frame_id = 0

        self.node_states[self.start_node] = 'blue'

        for i in range(5):
            self._create_and_save_frame(frame_id, highlight_line=i, pq_items=pq)
            frame_id += 1

        while pq:
            self._create_and_save_frame(frame_id, highlight_line=5, pq_items=pq)
            frame_id += 1

            pq.sort()
            current_h, current_node = pq.pop(0)
            open_set.remove(current_node)

            self.node_states[current_node] = 'red'
            self._create_and_save_frame(frame_id, highlight_line=6, pq_items=pq)
            frame_id += 1

            if current_node == self.goal_node:
                self._create_and_save_frame(frame_id, highlight_line=7, pq_items=pq)
                frame_id += 1
                self.node_states[current_node] = 'green'
                self._create_and_save_frame(frame_id, highlight_line=7, pq_items=pq)
                break

            self._create_and_save_frame(frame_id, highlight_line=8, pq_items=pq)
            frame_id += 1

            for child in self.children.get(current_node, []):
                self._create_and_save_frame(frame_id, highlight_line=9, pq_items=pq)
                frame_id += 1

                if child not in open_set and child not in closed_set:
                    self._create_and_save_frame(frame_id, highlight_line=10, pq_items=pq)
                    frame_id += 1

                    self.predecessors[child] = current_node
                    self._create_and_save_frame(frame_id, highlight_line=11, pq_items=pq)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=12, pq_items=pq)
                    frame_id += 1

                    pq.append((self.heuristic.get(child, 0), child))
                    pq.sort()
                    open_set.add(child)
                    self.node_states[child] = 'blue'

                    self._create_and_save_frame(frame_id, highlight_line=13, pq_items=pq)
                    frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=15, pq_items=pq)
            frame_id += 1

            self.node_states[current_node] = 'gray'
            closed_set.add(current_node)
            self.visited.add(current_node)

            self._create_and_save_frame(frame_id, highlight_line=16, pq_items=pq)
            frame_id += 1

        if not pq and current_node != self.goal_node:
            self._create_and_save_frame(frame_id, highlight_line=18, pq_items=[])
            frame_id += 1