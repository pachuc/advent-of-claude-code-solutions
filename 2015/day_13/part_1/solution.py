import re
from itertools import permutations


def parse_input(input_text):
    """Parse input and return happiness map and list of people"""
    happiness = {}
    people = set()

    pattern = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'

    for line in input_text.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            person1, action, value, person2 = match.groups()
            people.add(person1)
            people.add(person2)

            if person1 not in happiness:
                happiness[person1] = {}

            happiness_value = int(value) if action == 'gain' else -int(value)
            happiness[person1][person2] = happiness_value

    return happiness, list(people)


def calculate_happiness(arrangement, happiness_map):
    """Calculate total happiness for a circular arrangement"""
    total = 0
    n = len(arrangement)

    for i in range(n):
        person = arrangement[i]
        left_neighbor = arrangement[(i - 1) % n]
        right_neighbor = arrangement[(i + 1) % n]

        total += happiness_map[person][left_neighbor]
        total += happiness_map[person][right_neighbor]

    return total


def find_optimal_seating(happiness_map, people):
    """Find the seating arrangement with maximum happiness"""
    people_sorted = sorted(people)
    fixed_person = people_sorted[0]
    remaining_people = people_sorted[1:]

    max_happiness = float('-inf')

    for perm in permutations(remaining_people):
        arrangement = [fixed_person] + list(perm)
        current_happiness = calculate_happiness(arrangement, happiness_map)

        if current_happiness > max_happiness:
            max_happiness = current_happiness

    return max_happiness


def main():
    # Read input from input.md
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    happiness_map, people = parse_input(input_text)

    # Find optimal seating
    max_happiness = find_optimal_seating(happiness_map, people)

    # Output result
    print(max_happiness)


if __name__ == '__main__':
    main()
