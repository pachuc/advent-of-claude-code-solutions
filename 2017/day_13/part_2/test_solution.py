from solution import parse_input, is_caught, find_minimum_delay, verify_delay

# Test with example input
print("Testing with example input...")
layers = parse_input('test_example.md')
print(f"Layers: {layers}")

# Test is_caught function with specific cases from test plan
print("\nTesting is_caught function:")
print(f"is_caught(0, 3, 0) = {is_caught(0, 3, 0)} (expected: True)")
print(f"is_caught(0, 3, 1) = {is_caught(0, 3, 1)} (expected: False)")
print(f"is_caught(6, 4, 0) = {is_caught(6, 4, 0)} (expected: True)")
print(f"is_caught(6, 4, 2) = {is_caught(6, 4, 2)} (expected: False)")

# Test minimum delay for example
print("\nFinding minimum delay for example...")
min_delay = find_minimum_delay(layers)
print(f"Minimum delay: {min_delay} (expected: 10)")

# Verify delays 0-9 don't work
print("\nVerifying delays 0-9 should NOT work:")
for d in range(10):
    works = verify_delay(layers, d)
    print(f"delay={d}: {'WORKS' if works else 'caught'}")

# Verify delay=10 works
print(f"\ndelay=10: {'WORKS' if verify_delay(layers, 10) else 'caught'} (expected: WORKS)")

# Additional verification for delay=10
print("\nDetailed check for delay=10:")
for depth, range_val in layers:
    period = 2 * (range_val - 1)
    time = 10 + depth
    caught = is_caught(depth, range_val, 10)
    print(f"Layer {depth}: range={range_val}, period={period}, time={time}, {time}%{period}={time%period}, caught={caught}")
