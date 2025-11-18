from solution import parse_input, find_connected_group


def count_all_groups_with_sizes(graph):
    """Debug version that prints detailed group information."""
    visited_global = set()
    group_sizes = []

    for node in graph:
        if node not in visited_global:
            group_nodes = find_connected_group(graph, node)
            visited_global.update(group_nodes)
            group_sizes.append(len(group_nodes))

    print(f"Group sizes (largest first): {sorted(group_sizes, reverse=True)[:20]}")
    print(f"Total nodes covered: {sum(group_sizes)}")
    print(f"Total nodes in graph: {len(graph)}")
    print(f"One group has size 239 (Part 1 answer): {239 in group_sizes}")

    return len(group_sizes)


# Read and test
with open('input.md', 'r') as f:
    lines = f.readlines()
graph = parse_input(lines)
total = count_all_groups_with_sizes(graph)
print(f"\nTotal groups: {total}")
