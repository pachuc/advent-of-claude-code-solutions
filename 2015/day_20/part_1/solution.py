def sum_of_divisors(n):
    """
    Calculate the sum of all divisors of n efficiently.
    Time complexity: O(sqrt(n))
    """
    divisor_sum = 0
    # Iterate up to square root of n
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisor_sum += i
            # Add the corresponding divisor (n/i) if it's different from i
            if i != n // i:
                divisor_sum += n // i
        i += 1
    return divisor_sum


def calculate_presents(house_number):
    """
    Calculate total presents delivered to a house.
    Each elf N delivers 10*N presents to houses that are multiples of N.
    Total presents = 10 * sum_of_divisors(house_number)
    """
    return 10 * sum_of_divisors(house_number)


def find_lowest_house(target_presents):
    """
    Find the lowest house number that receives at least target_presents.
    Uses a lower bound heuristic to skip obviously insufficient houses.
    """
    # Lower bound heuristic: start at target/72
    # This assumes sum_of_divisors(n)/n <= 7.2 for large n
    start_house = max(1, target_presents // 72)

    print(f"Starting search from house {start_house}...")

    house = start_house
    while True:
        presents = calculate_presents(house)
        if presents >= target_presents:
            return house

        # Progress tracking every 50,000 houses
        if house % 50000 == 0:
            print(f"Checked up to house {house}... (current presents: {presents})")

        house += 1


def main():
    # Read target from input.md
    with open('input.md', 'r') as f:
        target = int(f.read().strip())

    print(f"Target presents: {target}")

    # Find the lowest house
    result = find_lowest_house(target)

    print(f"\nAnswer: {result}")
    return result


if __name__ == "__main__":
    main()
