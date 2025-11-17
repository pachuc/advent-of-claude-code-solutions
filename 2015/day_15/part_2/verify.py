"""Verification script to manually check the best combination."""

# Best combination found:
# Sugar: 21, Sprinkles: 8, Candy: 26, Chocolate: 45

# Ingredients from input.md:
# Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
# Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
# Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
# Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8

amounts = [21, 8, 26, 45]
ingredients = [
    {'name': 'Sugar', 'capacity': 3, 'durability': 0, 'flavor': 0, 'texture': -3, 'calories': 2},
    {'name': 'Sprinkles', 'capacity': -3, 'durability': 3, 'flavor': 0, 'texture': 0, 'calories': 9},
    {'name': 'Candy', 'capacity': -1, 'durability': 0, 'flavor': 4, 'texture': 0, 'calories': 1},
    {'name': 'Chocolate', 'capacity': 0, 'durability': 0, 'flavor': -2, 'texture': 2, 'calories': 8}
]

print("Manual Verification:")
print("=" * 60)

# Check total teaspoons
total_teaspoons = sum(amounts)
print(f"Total teaspoons: {total_teaspoons} (should be 100)")
assert total_teaspoons == 100, "Teaspoons should sum to 100!"

# Calculate calories
calories = sum(amounts[i] * ingredients[i]['calories'] for i in range(4))
print(f"\nCalories calculation:")
for i in range(4):
    print(f"  {ingredients[i]['name']}: {amounts[i]} × {ingredients[i]['calories']} = {amounts[i] * ingredients[i]['calories']}")
print(f"Total calories: {calories} (should be 500)")
assert calories == 500, "Calories should equal 500!"

# Calculate capacity
capacity = sum(amounts[i] * ingredients[i]['capacity'] for i in range(4))
print(f"\nCapacity calculation:")
for i in range(4):
    print(f"  {ingredients[i]['name']}: {amounts[i]} × {ingredients[i]['capacity']} = {amounts[i] * ingredients[i]['capacity']}")
print(f"Total capacity (before max): {capacity}")
capacity = max(0, capacity)
print(f"Total capacity (after max): {capacity}")

# Calculate durability
durability = sum(amounts[i] * ingredients[i]['durability'] for i in range(4))
print(f"\nDurability calculation:")
for i in range(4):
    print(f"  {ingredients[i]['name']}: {amounts[i]} × {ingredients[i]['durability']} = {amounts[i] * ingredients[i]['durability']}")
print(f"Total durability (before max): {durability}")
durability = max(0, durability)
print(f"Total durability (after max): {durability}")

# Calculate flavor
flavor = sum(amounts[i] * ingredients[i]['flavor'] for i in range(4))
print(f"\nFlavor calculation:")
for i in range(4):
    print(f"  {ingredients[i]['name']}: {amounts[i]} × {ingredients[i]['flavor']} = {amounts[i] * ingredients[i]['flavor']}")
print(f"Total flavor (before max): {flavor}")
flavor = max(0, flavor)
print(f"Total flavor (after max): {flavor}")

# Calculate texture
texture = sum(amounts[i] * ingredients[i]['texture'] for i in range(4))
print(f"\nTexture calculation:")
for i in range(4):
    print(f"  {ingredients[i]['name']}: {amounts[i]} × {ingredients[i]['texture']} = {amounts[i] * ingredients[i]['texture']}")
print(f"Total texture (before max): {texture}")
texture = max(0, texture)
print(f"Total texture (after max): {texture}")

# Calculate final score
score = capacity * durability * flavor * texture
print(f"\nFinal Score:")
print(f"  {capacity} × {durability} × {flavor} × {texture} = {score}")

print("\n" + "=" * 60)
print(f"VERIFIED: Score = {score}")
print("=" * 60)
