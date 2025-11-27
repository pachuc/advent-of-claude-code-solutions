from solution import solve

# Test with example data
print("Testing with example data:")
result = solve('test_example.md')
expected = 240

if result == expected:
    print(f"\n✓ Example test PASSED! Answer = {result}")
else:
    print(f"\n✗ Example test FAILED! Expected {expected}, got {result}")

# Test with actual input
print("\n" + "=" * 60)
print("Testing with actual input:")
actual_result = solve('input.md')
print(f"\nActual input result: {actual_result}")
