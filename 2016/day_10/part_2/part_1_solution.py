import re
from collections import defaultdict, deque

def parse_input(filename):
    """
    Parse input file and extract bot rules and initial chip assignments.

    Returns:
        tuple: (rules_dict, initial_assignments_list)
        - rules_dict: {bot_num: ((low_type, low_num), (high_type, high_num))}
        - initial_assignments_list: [(chip_value, bot_num), ...]
    """
    rules = {}
    initial_assignments = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse "value X goes to bot Y"
            value_match = re.match(r'value (\d+) goes to bot (\d+)', line)
            if value_match:
                chip_value = int(value_match.group(1))
                bot_num = int(value_match.group(2))
                initial_assignments.append((chip_value, bot_num))
                continue

            # Parse "bot X gives low to [bot/output] Y and high to [bot/output] Z"
            rule_match = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', line)
            if rule_match:
                bot_num = int(rule_match.group(1))
                low_type = rule_match.group(2)
                low_num = int(rule_match.group(3))
                high_type = rule_match.group(4)
                high_num = int(rule_match.group(5))
                rules[bot_num] = ((low_type, low_num), (high_type, high_num))
                continue

    return rules, initial_assignments


def give_chip(dest_type, dest_num, chip_value, bots, outputs, ready_queue):
    """
    Give a chip to a destination (bot or output).
    If the destination is a bot and it now has 2 chips, add it to the ready queue.
    """
    if dest_type == 'output':
        outputs[dest_num].append(chip_value)
    elif dest_type == 'bot':
        bots[dest_num].append(chip_value)
        if len(bots[dest_num]) == 2:
            ready_queue.append(dest_num)


def simulate(bots, outputs, rules, ready_queue, target_values={61, 17}):
    """
    Simulate the bot chip processing.

    Returns:
        int or None: bot number that compares the target values, or None if not found
    """
    while ready_queue:
        bot_id = ready_queue.popleft()
        chips = bots[bot_id]

        # Should have exactly 2 chips
        assert len(chips) == 2, f"Bot {bot_id} should have 2 chips, has {len(chips)}"

        # Check if this bot compares the target values
        if set(chips) == target_values:
            return bot_id

        # Process the bot
        low_chip = min(chips)
        high_chip = max(chips)

        low_dest_type, low_dest_num = rules[bot_id][0]
        high_dest_type, high_dest_num = rules[bot_id][1]

        # Give low chip to low destination
        give_chip(low_dest_type, low_dest_num, low_chip, bots, outputs, ready_queue)

        # Give high chip to high destination
        give_chip(high_dest_type, high_dest_num, high_chip, bots, outputs, ready_queue)

        # Clear this bot's chips
        bots[bot_id] = []

    return None


def main():
    # Parse input file
    rules, initial_assignments = parse_input('input.md')

    # Initialize data structures
    bots = defaultdict(list)
    outputs = defaultdict(list)
    ready_queue = deque()

    # Process initial chip assignments
    for chip_value, bot_num in initial_assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    # Run simulation to find which bot compares 61 and 17
    answer = simulate(bots, outputs, rules, ready_queue)

    # Validate answer
    if answer is None:
        print("ERROR: No bot compared 61 and 17")
        return

    # Output result
    print(answer)


if __name__ == '__main__':
    main()
