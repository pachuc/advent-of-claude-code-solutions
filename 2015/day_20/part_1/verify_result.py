from solution import calculate_presents

# Verify the solution
result = 786240
target = 34000000

print(f"Verifying result: House {result}")
print(f"Target: {target} presents")
print()

# Calculate presents for the result house
presents_at_result = calculate_presents(result)
print(f"Presents at house {result}: {presents_at_result}")
print(f"Meets target? {presents_at_result >= target}")
print()

# Calculate presents for the previous house
presents_at_prev = calculate_presents(result - 1)
print(f"Presents at house {result - 1}: {presents_at_prev}")
print(f"Below target? {presents_at_prev < target}")
print()

# Verification
if presents_at_result >= target and presents_at_prev < target:
    print("✓ VERIFICATION PASSED: House {} is the correct answer!".format(result))
else:
    print("✗ VERIFICATION FAILED")
    if presents_at_result < target:
        print(f"  ERROR: House {result} doesn't have enough presents")
    if presents_at_prev >= target:
        print(f"  ERROR: House {result-1} already has enough presents")
