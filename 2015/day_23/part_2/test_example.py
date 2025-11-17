from solution import parse_instructions, simulate

# Test Case 1: Example from problem description
print("Test Case 1: Example program with a=0")
test_instructions_1 = [
    {"op": "inc", "reg": "a"},
    {"op": "jio", "reg": "a", "offset": 2},
    {"op": "tpl", "reg": "a"},
    {"op": "inc", "reg": "a"}
]
registers = simulate(test_instructions_1, initial_a=0, initial_b=0, verbose=True)
print(f"Expected: a=2, b=0")
print(f"Got: a={registers['a']}, b={registers['b']}")
print(f"Test PASSED: {registers['a'] == 2 and registers['b'] == 0}\n")

# Test Case 2: Initial condition test (jio behavior)
print("Test Case 2: jio test with a=0")
test_instructions_2 = [
    {"op": "jio", "reg": "a", "offset": 2},
    {"op": "inc", "reg": "b"},
    {"op": "inc", "reg": "b"}
]
registers = simulate(test_instructions_2, initial_a=0, initial_b=0, verbose=True)
print(f"Expected: b=2 (a≠1, so doesn't jump)")
print(f"Got: b={registers['b']}")
print(f"Test PASSED: {registers['b'] == 2}\n")

# Test Case 3: jio test with a=1
print("Test Case 3: jio test with a=1")
test_instructions_3 = [
    {"op": "jio", "reg": "a", "offset": 2},
    {"op": "inc", "reg": "b"},
    {"op": "inc", "reg": "b"}
]
registers = simulate(test_instructions_3, initial_a=1, initial_b=0, verbose=True)
print(f"Expected: b=1 (a=1, so jumps to PC=2)")
print(f"Got: b={registers['b']}")
print(f"Test PASSED: {registers['b'] == 1}\n")

# Test Case 4: Jump offset test
print("Test Case 4: Jump offset semantics")
test_instructions_4 = [
    {"op": "jmp", "offset": 2},
    {"op": "inc", "reg": "b"},
    {"op": "inc", "reg": "a"}
]
registers = simulate(test_instructions_4, initial_a=0, initial_b=0, verbose=True)
print(f"Expected: a=1, b=0 (jump from PC=0 to PC=2, skip inc b)")
print(f"Got: a={registers['a']}, b={registers['b']}")
print(f"Test PASSED: {registers['a'] == 1 and registers['b'] == 0}\n")

# Test Case 5: All instruction types
print("Test Case 5: All instruction types")
test_instructions_5 = [
    {"op": "inc", "reg": "a"},  # a=1
    {"op": "tpl", "reg": "a"},  # a=3
    {"op": "inc", "reg": "a"},  # a=4
    {"op": "hlf", "reg": "a"},  # a=2
    {"op": "jie", "reg": "a", "offset": 2},  # a is even, jump to PC=7
    {"op": "inc", "reg": "b"},  # skipped
    {"op": "inc", "reg": "b"}   # PC=7, executed
]
registers = simulate(test_instructions_5, initial_a=0, initial_b=0, verbose=True)
print(f"Expected: a=2, b=1")
print(f"Got: a={registers['a']}, b={registers['b']}")
print(f"Test PASSED: {registers['a'] == 2 and registers['b'] == 1}\n")
