from solution import get_pattern, simulate_generation

print("=== Rule Application Verification ===\n")

# Test specific rules from the input
# Rule 1: .##.# => #
# Pattern .##.# at pot 5 requires: pot 3 empty, pot 4 plant, pot 5 plant, pot 6 empty, pot 7 plant
print("Test 1: Rule '.##.# => #'")
state = {4, 5, 7}
pattern = get_pattern(5, state)
print(f"State: {state}")
print(f"Pattern at pot 5: '{pattern}'")
print(f"Expected pattern: '.##.#'")
print(f"Pattern match: {'✓' if pattern == '.##.#' else '✗'}")

rules = {'.##.#': '#'}
next_state = simulate_generation(state, rules)
has_plant_at_5 = 5 in next_state
print(f"Pot 5 has plant in next generation: {has_plant_at_5}")
print(f"Pass: {'✓' if has_plant_at_5 else '✗'}\n")

# Rule 2: #..#. => .
# Pattern #..#. at pot 10 requires: pot 8 plant, pot 9 empty, pot 10 empty, pot 11 plant, pot 12 empty
print("Test 2: Rule '#..#. => .'")
state = {8, 11}
pattern = get_pattern(10, state)
print(f"State: {state}")
print(f"Pattern at pot 10: '{pattern}'")
print(f"Expected pattern: '#..#.'")
print(f"Pattern match: {'✓' if pattern == '#..#.' else '✗'}")

rules = {'#..#.': '.'}
next_state = simulate_generation(state, rules)
has_plant_at_10 = 10 in next_state
print(f"Pot 10 has plant in next generation: {has_plant_at_10}")
print(f"Pass: {'✓' if not has_plant_at_10 else '✗'}\n")

# Rule 3: #.#.# => #
# Pattern #.#.# at pot 0 requires: pot -2 plant, pot -1 empty, pot 0 plant, pot 1 empty, pot 2 plant
print("Test 3: Rule '#.#.# => #'")
state = {-2, 0, 2}
pattern = get_pattern(0, state)
print(f"State: {state}")
print(f"Pattern at pot 0: '{pattern}'")
print(f"Expected pattern: '#.#.#'")
print(f"Pattern match: {'✓' if pattern == '#.#.#' else '✗'}")

rules = {'#.#.#': '#'}
next_state = simulate_generation(state, rules)
has_plant_at_0 = 0 in next_state
print(f"Pot 0 has plant in next generation: {has_plant_at_0}")
print(f"Pass: {'✓' if has_plant_at_0 else '✗'}\n")

print("=== All Rule Tests Complete ===")
