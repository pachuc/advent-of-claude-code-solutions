from solution import parse_input, find_strongest_nanobot, count_in_range

# Parse actual input
nanobots = parse_input('input.md')
print(f"Total nanobots: {len(nanobots)}")

# Find strongest
strongest = find_strongest_nanobot(nanobots)
sx, sy, sz, sr = strongest
print(f"Strongest nanobot: pos=<{sx},{sy},{sz}>, r={sr}")

# Count in range
result = count_in_range(nanobots, strongest)
print(f"Nanobots in range: {result}")

# Sanity checks
print("\nSanity checks:")
print(f"  ✓ Total nanobots: {len(nanobots)} == 1000")
print(f"  ✓ Strongest radius: {sr} == 99859637")
print(f"  ✓ Result in valid range: 1 <= {result} <= 1000")
print(f"  ✓ Strongest nanobot position: ({sx},{sy},{sz}) == (113369857,1348469,44315500)")

# Verify the result is correct
assert len(nanobots) == 1000, "Should have 1000 nanobots"
assert sr == 99859637, "Strongest radius should be 99859637"
assert 1 <= result <= 1000, f"Result {result} should be between 1 and 1000"
assert (sx, sy, sz) == (113369857, 1348469, 44315500), "Strongest position mismatch"

print("\n✓ All sanity checks passed!")
print(f"\nFinal answer: {result}")
