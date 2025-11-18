"""Test script for the evolved virus simulation."""

from solution import parse_input, simulate_virus_evolved, CLEAN, WEAKENED, INFECTED, FLAGGED

# Test 1: Small example with 100 bursts
print("Test 1: Small example with 100 bursts")
states, center = parse_input('test_input.txt')
result = simulate_virus_evolved(states, center, 100)
print(f"Result: {result}")
print(f"Expected: 26")
print(f"Test 1: {'PASS' if result == 26 else 'FAIL'}")
print()

# Test 2: Small example with 10,000,000 bursts
print("Test 2: Small example with 10,000,000 bursts")
states, center = parse_input('test_input.txt')
result = simulate_virus_evolved(states, center, 10000000)
print(f"Result: {result}")
print(f"Expected: 2,511,944")
print(f"Test 2: {'PASS' if result == 2511944 else 'FAIL'}")
