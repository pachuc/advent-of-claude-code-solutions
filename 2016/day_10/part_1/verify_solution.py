from solution import *

def verify_full_input():
    """Verify the solution on full input and print details"""
    rules, assignments = parse_input('input.md')
    bots = defaultdict(list)
    outputs = defaultdict(list)
    ready_queue = deque()

    print(f"Total bot rules parsed: {len(rules)}")
    print(f"Total initial assignments: {len(assignments)}")

    # Process initial chip assignments
    for chip_value, bot_num in assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    print(f"Bots ready to process initially: {len(ready_queue)}")

    # Track all comparisons
    comparisons = []
    processed_bots = set()

    while ready_queue:
        bot_id = ready_queue.popleft()
        chips = bots[bot_id]

        if bot_id in processed_bots:
            print(f"ERROR: Bot {bot_id} processing twice!")
            return

        processed_bots.add(bot_id)
        comparisons.append((bot_id, sorted(chips)))

        # Check if this bot compares 61 and 17
        if set(chips) == {61, 17}:
            print(f"\n✓ Found target! Bot {bot_id} compares {sorted(chips)}")
            answer = bot_id

        # Process the bot
        low_chip = min(chips)
        high_chip = max(chips)

        low_dest_type, low_dest_num = rules[bot_id][0]
        high_dest_type, high_dest_num = rules[bot_id][1]

        give_chip(low_dest_type, low_dest_num, low_chip, bots, outputs, ready_queue)
        give_chip(high_dest_type, high_dest_num, high_chip, bots, outputs, ready_queue)

        bots[bot_id] = []

    print(f"\nTotal bots processed: {len(processed_bots)}")
    print(f"Total comparisons made: {len(comparisons)}")

    # Count chips
    initial_chip_count = len(assignments)
    final_chip_count = sum(len(chips) for chips in outputs.values())
    print(f"\nChip conservation check:")
    print(f"  Initial chips: {initial_chip_count}")
    print(f"  Final chips (in outputs): {final_chip_count}")
    print(f"  ✓ Conservation verified!" if initial_chip_count == final_chip_count else "  ✗ Chips lost or duplicated!")

    # Check for the comparison of 61 and 17
    target_comparisons = [comp for comp in comparisons if set(comp[1]) == {61, 17}]
    print(f"\nComparisons of {{61, 17}}: {len(target_comparisons)}")
    if target_comparisons:
        print(f"  Bot {target_comparisons[0][0]} compared {target_comparisons[0][1]}")

    print(f"\n✓ Final answer: {answer}")

if __name__ == '__main__':
    verify_full_input()
