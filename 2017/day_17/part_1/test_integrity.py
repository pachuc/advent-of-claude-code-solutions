def test_buffer_integrity(step_size):
    """
    Test buffer integrity after spinlock simulation.
    """
    buffer = [0]
    current_pos = 0

    for value in range(1, 2018):
        current_pos = (current_pos + step_size) % len(buffer)
        current_pos += 1
        buffer.insert(current_pos, value)

    # Verify buffer integrity
    print(f"Testing step_size={step_size}")
    print(f"  Final buffer size: {len(buffer)}")
    assert len(buffer) == 2018, f"Expected 2018 elements, got {len(buffer)}"

    print(f"  Unique values: {len(set(buffer))}")
    assert len(set(buffer)) == 2018, f"Expected 2018 unique values, got {len(set(buffer))}"

    print(f"  Contains all 0-2017: {set(buffer) == set(range(2018))}")
    assert set(buffer) == set(range(2018)), "Buffer missing some values"

    # Find value after 2017
    index_2017 = buffer.index(2017)
    next_index = (index_2017 + 1) % len(buffer)
    result = buffer[next_index]

    print(f"  Index of 2017: {index_2017}")
    print(f"  Value after 2017: {result}")
    print(f"  PASSED\n")

    return result

# Test all cases
print("Buffer Integrity Tests\n" + "="*50 + "\n")
test_buffer_integrity(3)
test_buffer_integrity(355)
test_buffer_integrity(1)
test_buffer_integrity(10000)
print("All integrity tests PASSED!")
