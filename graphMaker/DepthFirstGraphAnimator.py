from graphMaker.GraphAnimator import GraphAnimator

class DepthFirstGraphAnimator(GraphAnimator):
    def __init__(self, start_node, goal_node, children):
        pseudocode = [
            "StartNode := k",
            "OpenList := {StartNode}",
            "ClosedList := {}",
            "While OpenList is not empty do",
            "  CurrentNode := OpenList.pop()",
            "  If CurrentNode == Goal then return Success",
            "  Mark CurrentNode as visited",
            "  For each child of CurrentNode do",
            "      If child is not visited then",
            "          Add child to OpenList",
            "  Add CurrentNode to ClosedList",
            "End While",
            "Return Failure"
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
