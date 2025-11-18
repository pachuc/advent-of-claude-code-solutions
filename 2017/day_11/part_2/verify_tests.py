"""Quick verification tests for the solution"""
from solution import find_max_distance

def test_case(name, input_str, expected):
    """Run a test case and report results"""
    moves = [m.strip() for m in input_str.split(',') if m.strip()] if input_str else []
    result = find_max_distance(moves)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    print(f"{status}: {name}")
    print(f"  Input: {input_str}")
    print(f"  Expected: {expected}, Got: {result}")
    if result != expected:
        print(f"  ERROR: Mismatch!")
    print()
    return result == expected

# Run key tests from the test plan
all_passed = True

# Test 1.1: Simple linear path
all_passed &= test_case("Simple linear path", "ne,ne,ne", 3)

# Test 1.2: Path returning to origin (CRITICAL)
all_passed &= test_case("Path returning to origin", "ne,ne,sw,sw", 2)

# Test 1.3: Oscillating path
all_passed &= test_case("Oscillating path", "n,s,n,s,n", 1)

# Test 2.1: Empty input
all_passed &= test_case("Empty input", "", 0)

# Test 2.2: Single move
all_passed &= test_case("Single move north", "n", 1)

# Test 2.3: Immediate return to origin (CRITICAL)
all_passed &= test_case("Immediate return to origin", "n,s", 1)

# Test 3.1: Spiral pattern
all_passed &= test_case("Spiral pattern", "ne,se,s,sw,nw,n,ne,se", 2)

# Test 3.2: Path with multiple peaks
all_passed &= test_case("Multiple peaks", "ne,ne,ne,sw,sw,sw,ne,ne,ne,ne,sw,sw,sw,sw", 4)

# Test 3.3: Example from Part 1
all_passed &= test_case("Part 1 example", "ne,ne,s,s", 2)

# Test all six directions
print("Testing all six directions:")
for direction in ['n', 'ne', 'se', 's', 'sw', 'nw']:
    all_passed &= test_case(f"Direction {direction}", direction, 1)

if all_passed:
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
else:
    print("=" * 50)
    print("SOME TESTS FAILED!")
    print("=" * 50)
