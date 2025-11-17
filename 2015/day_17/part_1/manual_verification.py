from solution import parse_input

def find_and_print_combinations(containers, target, max_to_show=10):
    """
    Find combinations and print some examples for manual verification.
    """
    combinations = []
    n = len(containers)

    # Iterate through all possible subsets
    for mask in range(1 << n):
        subset = []
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):
                subset.append((i, containers[i]))
                subset_sum += containers[i]

        if subset_sum == target:
            combinations.append(subset)

    print(f"Total combinations found: {len(combinations)}")
    print(f"\nShowing first {min(max_to_show, len(combinations))} combinations:")
    print("="*60)

    for idx, combo in enumerate(combinations[:max_to_show]):
        values = [val for _, val in combo]
        indices = [i for i, _ in combo]
        print(f"{idx+1}. Containers at indices {indices}: {values} = {sum(values)}")

    return len(combinations)


if __name__ == '__main__':
    containers = parse_input('input.md')
    print(f"Container capacities: {containers}")
    print(f"Total containers: {len(containers)}")
    print(f"Target: 150 liters\n")

    result = find_and_print_combinations(containers, target=150, max_to_show=10)
