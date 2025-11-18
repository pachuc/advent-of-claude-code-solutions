#!/usr/bin/env python3
"""
Manual trace to verify algorithm correctness.
"""

def solve_spinlock_naive_with_trace(step_size, iterations):
    """Naive implementation with detailed trace."""
    buffer = [0]
    current_pos = 0

    print(f"Initial: buffer={buffer}, pos={current_pos}, len={len(buffer)}\n")

    for value in range(1, iterations + 1):
        old_pos = current_pos
        current_pos = (current_pos + step_size) % len(buffer)
        current_pos += 1
        buffer.insert(current_pos, value)

        print(f"i={value}:")
        print(f"  old_pos={old_pos}, new_pos after step={(old_pos+step_size)%len(buffer[:-1])}")
        print(f"  insert_pos={current_pos}")
        print(f"  buffer={buffer}")
        print(f"  buffer[1]={buffer[1]}")
        print()

    return buffer[1]


def solve_spinlock_optimized_with_trace(step_size, iterations):
    """Optimized implementation with detailed trace."""
    current_pos = 0
    buffer_len = 1
    value_after_zero = 0

    print(f"Initial: pos={current_pos}, len={buffer_len}, value_after_zero={value_after_zero}\n")

    for value in range(1, iterations + 1):
        old_pos = current_pos
        current_pos = (current_pos + step_size) % buffer_len
        insert_pos = current_pos + 1

        if insert_pos == 1:
            value_after_zero = value
            updated = " → UPDATE"
        else:
            updated = ""

        print(f"i={value}:")
        print(f"  old_pos={old_pos}, new_pos after step={current_pos}")
        print(f"  insert_pos={insert_pos}{updated}")
        print(f"  value_after_zero={value_after_zero}")

        current_pos = insert_pos
        buffer_len += 1
        print(f"  new current_pos={current_pos}, buffer_len={buffer_len}")
        print()

    return value_after_zero


# Test with step_size=3, N=5
print("=" * 60)
print("NAIVE IMPLEMENTATION (with actual buffer)")
print("=" * 60)
naive_result = solve_spinlock_naive_with_trace(3, 5)
print(f"Final result (buffer[1]): {naive_result}")

print("\n" + "=" * 60)
print("OPTIMIZED IMPLEMENTATION (tracking position 1 only)")
print("=" * 60)
optimized_result = solve_spinlock_optimized_with_trace(3, 5)
print(f"Final result (value_after_zero): {optimized_result}")

print("\n" + "=" * 60)
print(f"Results match: {naive_result == optimized_result}")
print("=" * 60)
