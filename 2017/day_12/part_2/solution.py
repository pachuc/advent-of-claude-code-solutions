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
        Set of all nodes in the connected component containing start_node
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

    return visited


def count_all_groups(graph):
    """Count total number of connected components in the graph.

    Args:
        graph: Adjacency list representation

    Returns:
        Integer count of distinct groups
    """
    visited_global = set()  # Track all visited nodes across all groups
    group_count = 0

    # Iterate through all nodes in the graph
    for node in graph:
        # If node hasn't been assigned to a group yet
        if node not in visited_global:
            # Find all nodes in this component
            group_nodes = find_connected_group(graph, node)

            # Mark all nodes in this group as visited
            visited_global.update(group_nodes)

            # Increment group counter
            group_count += 1

    return group_count


def main():
    """Main function to solve the problem."""
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse graph
    graph = parse_input(lines)

    # Count all groups
    total_groups = count_all_groups(graph)

    # Output result
    print(total_groups)


if __name__ == "__main__":
    main()
