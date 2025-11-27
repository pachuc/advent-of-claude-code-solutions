from solution import parse_input, count_matching_opcodes

# Load the samples and get some statistics
samples = parse_input("input.md")

print(f"Total number of samples: {len(samples)}")
print()

# Count samples by number of matching opcodes
match_counts = {}
for before, instruction, after in samples:
    matches = count_matching_opcodes(before, instruction, after)
    match_counts[matches] = match_counts.get(matches, 0) + 1

print("Distribution of matching opcodes:")
for num_matches in sorted(match_counts.keys()):
    count = match_counts[num_matches]
    marker = " ***" if num_matches >= 3 else ""
    print(f"  {num_matches} matches: {count} samples{marker}")

print()
samples_with_3_or_more = sum(count for matches, count in match_counts.items() if matches >= 3)
print(f"Samples with 3+ matching opcodes: {samples_with_3_or_more}")
