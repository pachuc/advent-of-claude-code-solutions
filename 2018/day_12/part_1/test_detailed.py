from solution import parse_input, simulate_generation

# Parse input
initial_state, rules = parse_input('input.md')

# Verify parsing
print("=== Input Parsing Verification ===")
print(f"Initial state has {len(initial_state)} plants")
print(f"Initial state range: {min(initial_state)} to {max(initial_state)}")
print(f"Number of rules: {len(rules)}")
print(f"Sample rules:")
for i, (pattern, result) in enumerate(list(rules.items())[:5]):
    print(f"  {pattern} => {result}")

# Verify initial state matches the input
with open('input.md', 'r') as f:
    first_line = f.readline().strip()
    state_string = first_line.split(': ')[1]
    expected_plants = state_string.count('#')
    print(f"\nExpected {expected_plants} plants in initial state")
    print(f"Parsed {len(initial_state)} plants in initial state")
    print(f"Match: {'✓' if expected_plants == len(initial_state) else '✗'}")

# Run simulation with detailed tracking
print("\n=== Simulation Progress ===")
state = initial_state
print(f"Gen  0: {len(state):3d} plants, range [{min(state):4d}, {max(state):4d}], sum = {sum(state):6d}")

for generation in range(1, 21):
    state = simulate_generation(state, rules)
    if len(state) > 0:
        print(f"Gen {generation:2d}: {len(state):3d} plants, range [{min(state):4d}, {max(state):4d}], sum = {sum(state):6d}")
    else:
        print(f"Gen {generation:2d}: No plants remaining!")
        break

# Final result
print(f"\n=== Final Result ===")
print(f"After 20 generations: {sum(state)}")
