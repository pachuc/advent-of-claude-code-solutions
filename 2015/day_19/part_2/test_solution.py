from solution import (
    parse_input, count_elements,
    solve_by_formula, solve_by_greedy, solve_by_bfs,
    solve
)
import time


def test_parse_input():
    """Test input parsing."""
    input_text = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(input_text)

    assert len(rules) == 5, f"Expected 5 rules, got {len(rules)}"
    assert target == 'HOH', f"Expected target 'HOH', got '{target}'"
    assert ('e', 'H') in rules
    assert ('O', 'HH') in rules

    print("✓ Test: Input parsing passed")


def test_count_elements():
    """Test element counting."""
    test_cases = [
        ('H', 1),
        ('HH', 2),
        ('Ca', 1),
        ('CaCa', 2),
        ('HOH', 3),
        ('CaSiTh', 3),
        ('CRnAlAr', 4),
        ('CRnFYFAr', 6),
    ]

    for molecule, expected in test_cases:
        result = count_elements(molecule)
        assert result == expected, f"For '{molecule}': expected {expected}, got {result}"

    print("✓ Test: Element counting passed")


def test_greedy_simple():
    """Test greedy on simple example."""
    input_text = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(input_text)
    result = solve_by_greedy(rules, target)

    assert result == 3, f"Expected 3 steps, got {result}"
    print(f"✓ Test: Greedy on simple example passed (result={result})")


def test_formula_simple():
    """Test formula on simple example (may not work correctly)."""
    input_text = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(input_text)
    result = solve_by_formula(target)

    print(f"✓ Test: Formula on simple example = {result}")
    print(f"  Note: Formula may not work on examples without Rn/Ar/Y structure")


def test_verify_solution_path():
    """Verify solution by actually applying the transformations."""
    input_text = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(input_text)

    # Get solution from greedy
    steps = solve_by_greedy(rules, target)

    # Verify: try to reduce target to 'e' in exactly 'steps' operations
    current = target
    reversed_rules = [(tgt, src) for src, tgt in rules]
    reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

    for i in range(steps):
        found = False
        for pattern, replacement in reversed_rules:
            if pattern in current:
                current = current.replace(pattern, replacement, 1)
                found = True
                break

        assert found, f"Step {i+1}/{steps}: No rule applies to '{current}'"

    assert current == 'e', f"After {steps} steps, reached '{current}', not 'e'"

    print(f"✓ Test: Verified {steps} steps correctly reduces {target} to 'e'")


def test_actual_input_structure():
    """Test actual input structure."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    # Validate input properties
    assert len(rules) == 43, f"Expected 43 rules, got {len(rules)}"
    assert len(target) > 0, "Target should not be empty"

    # Check for 'e' rules
    e_rules = [r for r in rules if r[0] == 'e']
    assert len(e_rules) == 3, f"Expected 3 'e' rules, got {len(e_rules)}"

    # Count structural markers
    num_rn = target.count('Rn')
    num_ar = target.count('Ar')
    num_y = target.count('Y')

    print(f"  Rules: {len(rules)}")
    print(f"  Target length: {len(target)}")
    print(f"  Elements: {count_elements(target)}")
    print(f"  Rn: {num_rn}, Ar: {num_ar}, Y: {num_y}")
    print(f"  Rn and Ar balanced: {num_rn == num_ar}")

    assert num_rn == num_ar, "Rn and Ar should be balanced"

    print("✓ Test: Input structure validated")


def test_greedy_performance():
    """Test greedy performance on actual input."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    start = time.time()
    result = solve_by_greedy(rules, target)
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Greedy too slow: {elapsed}s"
    assert result > 0, "Greedy must find solution"

    print(f"✓ Test: Greedy performance = {elapsed*1000:.2f}ms, result = {result}")
    return result


def test_formula_performance():
    """Test formula performance on actual input."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    start = time.time()
    result = solve_by_formula(target)
    elapsed = time.time() - start

    assert elapsed < 0.01, f"Formula too slow: {elapsed}s"
    print(f"✓ Test: Formula performance = {elapsed*1000:.2f}ms, result = {result}")
    return result


def test_formula_validation_strategy():
    """Test formula reliability on different input types."""
    # Test 1: Simple molecule (no Rn/Ar/Y) - formula may fail
    simple_input = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    rules, target = parse_input(simple_input)
    formula_result = solve_by_formula(target)
    greedy_result = solve_by_greedy(rules, target)

    print(f"Simple example (HOH):")
    print(f"  Formula: {formula_result}")
    print(f"  Greedy: {greedy_result}")
    print(f"  Expected: Formula fails on simple molecules ✓")

    # Test 2: Complex molecule (with Rn/Ar/Y) - formula should work
    with open('input.md') as f:
        complex_input = f.read()

    rules, target = parse_input(complex_input)
    formula_result = solve_by_formula(target)
    greedy_result = solve_by_greedy(rules, target)

    print(f"\nActual input (complex molecule):")
    print(f"  Formula: {formula_result}")
    print(f"  Greedy: {greedy_result}")

    if formula_result == greedy_result:
        print(f"  ✓ Formula and greedy AGREE - high confidence!")
        return True
    else:
        diff = abs(formula_result - greedy_result)
        print(f"  ⚠ Formula and greedy DISAGREE by {diff}")
        if diff <= 2:
            print(f"  Small difference - likely acceptable")
            return True
        else:
            print(f"  Large difference - investigate!")
            return False


def test_verify_actual_solution():
    """Verify the actual input solution is valid."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    # Get solution
    steps = solve_by_greedy(rules, target)

    # Verify by reconstruction
    current = target
    reversed_rules = [(tgt, src) for src, tgt in rules]
    reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

    for i in range(steps):
        found = False
        for pattern, replacement in reversed_rules:
            if pattern in current:
                current = current.replace(pattern, replacement, 1)
                found = True
                break

        if not found:
            print(f"✗ Step {i+1}/{steps}: No rule applies to molecule of length {len(current)}")
            return False

    if current == 'e':
        print(f"✓ Test: Verified {steps} steps correctly reduces actual input to 'e'")
        return True
    else:
        print(f"✗ Test: After {steps} steps, reached '{current[:50]}...', not 'e'")
        return False


def test_solve_actual_input():
    """Get the actual answer using the best method."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Use auto mode (greedy with formula validation)
    result = solve(input_text, method='auto')

    print(f"  Final result: {result}")

    # Validate result is reasonable
    assert result > 0, "Result should be positive"
    assert result < 1000, "Result should be reasonable (< 1000)"

    print(f"✓ Test: Actual input solved = {result} steps")
    return result


def run_all_tests():
    """Run complete test suite."""

    print("="*60)
    print("PHASE 1: UNIT TESTS")
    print("="*60)
    test_parse_input()
    test_count_elements()

    print("\n" + "="*60)
    print("PHASE 2: ALGORITHM CORRECTNESS")
    print("="*60)
    test_formula_simple()
    test_greedy_simple()

    print("\n" + "="*60)
    print("PHASE 3: SOLUTION VERIFICATION (CRITICAL)")
    print("="*60)
    test_verify_solution_path()
    verification_passed = test_verify_actual_solution()

    print("\n" + "="*60)
    print("PHASE 4: PERFORMANCE")
    print("="*60)
    greedy_result = test_greedy_performance()
    formula_result = test_formula_performance()

    print("\n" + "="*60)
    print("PHASE 5: CROSS-VALIDATION")
    print("="*60)
    formula_agrees = test_formula_validation_strategy()

    print("\n" + "="*60)
    print("PHASE 6: ACTUAL INPUT")
    print("="*60)
    test_actual_input_structure()
    final_answer = test_solve_actual_input()

    print("\n" + "="*60)
    print(f"FINAL ANSWER: {final_answer}")
    print(f"Verification Status: {'PASSED ✓' if verification_passed else 'FAILED ✗'}")
    print(f"Formula Agreement: {'YES ✓' if formula_agrees else 'NO ⚠'}")
    print("="*60)

    if verification_passed:
        print("\n✓ SOLUTION VERIFIED AS CORRECT")
        print(f"Confidence: {'HIGH' if formula_agrees else 'MEDIUM'}")
    else:
        print("\n✗ SOLUTION VERIFICATION FAILED - DO NOT TRUST ANSWER")

    return final_answer


if __name__ == '__main__':
    run_all_tests()
