"""
Advent of Code 2015 - Day 20 Part 2: Elf Present Delivery

This solution finds the lowest house number that receives at least a target
number of presents, given new delivery constraints where each elf has limited
delivery capacity.
"""

# Constants
PRESENTS_MULTIPLIER = 11
MAX_VISITS_PER_ELF = 50


def get_divisors_with_limit(house_num: int, max_visits: int = 50) -> set[int]:
    """
    Find all divisors of house_num that satisfy the 50-house constraint.

    An elf numbered 'd' visits house 'house_num' only if it's within the first
    50 houses that elf visits. Since elf 'd' visits houses d, 2d, 3d, ..., 50d,
    it visits house_num only if house_num <= 50d, which means house_num/d <= 50.

    Args:
        house_num: The house number to find divisors for
        max_visits: Maximum number of houses each elf visits (default 50)

    Returns:
        Set of divisors that satisfy the constraint
    """
    divisors = set()

    # Only need to check up to sqrt(house_num)
    i = 1
    while i * i <= house_num:
        if house_num % i == 0:
            # Check if divisor i satisfies the constraint
            # Elf i visits house_num only if house_num/i <= max_visits
            if house_num // i <= max_visits:
                divisors.add(i)

            # Check the complementary divisor
            complement = house_num // i
            if complement != i:  # Avoid duplicates for perfect squares
                # Elf complement visits house_num only if house_num/complement <= max_visits
                if house_num // complement <= max_visits:
                    divisors.add(complement)

        i += 1

    return divisors


def calculate_presents(house_num: int, multiplier: int = 11, max_visits: int = 50) -> int:
    """
    Calculate total presents delivered to a given house.

    Args:
        house_num: The house number
        multiplier: Number of presents per elf number (default 11)
        max_visits: Maximum number of houses each elf visits (default 50)

    Returns:
        Total number of presents delivered to the house
    """
    valid_divisors = get_divisors_with_limit(house_num, max_visits)
    total_presents = sum(multiplier * divisor for divisor in valid_divisors)
    return total_presents


def find_lowest_house(target: int, multiplier: int = 11, max_visits: int = 50) -> int:
    """
    Find the lowest house number that receives at least the target number of presents.

    Args:
        target: Minimum number of presents required
        multiplier: Number of presents per elf number (default 11)
        max_visits: Maximum number of houses each elf visits (default 50)

    Returns:
        The lowest house number meeting the criteria
    """
    # Start from a reasonable point to skip unnecessary iterations
    # Conservative estimate: target // 500
    start = target // 500

    house = start
    while True:
        presents = calculate_presents(house, multiplier, max_visits)
        if presents >= target:
            return house
        house += 1

        # Safety check to avoid infinite loop
        if house > target // 5:
            raise ValueError(f"Search exceeded reasonable bounds without finding answer")


if __name__ == "__main__":
    # Read input
    with open('input.md', 'r') as f:
        target_presents = int(f.read().strip())

    # Find answer
    result = find_lowest_house(target_presents, PRESENTS_MULTIPLIER, MAX_VISITS_PER_ELF)

    # Output result
    print(result)
