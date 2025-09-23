from collections import deque
from graphMaker.GraphAnimator import GraphAnimator
from graphMaker.CollectionRenderer import QueueRenderer
from graphMaker.ENodeStateColors import ENodeStateColors

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
        self.open_collection = deque([self.start_node])
        self.open_set = {self.start_node}
        self.node_states[self.start_node] = ENodeStateColors.OPEN

    def create_collection_renderer(self):
        return QueueRenderer()

    def prepare_memory_state(self, collection_items=None):
        if collection_items is None:
            collection_items = list(self.open_collection)
        return {"Nyílt": collection_items, "Zárt": self.closed_set}

    def generate_animation(self):
        self.highlight_pseudocode_lines(range(5))

        while self.open_collection:
            self.generate_frame(highlight_line=5)
            self.frame_id += 1

            current_node = self.open_collection.popleft()
            self.open_set.remove(current_node)
            self.node_states[current_node] = ENodeStateColors.CURRENT

            self.generate_frame(highlight_line=6)
            self.frame_id += 1

            if current_node == self.goal_node:
                self.generate_frame(highlight_line=7)
                self.frame_id += 1
                self.node_states[current_node] = ENodeStateColors.GOAL
                self.generate_frame(highlight_line=7)
                break

            self.generate_frame(highlight_line=8)
            self.frame_id += 1

            for child in self.children.get(current_node, []):
                self.generate_frame(highlight_line=9)
                self.frame_id += 1

                if child not in self.open_set and child not in self.closed_set:
                    self.node_states[child] = ENodeStateColors.OPEN
                    self.open_collection.append(child)
                    self.open_set.add(child)

                    self.generate_frame(highlight_line=10)
                    self.frame_id += 1
                    self.generate_frame(highlight_line=11)
                    self.frame_id += 1
                    self.generate_frame(highlight_line=12)
                    self.frame_id += 1

            self.node_states[current_node] = ENodeStateColors.CLOSED
            self.closed_set.add(current_node)
            self.visited.add(current_node)

            self.generate_frame(highlight_line=13)
            self.frame_id += 1
            self.generate_frame(highlight_line=14)
            self.frame_id += 1

        if not self.open_collection and current_node != self.goal_node:
            self.generate_frame(highlight_line=16)
            self.frame_id += 1