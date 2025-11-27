from solution import solve, parse_input, get_y_range, flow_down
import sys

# Test on actual input
with open('input.md', 'r') as f:
    actual_input = f.read()

# Parse and simulate
lines = actual_input.strip().split('\n')
clay_set = parse_input(lines)
min_y, max_y = get_y_range(clay_set)

flowing_water = set()
settled_water = set()
sys.setrecursionlimit(10000)

flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

# Calculate both Part 1 and Part 2 answers
part1_count = len({(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y})
part2_count = len({(x, y) for (x, y) in settled_water if min_y <= y <= max_y})

print("Verification Tests:")
print("=" * 60)

# Test 1: Part 1 regression
print(f"\nTest 1: Part 1 Regression")
print(f"  Part 1 result: {part1_count}")
print(f"  Expected: 41027")
assert part1_count == 41027, f"Part 1 regression failed: expected 41027, got {part1_count}"
print(f"  ✓ PASSED")

# Test 2: Part 2 result
print(f"\nTest 2: Part 2 Result")
print(f"  Part 2 result: {part2_count}")
print(f"  ✓ Result: {part2_count}")

# Test 3: Part 2 < Part 1
print(f"\nTest 3: Part 2 < Part 1")
print(f"  Part 2 ({part2_count}) < Part 1 ({part1_count}): {part2_count < part1_count}")
assert part2_count < part1_count, f"Part 2 should be less than Part 1"
print(f"  ✓ PASSED")

# Test 4: Part 2 > 0
print(f"\nTest 4: Part 2 > 0")
print(f"  Part 2 result > 0: {part2_count > 0}")
assert part2_count > 0, f"Part 2 should be positive"
print(f"  ✓ PASSED")

# Test 5: Set disjointness
print(f"\nTest 5: Set Disjointness")
intersection = flowing_water & settled_water
print(f"  Flowing ∩ Settled = {len(intersection)} (should be 0)")
assert len(intersection) == 0, f"Sets should be disjoint, found {len(intersection)} tiles in both"
print(f"  ✓ PASSED")

# Test 6: Reasonableness
print(f"\nTest 6: Reasonableness Check")
ratio = part2_count / part1_count
print(f"  Settled water ratio: {ratio:.1%}")
print(f"  Flowing water: {part1_count - part2_count}")
print(f"  Settled water: {part2_count}")
if 0.3 <= ratio <= 0.9:
    print(f"  ✓ Ratio within expected range (30%-90%)")
else:
    print(f"  ⚠ Ratio outside typical range, but may be valid")

print("\n" + "=" * 60)
print(f"All core tests PASSED!")
print(f"\nFinal Answer (Part 2): {part2_count}")
