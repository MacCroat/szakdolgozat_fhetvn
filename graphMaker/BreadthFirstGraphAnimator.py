from collections import deque
from graphMaker.GraphAnimator import GraphAnimator

class BreadthFirstGraphAnimator(GraphAnimator):
    def __init__(self, start_node, goal_node, children):
        """
        Initialize the BFS animator with start node, goal node, and children mapping.
        """
        pseudocode = [
            "StartNode := k",
            "OpenList := {StartNode}",
            "ClosedList := {}",
            "While OpenList is not empty do",
            "  CurrentNode := OpenList.dequeue()",
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
        self.queue = deque()

    def _create_and_save_frame(self, frame_id, highlight_line):
        """
        Helper function to create and save the current animation frame.
        """
        frame_filename = f"{self.frames_dir}/frame_{frame_id}.png"
        self.create_frame(frame_filename, highlight_line)

    def generate_animation(self):
        """
        Generate BFS animation frames by traversing the graph.
        """
        self.queue.append(self.start_node)
        frame_id = 0

        while self.queue:
            # Dequeue the current node
            current_node = self.queue.popleft()
            self.node_states[current_node] = 'red'

            # Highlight dequeuing in the pseudocode
            self._create_and_save_frame(frame_id, highlight_line=4)
            frame_id += 1

            # Check if the current node is the goal
            if current_node == self.goal_node:
                self.node_states[current_node] = 'black'
                self._create_and_save_frame(frame_id, highlight_line=5)
                break

            # Mark current node as visited
            self.node_states[current_node] = 'black'
            self.visited.add(current_node)

            # Explore child nodes
            for child in self.children[current_node]:
                if child not in self.visited and child not in self.queue:
                    self.queue.append(child)

            # Highlight node addition to ClosedList
            self._create_and_save_frame(frame_id, highlight_line=10)
            frame_id += 1
