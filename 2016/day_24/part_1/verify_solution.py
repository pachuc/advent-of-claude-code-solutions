from solution import parse_grid, calculate_distances, solve_tsp

# Read actual input
with open('input.md', 'r') as f:
    grid = [line.rstrip('\n') for line in f if line and not line.startswith('```')]

locations = parse_grid(grid)
distances, location_mapping = calculate_distances(grid, locations)

# Test 1: Check distance matrix symmetry
print('Test 1: Distance Matrix Symmetry')
is_symmetric = True
for i in range(len(distances)):
    for j in range(len(distances)):
        if abs(distances[i][j] - distances[j][i]) > 0.001:
            print(f'  Not symmetric: distances[{i}][{j}]={distances[i][j]}, distances[{j}][{i}]={distances[j][i]}')
            is_symmetric = False
if is_symmetric:
    print('  PASSED: Distance matrix is symmetric')
else:
    print('  FAILED: Distance matrix is not symmetric')

# Test 2: Check for unreachable locations
print('\nTest 2: All Locations Reachable')
has_unreachable = False
for i in range(len(distances)):
    for j in range(len(distances)):
        if distances[i][j] == float('inf'):
            print(f'  Unreachable: location {i} to {j}')
            has_unreachable = True
if not has_unreachable:
    print('  PASSED: All locations are reachable from each other')
else:
    print('  FAILED: Some locations are unreachable')

# Test 3: Check location 0 exists
print('\nTest 3: Starting Location Exists')
if 0 in locations:
    print('  PASSED: Location 0 exists')
else:
    print('  FAILED: Location 0 does not exist')

# Test 4: Check answer is reasonable (positive and within bounds)
min_steps = solve_tsp(distances, location_mapping, start_location=0)
print(f'\nTest 4: Answer Reasonableness')
print(f'  Answer: {min_steps}')
if min_steps > 0 and min_steps < 1000:
    print('  PASSED: Answer is in reasonable range')
else:
    print('  FAILED: Answer seems unreasonable')

print(f'\n=== FINAL ANSWER: {min_steps} ===')
