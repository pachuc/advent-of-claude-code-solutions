import re
from itertools import permutations


def parse_input(input_text):
    """
    Parse happiness relationships from input text
    Returns:
    - happiness_map: dict[person][neighbor] = happiness_value
    - people: set of all person names
    """
    happiness_map = {}
    people = set()

    # Pattern: "PersonA would gain/lose X happiness units by sitting next to PersonB."
    pattern = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'

    for line in input_text.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            person, gain_lose, magnitude, neighbor = match.groups()
            magnitude = int(magnitude)

            # Convert "lose" to negative value
            if gain_lose == "lose":
                magnitude = -magnitude

            # Add to happiness map
            if person not in happiness_map:
                happiness_map[person] = {}
            happiness_map[person][neighbor] = magnitude

            # Track all people
            people.add(person)
            people.add(neighbor)

    return happiness_map, people


def add_self(happiness_map, people, self_name="Me"):
    """
    Add ourselves to the seating arrangement with 0 happiness
    Modifies happiness_map and people in place
    """
    # Add bidirectional 0 happiness relationships with all existing people
    happiness_map[self_name] = {}
    for person in list(people):
        happiness_map[self_name][person] = 0
        happiness_map[person][self_name] = 0

    # Add self to people set
    people.add(self_name)


def calculate_happiness(arrangement, happiness_map):
    """
    Calculate total happiness for a circular seating arrangement
    Args:
        arrangement: list of people in seating order
        happiness_map: nested dict of happiness values
    Returns: total happiness (int)
    """
    total_happiness = 0
    n = len(arrangement)

    for i in range(n):
        person = arrangement[i]
        left_neighbor = arrangement[(i - 1) % n]
        right_neighbor = arrangement[(i + 1) % n]

        # Add happiness from both neighbors
        total_happiness += happiness_map[person][left_neighbor]
        total_happiness += happiness_map[person][right_neighbor]

    return total_happiness


def find_optimal_seating(people, happiness_map):
    """
    Find the seating arrangement with maximum happiness
    Returns: (maximum happiness value, optimal arrangement)
    """
    people_list = list(people)

    # Fix the first person to eliminate rotational duplicates
    fixed_person = people_list[0]
    others = people_list[1:]

    max_happiness = float('-inf')
    optimal_arrangement = None

    # Generate all permutations of remaining people
    for perm in permutations(others):
        arrangement = [fixed_person] + list(perm)
        happiness = calculate_happiness(arrangement, happiness_map)

        if happiness > max_happiness:
            max_happiness = happiness
            optimal_arrangement = arrangement

    return max_happiness, optimal_arrangement


def solve(input_file):
    """
    Main solver function
    """
    # 1. Read input file
    with open(input_file, 'r') as f:
        input_text = f.read()

    # 2. Parse input
    happiness_map, people = parse_input(input_text)

    # 3. Add self
    add_self(happiness_map, people)

    # 4. Find optimal seating
    max_happiness, optimal_arrangement = find_optimal_seating(people, happiness_map)

    # 5. Output results
    print(f"Maximum happiness: {max_happiness}")
    print(f"Optimal arrangement: {' -> '.join(optimal_arrangement)}")

    return max_happiness


if __name__ == "__main__":
    result = solve("input.md")
    print(f"\nAnswer: {result}")
