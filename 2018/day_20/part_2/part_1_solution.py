from collections import defaultdict, deque


def parse_regex_and_build_graph(regex):
    """
    Parse the regex and build a set of doors connecting rooms.

    Args:
        regex: The regex string (without ^ and $)

    Returns:
        A set of frozensets, where each frozenset contains two adjacent room positions
    """
    doors = set()
    current_positions = {(0, 0)}
    stack = []
    directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

    for char in regex:
        if char in 'NSEW':
            dx, dy = directions[char]
            new_positions = set()
            for x, y in current_positions:
                new_x, new_y = x + dx, y + dy
                doors.add(frozenset([(x, y), (new_x, new_y)]))
                new_positions.add((new_x, new_y))
            current_positions = new_positions

        elif char == '(':
            # Push current positions and empty branch endpoints list
            stack.append((current_positions, []))

        elif char == '|':
            # Save current endpoints and restore starting positions
            starting_positions, branch_endpoints = stack[-1]
            branch_endpoints.append(current_positions)
            current_positions = starting_positions.copy()

        elif char == ')':
            # Merge all branch endpoints
            starting_positions, branch_endpoints = stack.pop()
            branch_endpoints.append(current_positions)
            current_positions = set()
            for endpoints in branch_endpoints:
                current_positions.update(endpoints)

    return doors


def build_adjacency_graph(doors):
    """
    Build an adjacency graph from the doors set.

    Args:
        doors: Set of frozensets representing doors between rooms

    Returns:
        A defaultdict(set) representing the adjacency graph
    """
    graph = defaultdict(set)
    for door in doors:
        pos1, pos2 = door
        graph[pos1].add(pos2)
        graph[pos2].add(pos1)
    return graph


def find_max_distance(graph, start=(0, 0)):
    """
    Find the maximum shortest path distance from start to any room.

    Args:
        graph: Adjacency graph (defaultdict of sets)
        start: Starting position (default: (0, 0))

    Returns:
        The maximum distance (number of doors) to reach any room
    """
    queue = deque([(start, 0)])
    visited = {start}
    max_distance = 0

    while queue:
        pos, dist = queue.popleft()
        max_distance = max(max_distance, dist)

        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return max_distance


def solve(input_text):
    """
    Solve the problem given the input text.

    Args:
        input_text: The regex string including ^ and $

    Returns:
        The maximum number of doors needed to reach the furthest room
    """
    # Strip whitespace and remove ^ and $
    regex = input_text.strip()[1:-1]

    # Build the doors set by parsing the regex
    doors = parse_regex_and_build_graph(regex)

    # Build the adjacency graph
    graph = build_adjacency_graph(doors)

    # Find the maximum distance using BFS
    max_dist = find_max_distance(graph)

    return max_dist


if __name__ == '__main__':
    # Read input from file
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Maximum number of doors: {result}")
