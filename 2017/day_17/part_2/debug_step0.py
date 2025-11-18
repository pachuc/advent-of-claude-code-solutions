"""Debug script to trace step_size=0 behavior"""

def trace_step_0():
    """Trace through step_size=0, N=5 manually"""
    step_size = 0
    iterations = 5

    # Naive version with trace
    print("Naive version with full buffer:")
    buffer = [0]
    current_pos = 0

    for value in range(1, iterations + 1):
        old_pos = current_pos
        current_pos = (current_pos + step_size) % len(buffer)
        current_pos += 1
        buffer.insert(current_pos, value)
        print(f"  i={value}: step from {old_pos} -> {current_pos-1} -> insert at {current_pos}, buffer={buffer}")

    print(f"  Final buffer[1] = {buffer[1]}\n")

    # Optimized version with trace
    print("Optimized version tracking position 1:")
    current_pos = 0
    buffer_len = 1
    value_after_zero = 0

    for value in range(1, iterations + 1):
        old_pos = current_pos
        current_pos = (current_pos + step_size) % buffer_len
        insert_pos = current_pos + 1

        update = ""
        if insert_pos == 1:
            value_after_zero = value
            update = f" -> UPDATE value_after_zero={value}"

        print(f"  i={value}: pos={old_pos}, step to {current_pos}, insert_pos={insert_pos}, buffer_len={buffer_len}{update}")

        current_pos = insert_pos
        buffer_len += 1

    print(f"  Final value_after_zero = {value_after_zero}")

if __name__ == "__main__":
    trace_step_0()
