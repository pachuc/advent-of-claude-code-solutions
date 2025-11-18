#!/usr/bin/env python3
"""Verify specific layers from the actual input."""

from solution import parse_input, is_caught

# Parse actual input
layers = parse_input('input.md')

print(f"Total layers in input: {len(layers)}")
print("\n--- Spot-Check Verification (from test plan) ---\n")

# Expected to be caught (from test plan):
print("Expected to be CAUGHT:")
spot_checks_caught = [
    (0, 3, 4, True),   # Layer 0, range 3: period=4, 0 % 4 = 0
    (6, 4, 6, True),   # Layer 6, range 4: period=6, 6 % 6 = 0
]

for depth, range_val, period, should_be_caught in spot_checks_caught:
    caught = is_caught(depth, range_val)
    severity = depth * range_val if caught else 0
    mod_result = depth % period if period > 0 else 0
    status = "✓" if caught == should_be_caught else "✗"
    print(f"  {status} Layer {depth}, range {range_val}: period={period}, {depth}%{period}={mod_result}, caught={caught}, severity={severity}")

print("\nExpected NOT to be caught:")
spot_checks_not_caught = [
    (2, 4, 6, False),   # Layer 2, range 4: period=6, 2 % 6 = 2
    (4, 6, 10, False),  # Layer 4, range 6: period=10, 4 % 10 = 4
    (8, 6, 10, False),  # Layer 8, range 6: period=10, 8 % 10 = 8
    (12, 6, 10, False), # Layer 12, range 6: period=10, 12 % 10 = 2
]

for depth, range_val, period, should_be_caught in spot_checks_not_caught:
    caught = is_caught(depth, range_val)
    severity = depth * range_val if caught else 0
    mod_result = depth % period
    status = "✓" if caught == should_be_caught else "✗"
    print(f"  {status} Layer {depth}, range {range_val}: period={period}, {depth}%{period}={mod_result}, caught={caught}, severity={severity}")

print("\n--- Complete Analysis: All Caught Layers ---\n")

total_severity = 0
caught_count = 0
for depth, range_val in layers:
    if is_caught(depth, range_val):
        severity = depth * range_val
        total_severity += severity
        caught_count += 1
        period = 2 * (range_val - 1) if range_val > 1 else 0
        print(f"Layer {depth:3d} (range {range_val:2d}): severity = {depth:3d} × {range_val:2d} = {severity:4d}")

print(f"\nTotal caught layers: {caught_count}")
print(f"Total severity: {total_severity}")
print(f"\nExpected from implementation summary: 1612")
print(f"Match: {total_severity == 1612}")
