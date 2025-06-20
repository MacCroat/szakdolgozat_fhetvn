from collections import deque
from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import QueueRenderer


class BreadthFirstGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := k",
            "M (Startcsúcs) := 0",
            "Sz (Startcsúcs) := nincs",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. M(C) = Min{M(D) | D eleme Nyílt}",
            "   if C eleme V then return C",
            "   for C minden D gyermekére do",
            "       if D nem eleme Nyílt és D nem eleme Zárt then",
            "           M(D) := M(C)+1",
            "           Sz(D) := C",
            "           Nyílt := Nyílt U {D}",
            "   Nyílt := Nyílt \\ {C}",
            "   Zárt := Zárt U {C}",
            "od",
            "return „Nincs megoldás"
        ]
        super().__init__(graph, pseudocode, start_node, goal_node, children)

    def _create_collection_renderer(self):
        return QueueRenderer()

    def _create_and_save_frame(self, frame_id, highlight_line=None, memory_state=None):
        frame_filename = f"{self.frames_dir}/frame_{frame_id:04d}.png"
        self.create_frame(frame_filename, highlight_line, memory_state)

    def generate_animation(self):
        queue = deque([self.start_node])
        frame_id = 0

        memory_state = {"Nyílt": list(queue), "Zárt": set()}
        self.node_states[self.start_node] = 'blue'

        for i in range(5):
            self._create_and_save_frame(frame_id, highlight_line=i, memory_state=memory_state)
            frame_id += 1

        while queue:
            self._create_and_save_frame(frame_id, highlight_line=5, memory_state=memory_state)
            frame_id += 1

            current_node = queue.popleft()
            memory_state["Nyílt"] = list(queue)
            self.node_states[current_node] = 'red'

            self._create_and_save_frame(frame_id, highlight_line=6, memory_state=memory_state)
            frame_id += 1

            if current_node == self.goal_node:
                self._create_and_save_frame(frame_id, highlight_line=7, memory_state=memory_state)
                frame_id += 1
                self.node_states[current_node] = 'green'
                self._create_and_save_frame(frame_id, highlight_line=7, memory_state=memory_state)
                break

            self._create_and_save_frame(frame_id, highlight_line=8, memory_state=memory_state)
            frame_id += 1

            for child in self.children.get(current_node, []):
                self._create_and_save_frame(frame_id, highlight_line=9, memory_state=memory_state)
                frame_id += 1

                if child not in self.visited and child not in queue:
                    self.node_states[child] = 'blue'
                    queue.append(child)
                    memory_state["Nyílt"] = list(queue)

                    self._create_and_save_frame(frame_id, highlight_line=10, memory_state=memory_state)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=11, memory_state=memory_state)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=12, memory_state=memory_state)
                    frame_id += 1

            self.node_states[current_node] = 'gray'
            self.visited.add(current_node)
            memory_state["Zárt"] = self.visited.copy()

            self._create_and_save_frame(frame_id, highlight_line=13, memory_state=memory_state)
            frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=14, memory_state=memory_state)
            frame_id += 1

        if not queue and current_node != self.goal_node:
            self._create_and_save_frame(frame_id, highlight_line=16, memory_state=memory_state)
            frame_id += 1