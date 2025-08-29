from collections import deque


# Example AST node class
class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []


def construct_symbol_name(stack):
    # Start with the prefix
    prefix = 'nft_'

    # If stack has only one entry (root), return prefix
    if len(stack) <= 1:
        return prefix

    # Convert node names to snake_case, excluding first entry
    names = []
    for node in list(stack)[1:]:
        snake_case_name = node.name.lower().replace(' ', '_')
        names.append(snake_case_name)

    # Join names with underscores and append to prefix
    return prefix + '_'.join(names)


def traverse_ast(root_node, hidden_prefix='.'):
    if not isinstance(root_node, Node):
        print(f"Node {root_node} is not valid; aborted.")
        return

    def recursive_traverse(node, stack=deque()):
        stack.append(node)
        # Print stack contents, skipping the first entry if stack has more than one
        print(f"Stack Contents: {[n.name for n in list(stack)[1:]] if len(stack) > 1 else []}")
        print(f"Symbol Name: {construct_symbol_name(stack)}")
        print(f"Current Node: {node.name}")
        try:
            for child in node.children:
                if child.name.startswith(hidden_prefix):
                    continue
                if not child.children:  # Leaf node (like a file)
                    print(f"  Leaf: {child.name}")
                else:  # Non-leaf node (like a directory)
                    recursive_traverse(child, stack)
        except Exception as e:
            print(f"  Error processing node {node.name}: {e}")
        stack.pop()

    recursive_traverse(root_node)


# Example usage
root = Node('Project', [
    Node('.hidden'),  # Skipped due to hidden_prefix
    Node('Sub Dir1', [Node('File1'), Node('SubDir2', [Node('File2')])])
])
traverse_ast(root)