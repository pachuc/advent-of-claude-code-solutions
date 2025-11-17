#!/usr/bin/env python3
"""
Test script to verify the solution correctness.
"""

from solution import parse_input, count_elements, solve_by_formula, solve_by_greedy, solve_by_bfs, solve


def test_simple_example():
    """Test on the simple example from the problem description."""
    print("="*60)
    print("Testing Simple Example (HOH)")
    print("="*60)

    input_text = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(input_text)

    print(f"Target: {target}")
    print(f"Rules: {len(rules)}")

    # Test greedy
    greedy_result = solve_by_greedy(rules, target)
    print(f"Greedy result: {greedy_result}")
    print(f"Expected: 3")

    if greedy_result == 3:
        print("✓ Simple example PASSED")
        return True
    else:
        print("✗ Simple example FAILED")
        return False


def test_formula_calculation():
    """Test formula calculation on actual input."""
    print("\n" + "="*60)
    print("Testing Formula Calculation")
    print("="*60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    print(f"Target length: {len(target)}")

    # Count elements
    num_elements = count_elements(target)
    num_rn = target.count('Rn')
    num_ar = target.count('Ar')
    num_y = target.count('Y')

    print(f"Elements: {num_elements}")
    print(f"Rn: {num_rn}")
    print(f"Ar: {num_ar}")
    print(f"Y: {num_y}")

    # Calculate formula
    steps = num_elements - num_rn - num_ar - 2 * num_y - 1

    print(f"\nFormula: {num_elements} - {num_rn} - {num_ar} - 2*{num_y} - 1")
    print(f"       = {num_elements} - {num_rn} - {num_ar} - {2*num_y} - 1")
    print(f"       = {steps}")

    # Test solve_by_formula
    formula_result = solve_by_formula(target)
    print(f"\nsolve_by_formula result: {formula_result}")

    if formula_result == steps:
        print("✓ Formula calculation PASSED")
        return True, steps
    else:
        print("✗ Formula calculation FAILED")
        return False, steps


def test_greedy_on_actual():
    """Test greedy on actual input (for comparison)."""
    print("\n" + "="*60)
    print("Testing Greedy on Actual Input")
    print("="*60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    print("Running greedy backward reduction...")
    greedy_result = solve_by_greedy(rules, target)

    print(f"Greedy result: {greedy_result}")

    if greedy_result > 0:
        print("✓ Greedy found a solution")
        return True, greedy_result
    else:
        print("✗ Greedy failed to find solution")
        return False, greedy_result


def test_verification():
    """Verify the solution by backward reduction."""
    print("\n" + "="*60)
    print("Testing Solution Verification")
    print("="*60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    # Get greedy result
    steps = solve_by_greedy(rules, target)
    print(f"Testing {steps} steps to reduce '{target[:30]}...' to 'e'")

    # Try to reduce
    current = target
    reversed_rules = [(tgt, src) for src, tgt in rules]
    reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

    for i in range(steps):
        found = False
        for pattern, replacement in reversed_rules:
            if pattern in current:
                old_len = len(current)
                current = current.replace(pattern, replacement, 1)
                new_len = len(current)
                found = True
                if i < 3 or i >= steps - 3:  # Show first and last few steps
                    print(f"  Step {i+1}: length {old_len} -> {new_len}")
                elif i == 3:
                    print(f"  ...")
                break

        if not found:
            print(f"✗ Step {i+1}: No rule applies to molecule of length {len(current)}")
            return False

    if current == 'e':
        print(f"✓ Successfully reduced to 'e' in {steps} steps")
        return True
    else:
        print(f"✗ After {steps} steps, reached '{current}', not 'e'")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VERIFICATION TEST SUITE")
    print("="*60)

    # Test 1: Simple example
    simple_passed = test_simple_example()

    # Test 2: Formula calculation
    formula_passed, formula_result = test_formula_calculation()

    # Test 3: Greedy on actual
    greedy_passed, greedy_result = test_greedy_on_actual()

    # Test 4: Verification
    verification_passed = test_verification()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Simple example: {'PASSED ✓' if simple_passed else 'FAILED ✗'}")
    print(f"Formula calculation: {'PASSED ✓' if formula_passed else 'FAILED ✗'}")
    print(f"Greedy on actual: {'PASSED ✓' if greedy_passed else 'FAILED ✗'}")
    print(f"Solution verification: {'PASSED ✓' if verification_passed else 'FAILED ✗'}")

    print("\n" + "="*60)
    print("RESULTS COMPARISON")
    print("="*60)
    print(f"Formula result: {formula_result}")
    print(f"Greedy result: {greedy_result}")

    if formula_result == greedy_result:
        print("✓ Formula and Greedy AGREE - High confidence!")
    else:
        print(f"⚠ Formula and Greedy differ by {abs(formula_result - greedy_result)}")

    print("\n" + "="*60)
    print("FINAL VERDICT")
    print("="*60)

    all_passed = simple_passed and formula_passed and greedy_passed and verification_passed

    if all_passed and formula_result == greedy_result:
        print(f"✓ ALL TESTS PASSED")
        print(f"✓ SOLUTION VERIFIED: {formula_result} steps")
        return formula_result
    else:
        print("✗ SOME TESTS FAILED - Review needed")
        return None


if __name__ == '__main__':
    result = main()
    if result:
        print(f"\n>>> Final Answer: {result}")
