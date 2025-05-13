import matplotlib.pyplot as plt
import networkx as nx

# Function to add nodes and edges from a BST tuple
def add_edges(G, node_tuple):
    node, left, right = node_tuple
    if left:
        G.add_edge(node, left[0])
        add_edges(G, left)
    if right:
        G.add_edge(node, right[0])
        add_edges(G, right)

# Function to perform in-order traversal and color nodes
def inorder_traversal(node, visit_order):
    if node[1]:  # Left subtree
        inorder_traversal(node[1], visit_order)
    visit_order.append(node[0])
    if node[2]:  # Right subtree
        inorder_traversal(node[2], visit_order)

# Function to perform pre-order traversal and color nodes
def preorder_traversal(node, visit_order):
    visit_order.append(node[0])
    if node[1]:  # Left subtree
        preorder_traversal(node[1], visit_order)
    if node[2]:  # Right subtree
        preorder_traversal(node[2], visit_order)

# Function to insert a node in BST
def insert_node(bst, value):
    if bst is None:
        return (value, None, None)
    node, left, right = bst
    if value < node:
        return (node, insert_node(left, value), right)
    elif value > node:
        return (node, left, insert_node(right, value))
    return bst

# Define the initial BST as nested tuples: (value, left_subtree, right_subtree)
bst = (10,
       (5, (3, None, None), (7, None, None)),
       (15, None, (18, None, None)))

# Create the directed graph
G = nx.DiGraph()
add_edges(G, bst)

# Layout using graphviz 'dot' for tree-like appearance
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

# Function to draw the tree
def draw_tree(G, pos, title="Binary Search Tree"):
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color='lightblue', font_size=10, arrows=False)
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Initial drawing of the tree
draw_tree(G, pos)

# Add a new node (dynamically)
new_value = 12
bst = insert_node(bst, new_value)

# Update the graph with the new tree structure
G.clear()  # Clear the previous graph
add_edges(G, bst)

# Update the drawing with the new tree
draw_tree(G, pos, title=f"Binary Search Tree (After Insertion of {new_value})")

# Traverse the tree (In-order and Pre-order)
inorder_order = []
inorder_traversal(bst, inorder_order)

preorder_order = []
preorder_traversal(bst, preorder_order)

print(f"In-order Traversal: {inorder_order}")
print(f"Pre-order Traversal: {preorder_order}")
