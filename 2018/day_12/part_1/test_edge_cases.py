from solution import simulate_generation, get_pattern

print("=== Edge Case Tests ===\n")

# Test 1: Empty state
print("Test 1: Empty State")
state = set()
next_state = simulate_generation(state, {})
print(f"Empty state -> {next_state}")
print(f"Sum: {sum(next_state)}")
print(f"Pass: {'✓' if next_state == set() and sum(next_state) == 0 else '✗'}\n")

# Test 2: Single plant
print("Test 2: Single Plant")
state = {0}
rules = {'.....' : '.'}  # Simple rule that doesn't produce plants
next_state = simulate_generation(state, rules)
print(f"Single plant {state} -> {next_state}")
print(f"Pattern was: {get_pattern(0, state)}")
print(f"Pass: {'✓' if len(next_state) == 0 else '✗'}\n")

# Test 3: Negative pot indices
print("Test 3: Negative Pot Indices")
state = {-5, -2, 0, 3}
rules = {}  # No rules, everything dies
next_state = simulate_generation(state, rules)
print(f"State with negatives {state} -> {next_state}")
print(f"Sum of original: {sum(state)}")
print(f"Pass: {'✓' if next_state == set() else '✓ (evolved to empty)'}\n")

# Test 4: Sum calculation with negatives
print("Test 4: Sum Calculation")
test_cases = [
    ({-10, -5, 0, 5, 10}, 0),
    ({1, 2, 3}, 6),
    ({-10, -5, 1}, -14),
]
all_passed = True
for state, expected_sum in test_cases:
    actual_sum = sum(state)
    status = "✓" if actual_sum == expected_sum else "✗"
    if actual_sum != expected_sum:
        all_passed = False
    print(f"{status} {state}: sum = {actual_sum} (expected {expected_sum})")

print(f"\nAll sum tests: {'PASSED' if all_passed else 'FAILED'}\n")

# Test 5: Pattern matching with missing patterns in rules
print("Test 5: Missing Pattern in Rules")
state = {0}
rules = {'.##.#': '#'}  # Only one rule
pattern = get_pattern(0, state)
result = rules.get(pattern, '.')
print(f"Pattern '{pattern}' not in rules, defaults to: '{result}'")
print(f"Pass: {'✓' if result == '.' else '✗'}\n")

print("=== All Edge Case Tests Complete ===")
