from collections import deque


def parse_input(lines):
    """Parse input lines into an adjacency list graph.

    Args:
        lines: List of strings in format "program_id <-> neighbor1, neighbor2, ..."

    Returns:
        Dictionary mapping program_id to list of connected program IDs
    """
    graph = {}
    for line in lines:
        # Skip empty lines
        line = line.strip()
        if not line:
            continue

        # Split by '<->'
        parts = line.split('<->')
        program_id = int(parts[0].strip())

        # Split connections by comma
        connections = [int(x.strip()) for x in parts[1].split(',')]
        graph[program_id] = connections

    return graph


def find_connected_group(graph, start_node):
    """Find all nodes connected to start_node using BFS.

    Args:
        graph: Adjacency list representation of the graph
        start_node: Starting node ID

    Returns:
        Number of nodes in the connected component containing start_node
    """
    queue = deque([start_node])
    visited = set()

    while queue:
        current = queue.popleft()

        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)

        # Add all unvisited neighbors to queue
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append(neighbor)

    return len(visited)


def main():
    """Main function to solve the problem."""
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse graph
    graph = parse_input(lines)

    # Find connected group containing program 0
    count = find_connected_group(graph, 0)

    # Output result
    print(count)


if __name__ == "__main__":
    main()
