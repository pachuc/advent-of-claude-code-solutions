from solution import simulate_marble_game

# Test cases from Part 1
test_cases = [
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
]

print("Running Part 1 example test cases...")
all_passed = True

for num_players, last_marble, expected in test_cases:
    result = simulate_marble_game(num_players, last_marble)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {num_players} players, {last_marble} marbles -> {result} (expected {expected})")
    if not passed:
        all_passed = False

if all_passed:
    print("\nAll test cases PASSED!")
else:
    print("\nSome test cases FAILED!")
