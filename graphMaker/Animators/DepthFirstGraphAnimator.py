from graphMaker.GraphAnimator.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import StackRenderer
from graphMaker.ENodeStateColors import ENodeStateColors


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
        self.stack = [start_node]
        self.node_states[start_node] = ENodeStateColors.OPEN

    def create_collection_renderer(self):
        return StackRenderer()

    def _create_and_save_frame(self, frame_id, highlight_line, stack_items=None, closed_items=None):
        frame_filename = f"{self.frames_dir}/frame_{frame_id:04d}.png"

        memory_state = {"Nyílt": stack_items} if stack_items is not None else {}
        if closed_items is not None:
            memory_state["Zárt"] = closed_items

        self.create_frame(frame_filename, highlight_line, memory_state)
        self.frames.append(frame_filename)

    def generate_animation(self):
        frame_id = 0
        self.stack = [self.start_node]
        closed_set = set()

        for i in range(5):
            self._create_and_save_frame(frame_id, highlight_line=i, stack_items=self.stack, closed_items=closed_set)
            frame_id += 1

        while self.stack:
            current_node = self.stack.pop()
            self.node_states[current_node] = ENodeStateColors.CURRENT

            self._create_and_save_frame(frame_id, highlight_line=6, stack_items=self.stack, closed_items=closed_set)
            frame_id += 1

            if current_node == self.goal_node:
                self.node_states[current_node] = ENodeStateColors.GOAL
                self._create_and_save_frame(frame_id, highlight_line=7, stack_items=self.stack, closed_items=closed_set)
                break

            for child in self.children.get(current_node, []):
                if child not in self.stack and child not in closed_set:
                    self.stack.append(child)
                    self.node_states[child] = ENodeStateColors.OPEN

            closed_set.add(current_node)
            self.node_states[current_node] = ENodeStateColors.CLOSED

            self._create_and_save_frame(frame_id, highlight_line=8, stack_items=self.stack, closed_items=closed_set)
            frame_id += 1

        if not self.stack and self.goal_node not in closed_set:
            self._create_and_save_frame(frame_id, highlight_line=16, stack_items=self.stack, closed_items=closed_set)
            frame_id += 1