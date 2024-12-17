from graphMaker.GraphAnimator import GraphAnimator

class DepthFirstGraphAnimator(GraphAnimator):
    def __init__(self, start_node, goal_node, children):
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
            "return „Nincs megoldás”"
        ]
        super().__init__(pseudocode, start_node, goal_node, children)

    def generate_animation(self):
        stack = [self.start_node]
        frame_id = 0

        while stack:
            current_node = stack.pop()

            highlight_line = 4 if current_node != self.goal_node else 5

            self.node_states[current_node] = 'red'

            frame_filename = f'{self.frames_dir}/frame_{frame_id}.png'
            self.create_frame(frame_filename, highlight_line)
            frame_id += 1

            if current_node == self.goal_node:
                self.node_states[current_node] = 'black'
                frame_filename = f'{self.frames_dir}/frame_{frame_id}.png'
                self.create_frame(frame_filename, 5)
                break

            self.node_states[current_node] = 'black'
            self.visited.add(current_node)

            for child in reversed(self.children.get(current_node, [])):
                if child not in self.visited and child not in stack:
                    stack.append(child)
