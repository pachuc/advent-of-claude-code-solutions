from solution import parse_input, solve_by_formula, solve_by_greedy, solve, count_elements

# Test on simple example first
print("="*60)
print("TEST 1: Simple Example (HOH)")
print("="*60)

simple_input = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

rules, target = parse_input(simple_input)
greedy_result = solve_by_greedy(rules, target)
auto_result = solve(simple_input, method='auto')

print(f"Greedy result: {greedy_result}")
print(f"Auto result: {auto_result}")
print(f"Expected: 3")
print(f"✓ PASSED" if auto_result == 3 else f"✗ FAILED")

# Test on actual input
print("\n" + "="*60)
print("TEST 2: Actual Input")
print("="*60)

with open('input.md', 'r') as f:
    input_text = f.read()

rules, target = parse_input(input_text)

# Analyze input
num_elements = count_elements(target)
num_rn = target.count('Rn')
num_ar = target.count('Ar')
num_y = target.count('Y')

print(f"Target molecule analysis:")
print(f"  Total length: {len(target)}")
print(f"  Number of elements: {num_elements}")
print(f"  Rn: {num_rn}")
print(f"  Ar: {num_ar}")
print(f"  Y: {num_y}")
print(f"  Rn and Ar balanced: {num_rn == num_ar}")

# Calculate using formula
formula_result = solve_by_formula(target)
print(f"\nFormula calculation:")
print(f"  {num_elements} - {num_rn} - {num_ar} - 2*{num_y} - 1 = {formula_result}")

# Get auto result
auto_result = solve(input_text, method='auto')
print(f"\nAuto solve result: {auto_result}")

# For AoC 2015 Day 19 Part 2, the formula is the correct approach
print(f"\n✓ FINAL ANSWER: {auto_result}")
