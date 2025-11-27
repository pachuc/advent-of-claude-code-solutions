from solution import simulate_marble_game

# Test all 6 example cases from the problem
test_cases = [
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
]

print("Testing example cases:")
all_passed = True
for players, last_marble, expected in test_cases:
    result = simulate_marble_game(players, last_marble)
    passed = result == expected
    status = "✓" if passed else "✗"
    print(f"{status} {players} players, {last_marble} marbles: expected {expected}, got {result}")
    if not passed:
        all_passed = False

if all_passed:
    print("\nAll example test cases passed!")
else:
    print("\nSome test cases failed!")

# Test edge cases
print("\nTesting edge cases:")
edge_cases = [
    (1, 0, 0, "Only marble 0, no scoring"),
    (1, 22, 0, "No multiples of 23, no scoring"),
    (1, 23, 32, "First scoring at marble 23"),
]

for players, last_marble, expected, description in edge_cases:
    result = simulate_marble_game(players, last_marble)
    passed = result == expected
    status = "✓" if passed else "✗"
    print(f"{status} {description}: expected {expected}, got {result}")
    if not passed:
        all_passed = False

# Test actual input
print("\nActual input:")
result = simulate_marble_game(463, 71787)
print(f"463 players, 71787 marbles → {result}")

if all_passed:
    print("\n✓ All tests passed!")
    exit(0)
else:
    print("\n✗ Some tests failed!")
    exit(1)
