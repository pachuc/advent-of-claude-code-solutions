from solution import parse_input

example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
y=13, x=498..504"""

lines = example_input.strip().split('\n')
clay_set = parse_input(lines)

print("Clay positions:")
for y in range(0, 15):
    clay_in_row = sorted([x for x, cy in clay_set if cy == y])
    if clay_in_row:
        print(f"y={y}: {clay_in_row}")
