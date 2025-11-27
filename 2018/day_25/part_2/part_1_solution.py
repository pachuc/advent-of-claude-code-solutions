def solve(input_file='input.md'):
    """
    Solve the Four-Dimensional Constellation Grouping problem.

    Uses Union-Find algorithm to count connected components where points
    are connected if their Manhattan distance <= 3.
    """
    # Step 1: Parse input
    points = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                coords = [int(x) for x in line.split(',')]
                points.append(tuple(coords))

    n = len(points)

    # Handle empty input
    if n == 0:
        print(0)
        return 0

    # Step 2: Initialize Union-Find
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        """Find with path compression"""
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        """Union by rank"""
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1

    # Step 3: Manhattan distance function
    def manhattan_distance(p1, p2):
        """Calculate Manhattan distance in 4D space"""
        return sum(abs(p1[i] - p2[i]) for i in range(4))

    # Step 4: Build constellations by comparing all pairs
    for i in range(n):
        for j in range(i + 1, n):
            if manhattan_distance(points[i], points[j]) <= 3:
                union(i, j)

    # Step 5: Count distinct constellations
    num_constellations = len(set(find(i) for i in range(n)))

    # Step 6: Output
    print(num_constellations)
    return num_constellations


if __name__ == "__main__":
    solve()
