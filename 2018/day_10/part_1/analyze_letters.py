"""
Script to analyze the visual output letter by letter.
"""

# The message from the output
message = """#       #####    ####   #####   #####   #    #  ######  ######
#       #    #  #    #  #    #  #    #  #    #  #            #
#       #    #  #       #    #  #    #  #    #  #            #
#       #    #  #       #    #  #    #  #    #  #           #
#       #####   #       #####   #####   ######  #####      #
#       #  #    #  ###  #       #    #  #    #  #         #
#       #   #   #    #  #       #    #  #    #  #        #
#       #   #   #    #  #       #    #  #    #  #       #
#       #    #  #   ##  #       #    #  #    #  #       #
######  #    #   ### #  #       #####   #    #  ######  ######"""

lines = message.split('\n')

# Try different letter widths and separations
# Letters typically are 6-8 characters wide with spacing
# Let me manually find letter boundaries by looking at gaps

# Find where vertical gaps (all spaces in a column) occur
width = len(lines[0])
height = len(lines)

print(f"Total width: {width}, height: {height}")
print()

# Check each column for all spaces
columns_with_content = []
for col in range(width):
    has_content = False
    for row in range(height):
        if col < len(lines[row]) and lines[row][col] == '#':
            has_content = True
            break
    if has_content:
        columns_with_content.append(col)

print(f"Columns with content: {columns_with_content}")
print()

# Find gaps (consecutive columns without content)
gaps = []
if columns_with_content:
    for i in range(len(columns_with_content) - 1):
        gap_size = columns_with_content[i+1] - columns_with_content[i] - 1
        if gap_size > 0:
            gaps.append((columns_with_content[i] + 1, columns_with_content[i+1] - 1, gap_size))

print("Gaps found (start, end, size):")
for gap in gaps:
    print(f"  Columns {gap[0]}-{gap[1]}: {gap[2]} spaces")
print()

# Let's extract letters based on larger gaps (2+ spaces)
letter_boundaries = []
start = 0
for gap in gaps:
    if gap[2] >= 2:  # Gap of 2 or more spaces indicates letter separation
        letter_boundaries.append((start, gap[0] - 1))
        start = gap[1] + 1
# Don't forget the last letter
letter_boundaries.append((start, width - 1))

print(f"Found {len(letter_boundaries)} letters:")
print()

# Extract and display each letter
for i, (start, end) in enumerate(letter_boundaries, 1):
    print(f"Letter {i} (columns {start}-{end}):")
    for row in lines:
        # Ensure we don't go out of bounds
        segment = row[start:end+1] if start < len(row) else ''
        print(f"  |{segment}|")
    print()
