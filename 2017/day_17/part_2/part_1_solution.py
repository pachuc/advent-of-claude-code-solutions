def solve_spinlock(step_size):
    """
    Simulate spinlock algorithm and find value after 2017.

    Args:
        step_size: Number of steps to move forward each iteration

    Returns:
        The value immediately after 2017 in the final buffer
    """
    buffer = [0]
    current_pos = 0

    for value in range(1, 2018):
        # Step forward with circular wrapping
        current_pos = (current_pos + step_size) % len(buffer)

        # Insert after current position
        current_pos += 1
        buffer.insert(current_pos, value)

    # Find value after 2017
    index_2017 = buffer.index(2017)
    next_index = (index_2017 + 1) % len(buffer)

    return buffer[next_index]

def main():
    step_size = int(input().strip())
    result = solve_spinlock(step_size)
    print(result)

if __name__ == "__main__":
    main()
