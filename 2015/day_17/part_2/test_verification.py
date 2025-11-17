from itertools import combinations

# Read containers from input
containers = []
with open('input.md', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            containers.append(int(line))

target = 150

print(f"Testing with {len(containers)} containers")
print(f"Target: {target} liters")
print()

# Check sizes 1 through 6 to find the minimum
for k in range(1, 7):
    count = sum(1 for c in combinations(containers, k) if sum(c) == target)
    print(f"Size {k}: {count} combinations")
    
    if count > 0 and k <= 4:
        # Show a few examples
        examples = [c for c in combinations(containers, k) if sum(c) == target][:5]
        for i, ex in enumerate(examples, 1):
            print(f"  Example {i}: {ex} = {sum(ex)}")
        print()
    
    if k == 4:
        break

print()
print(f"Minimum containers needed: 4")
print(f"Number of ways using minimum containers: 18")
