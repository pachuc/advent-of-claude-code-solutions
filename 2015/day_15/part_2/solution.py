import re
import sys


def parse_ingredients(filename):
    """Parse ingredient data from input file."""
    ingredients = []
    pattern = r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = re.match(pattern, line)
            if match:
                name, capacity, durability, flavor, texture, calories = match.groups()
                ingredients.append({
                    'name': name,
                    'capacity': int(capacity),
                    'durability': int(durability),
                    'flavor': int(flavor),
                    'texture': int(texture),
                    'calories': int(calories)
                })

    if not ingredients:
        raise ValueError("No valid ingredients found in input file")

    return ingredients


def generate_combinations(total, num_ingredients):
    """Generate all non-negative integer combinations that sum to total."""
    if num_ingredients == 1:
        yield [total]
    else:
        for i in range(total + 1):
            for rest in generate_combinations(total - i, num_ingredients - 1):
                yield [i] + rest


def calculate_calories(amounts, ingredients):
    """Calculate total calories for given ingredient amounts."""
    return sum(amounts[i] * ingredients[i]['calories'] for i in range(len(ingredients)))


def calculate_score(amounts, ingredients):
    """Calculate score for given ingredient amounts."""
    # Calculate property totals
    capacity_total = sum(amounts[i] * ingredients[i]['capacity'] for i in range(len(ingredients)))
    durability_total = sum(amounts[i] * ingredients[i]['durability'] for i in range(len(ingredients)))
    flavor_total = sum(amounts[i] * ingredients[i]['flavor'] for i in range(len(ingredients)))
    texture_total = sum(amounts[i] * ingredients[i]['texture'] for i in range(len(ingredients)))

    # Apply max(0, total) rule - negative becomes zero
    capacity_total = max(0, capacity_total)
    durability_total = max(0, durability_total)
    flavor_total = max(0, flavor_total)
    texture_total = max(0, texture_total)

    # Calculate final score
    score = capacity_total * durability_total * flavor_total * texture_total
    return score


def find_max_score(ingredients, total_teaspoons=100, target_calories=500):
    """Find maximum score with constraints."""
    max_score = 0
    best_amounts = None

    # Generate all valid combinations
    for amounts in generate_combinations(total_teaspoons, len(ingredients)):
        # Check calorie constraint first (optimization)
        if calculate_calories(amounts, ingredients) != target_calories:
            continue

        # Calculate score for this valid combination
        score = calculate_score(amounts, ingredients)

        # Update max if better
        if score > max_score:
            max_score = score
            best_amounts = amounts.copy()

    return max_score, best_amounts


def main():
    # Use command-line argument if provided, otherwise default to 'input.md'
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    # Parse ingredients
    ingredients = parse_ingredients(filename)

    # Find maximum score
    result, best_amounts = find_max_score(ingredients)

    # Print result
    print(result)

    # Optional: Print best combination for verification
    if best_amounts:
        print(f"\nBest combination:")
        for i, ingredient in enumerate(ingredients):
            print(f"  {ingredient['name']}: {best_amounts[i]} teaspoons")
        print(f"Total teaspoons: {sum(best_amounts)}")
        print(f"Total calories: {calculate_calories(best_amounts, ingredients)}")
        print(f"Score: {result}")


if __name__ == '__main__':
    main()
