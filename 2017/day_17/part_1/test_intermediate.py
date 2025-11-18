def solve_spinlock_debug(step_size, debug_up_to=6):
    """
    Simulate spinlock algorithm with debug output.
    """
    buffer = [0]
    current_pos = 0

    for value in range(1, 2018):
        # Step forward with circular wrapping
        current_pos = (current_pos + step_size) % len(buffer)

        # Insert after current position
        current_pos += 1
        buffer.insert(current_pos, value)

        # Debug output for first few iterations
        if value <= debug_up_to:
            print(f"After insert {value}: {buffer}, current_pos={current_pos}")

    # Find value after 2017
    index_2017 = buffer.index(2017)
    next_index = (index_2017 + 1) % len(buffer)

    print(f"\nFinal buffer size: {len(buffer)}")
    print(f"Index of 2017: {index_2017}")
    print(f"Value after 2017: {buffer[next_index]}")

    # Verify buffer integrity
    assert len(buffer) == 2018, f"Expected 2018 elements, got {len(buffer)}"
    assert set(buffer) == set(range(2018)), "Buffer missing some values"
    print("Buffer integrity check: PASSED")

    return buffer[next_index]

result = solve_spinlock_debug(3)
print(f"\nResult: {result}")
