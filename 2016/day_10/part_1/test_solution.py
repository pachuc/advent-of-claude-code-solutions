from solution import *

def test_example():
    """Test the example from problem statement - should return bot 2 for values {2, 5}"""
    rules, assignments = parse_input('example_input.txt')
    bots = defaultdict(list)
    outputs = defaultdict(list)
    ready_queue = deque()

    for chip_value, bot_num in assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    # For the example, we're looking for bot comparing 2 and 5
    result = simulate(bots, outputs, rules, ready_queue, target_values={2, 5})

    print(f"Example test result: Bot {result}")
    assert result == 2, f"Expected bot 2, got {result}"
    print("✓ Example test passed!")

if __name__ == '__main__':
    test_example()
    print("All tests passed!")
