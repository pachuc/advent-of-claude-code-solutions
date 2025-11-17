from solution import parse_input, solve_by_greedy, solve_by_formula, count_elements

# Load actual input
with open('input.md', 'r') as f:
    input_text = f.read()

rules, target = parse_input(input_text)

print(f"Number of rules: {len(rules)}")
print(f"Target length: {len(target)}")
print(f"Target: {target[:100]}...")

# Try greedy with debugging
reversed_rules = [(tgt, src) for src, tgt in rules]
reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

print(f"\nTop 10 reversed rules (by pattern length):")
for i, (pattern, replacement) in enumerate(reversed_rules[:10]):
    print(f"  {i+1}. '{pattern}' => '{replacement}' (length: {len(pattern)})")

current = target
steps = 0
max_steps = 20

print(f"\nAttempting greedy reduction:")
for i in range(max_steps):
    found = False
    for pattern, replacement in reversed_rules:
        if pattern in current:
            old_len = len(current)
            current = current.replace(pattern, replacement, 1)
            new_len = len(current)
            steps += 1
            found = True
            print(f"  Step {steps}: Applied '{pattern}' => '{replacement}' (length: {old_len} -> {new_len})")
            break

    if not found:
        print(f"  STUCK at step {steps}: No rule applies to molecule of length {len(current)}")
        print(f"  Current molecule: {current[:100]}...")
        break

    if current == 'e':
        print(f"  SUCCESS: Reached 'e' in {steps} steps")
        break

# Check formula
print(f"\nFormula approach:")
num_elements = count_elements(target)
num_rn = target.count('Rn')
num_ar = target.count('Ar')
num_y = target.count('Y')
formula_result = num_elements - num_rn - num_ar - 2 * num_y - 1

print(f"  Elements: {num_elements}")
print(f"  Rn: {num_rn}, Ar: {num_ar}, Y: {num_y}")
print(f"  Formula result: {formula_result}")
