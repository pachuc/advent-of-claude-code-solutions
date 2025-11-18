from solution import parse_input, is_caught

# Load actual input
layers = parse_input('input.md')

print("Spot-checking specific layers from actual input:")
print("=" * 70)

# Test cases from test plan
test_cases = [
    (0, 3, "Expected to be caught (0 % 4 = 0)"),
    (6, 4, "Expected to be caught (6 % 6 = 0)"),
    (2, 4, "Expected NOT caught (2 % 6 = 2)"),
    (4, 6, "Expected NOT caught (4 % 10 = 4)"),
    (8, 6, "Expected NOT caught (8 % 10 = 8)"),
    (12, 6, "Expected NOT caught (12 % 10 = 2)"),
]

total_severity = 0

for depth, range_val, description in test_cases:
    caught = is_caught(depth, range_val)
    if range_val > 1:
        period = 2 * (range_val - 1)
        modulo = depth % period
    else:
        period = 0
        modulo = "N/A"

    severity = depth * range_val if caught else 0

    print(f"Layer {depth}, Range {range_val}:")
    print(f"  Period: {period}, Depth % Period: {modulo}")
    print(f"  Caught: {caught}")
    print(f"  Severity: {severity}")
    print(f"  {description}")
    print()

    if caught:
        total_severity += severity

print("=" * 70)
print(f"Partial severity from spot-checked layers: {total_severity}")
print()

# Now calculate full severity and show which layers are caught
print("All caught layers:")
print("=" * 70)

full_severity = 0
caught_count = 0

for depth, range_val in layers:
    if is_caught(depth, range_val):
        severity = depth * range_val
        full_severity += severity
        caught_count += 1
        print(f"Layer {depth:2d} (range {range_val:2d}): severity = {depth:2d} × {range_val:2d} = {severity:4d}")

print("=" * 70)
print(f"Total caught layers: {caught_count}")
print(f"Total severity: {full_severity}")
