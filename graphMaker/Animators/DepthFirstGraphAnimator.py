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

    def generate_animation(self):
        self.stack = [self.start_node]
        closed_set = set()

        for i in range(5):
            self.generate_frame(highlight_line=i, open_items=list(self.stack), closed=closed_set)

        while self.stack:
            current_node = self.stack.pop()
            self.node_states[current_node] = ENodeStateColors.CURRENT

            self.generate_frame(highlight_line=6, open_items=list(self.stack), closed=closed_set)

            if current_node == self.goal_node:
                self.node_states[current_node] = ENodeStateColors.GOAL
                self.generate_frame(highlight_line=7, open_items=list(self.stack), closed=closed_set)
                break

            for child in self.children.get(current_node, []):
                if child not in self.stack and child not in closed_set:
                    self.stack.append(child)
                    self.node_states[child] = ENodeStateColors.OPEN

            closed_set.add(current_node)
            self.node_states[current_node] = ENodeStateColors.CLOSED

            self.generate_frame(highlight_line=8, open_items=list(self.stack), closed=closed_set)

        if not self.stack and self.goal_node not in closed_set:
            self.generate_frame(highlight_line=16, open_items=list(self.stack), closed=closed_set)