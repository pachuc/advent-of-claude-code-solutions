"""
Verify the answer is correct.
"""

from solution import calculate_presents

answer = 831600

print(f"Verifying answer: {answer}")
print()

# Check the answer house
presents_at_answer = calculate_presents(answer)
print(f"House {answer}: {presents_at_answer:,} presents")
print(f"Target: 34,000,000 presents")
print(f"Meets target? {presents_at_answer >= 34000000}")
print()

# Check the previous house
presents_at_prev = calculate_presents(answer - 1)
print(f"House {answer - 1}: {presents_at_prev:,} presents")
print(f"Below target? {presents_at_prev < 34000000}")
print()

if presents_at_answer >= 34000000 and presents_at_prev < 34000000:
    print("✓ Answer verified! House", answer, "is the lowest house that receives at least 34,000,000 presents.")
else:
    print("✗ Verification failed!")
