def solve_spinlock_optimized(step_size, iterations):
    """
    Optimized spinlock simulation that only tracks value after position 0.

    Since value 0 never moves from position 0, we only need to track what value
    is at position 1 (immediately after 0) without maintaining the entire buffer.

    Args:
        step_size: Number of steps to move forward each iteration
        iterations: Number of values to insert (50,000,000 for Part 2)

    Returns:
        The value at position 1 (immediately after 0) after all insertions
    """
    # Initialize state
    current_pos = 0
    buffer_len = 1
    value_after_zero = 0

    # Simulate each insertion
    for value in range(1, iterations + 1):
        # Step forward with circular wrapping
        current_pos = (current_pos + step_size) % buffer_len

        # Insert position is one after current position
        insert_pos = current_pos + 1

        # If inserting at position 1, update our tracked value
        if insert_pos == 1:
            value_after_zero = value

        # Update state
        current_pos = insert_pos
        buffer_len += 1

    return value_after_zero


def main():
    step_size = int(input().strip())
    result = solve_spinlock_optimized(step_size, 50_000_000)
    print(result)


if __name__ == "__main__":
    main()
