from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import StackRenderer

class DepthFirstGraphAnimator(GraphAnimator):
    def __init__(self, graph, start_node, goal_node, children):
        pseudocode = [
            "Startcsúcs := k",
            "M (Startcsúcs) := 0",
            "Sz (Startcsúcs) := nincs",
            "Nyílt := {Startcsúcs}",
            "Zárt := {}",
            "While Nyílt nem üres do",
            "   Legyen C eleme Nyílt uh. M(C) = Max{M(D) | D eleme Nyílt}",
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

        self.m_values = {node: float('inf') for node in self.graph.nodes()}
        self.m_values[start_node] = 0
        self.parent = {node: None for node in self.graph.nodes()}

    def get_collection_type(self):
        return "Stack"

    def _create_collection_renderer(self):
        return StackRenderer()

    def _create_and_save_frame(self, frame_id, highlight_line, memory_state=None):
        self.memory_state = memory_state
        frame_filename = f"{self.frames_dir}/frame_{frame_id:04d}.png"
        self.create_frame(frame_filename, highlight_line, memory_state)

    def generate_animation(self):
        stack = [self.start_node]
        frame_id = 0

        memory_state = {"Nyílt": stack.copy(), "Zárt": set()}

        self._create_and_save_frame(frame_id, highlight_line=0, memory_state=memory_state)
        frame_id += 1
        self._create_and_save_frame(frame_id, highlight_line=1, memory_state=memory_state)
        frame_id += 1
        self._create_and_save_frame(frame_id, highlight_line=2, memory_state=memory_state)
        frame_id += 1
        self._create_and_save_frame(frame_id, highlight_line=3, memory_state=memory_state)
        frame_id += 1
        self._create_and_save_frame(frame_id, highlight_line=4, memory_state=memory_state)
        frame_id += 1

        while stack:
            self._create_and_save_frame(frame_id, highlight_line=5, memory_state=memory_state)
            frame_id += 1

            current_node = stack.pop()
            memory_state["Nyílt"] = stack.copy()  # Update stack in memory state
            self.node_states[current_node] = 'red'

            self._create_and_save_frame(frame_id, highlight_line=6, memory_state=memory_state)
            frame_id += 1

            if current_node == self.goal_node:
                self._create_and_save_frame(frame_id, highlight_line=7, memory_state=memory_state)
                frame_id += 1
                self.node_states[current_node] = 'green'
                self._create_and_save_frame(frame_id, highlight_line=7, memory_state=memory_state)
                break

            self.node_states[current_node] = 'gray'
            self.visited.add(current_node)
            memory_state["Zárt"] = self.visited.copy()

            self._create_and_save_frame(frame_id, highlight_line=8, memory_state=memory_state)
            frame_id += 1

            for child in reversed(self.children.get(current_node, [])):
                self._create_and_save_frame(frame_id, highlight_line=9, memory_state=memory_state)
                frame_id += 1

                if child not in self.visited and child not in stack:
                    self.node_states[child] = 'blue'
                    # Add to stack immediately when detected
                    stack.append(child)
                    # Update memory state immediately
                    memory_state["Nyílt"] = stack.copy()

                    self._create_and_save_frame(frame_id, highlight_line=10, memory_state=memory_state)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=11, memory_state=memory_state)
                    frame_id += 1

                    self._create_and_save_frame(frame_id, highlight_line=12, memory_state=memory_state)
                    frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=13, memory_state=memory_state)
            frame_id += 1

            self._create_and_save_frame(frame_id, highlight_line=14, memory_state=memory_state)
            frame_id += 1

        if not stack and current_node != self.goal_node:
            self._create_and_save_frame(frame_id, highlight_line=16, memory_state=memory_state)
            frame_id += 1

