import networkx as nx
import matplotlib.pyplot as plt
import os
from PIL import Image


def create_graph_frame(node_colors, filename, node_labels, pseudocode, highlight_line=None):

    G = nx.DiGraph()

    pos = {
        '0': (0.5, 1),
        '1': (0.4, 0.7),
        '2a': (0.6, 0.7),
        '2b': (0.3, 0.4),
        '2c': (0.5, 0.4),
        '3': (0.4, 0.2),
        'T': (0.4, 0)
    }

    edges = [
        ('0', '1'), ('0', '2a'),
        ('1', '2b'), ('1', '2c'),
        ('1', '2a'),
        ('2b', '3'), ('2c', '3'),
        ('3', 'T')
    ]
    G.add_edges_from(edges)

    plt.figure(figsize=(5, 10))

    nx.draw(
        G, pos,
        labels=node_labels,
        node_color=[node_colors[node] for node in G.nodes()],
        node_size=1000,
        with_labels=True,
        font_color='white',
        font_size=16,
        arrows=True
    )

    for i, line in enumerate(pseudocode):
        color = 'red' if i == highlight_line else 'black'
        plt.text(0.75, 1 - i * 0.08, line, fontsize=12, color=color, family='monospace', va='top')


    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    return filename


if not os.path.exists('graph_frames'):
    os.makedirs('graph_frames')

frames = []
node_states = {node: 'yellow' for node in ['0', '1', '2a', '2b', '2c', '3', 'T']}
visited = set()
open_list = []

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

start_node = '0'
goal_node = 'T'

open_list.append(start_node)

frame_id = 0
while open_list:
    current_node = open_list.pop()
    node_states[current_node] = 'red'

    highlight_line = 4 if current_node != goal_node else 5

    frame_filename = f'graph_frames/frame_{frame_id}.png'
    frames.append(create_graph_frame(node_states, frame_filename, {n: n for n in node_states}, pseudocode, highlight_line))
    frame_id += 1

    if current_node == goal_node:
        node_states[current_node] = 'black'
        frame_filename = f'graph_frames/frame_{frame_id}.png'
        frames.append(create_graph_frame(node_states, frame_filename, {n: n for n in node_states}, pseudocode, 5))
        break

    node_states[current_node] = 'black'
    visited.add(current_node)

    children = {
        '0': ['1', '2a'],
        '1': ['2b', '2c'],
        '2a': ['2c'],
        '2b': ['3'],
        '2c': ['3'],
        '3': ['T'],
        'T': []
    }
    for child in reversed(children[current_node]):
        if child not in visited and child not in open_list:
            open_list.append(child)

images = [Image.open(frame) for frame in frames]
images[0].save(
    'graph_animation_with_pseudocode.gif',
    save_all=True,
    append_images=images[1:],
    duration=1000,
    loop=0
)

print("GIF with pseudocode has been created as 'graph_animation_with_pseudocode.gif' in your current directory!")

for file in frames:
    os.remove(file)
os.rmdir('graph_frames')