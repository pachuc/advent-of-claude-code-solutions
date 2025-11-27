"""
Identify each letter by comparing to standard patterns.
"""

# Standard 10-row letter patterns (6 chars wide typically)

# Common patterns for reference:
PATTERNS = {
    'L': ['#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '######'],
    'R': ['##### ', '#    #', '#    #', '#    #', '##### ', '#  #  ', '#   # ', '#   # ', '#    #', '#    #'],
    'C': [' #### ', '#    #', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#    #', ' #### '],
    'G': [' #### ', '#    #', '#     ', '#     ', '#     ', '#  ###', '#    #', '#    #', '#   ##', ' ### #'],
    'P': ['##### ', '#    #', '#    #', '#    #', '##### ', '#     ', '#     ', '#     ', '#     ', '#     '],
    'B': ['##### ', '#    #', '#    #', '#    #', '##### ', '#    #', '#    #', '#    #', '#    #', '##### '],
    'H': ['#    #', '#    #', '#    #', '#    #', '######', '#    #', '#    #', '#    #', '#    #', '#    #'],
    'E': ['######', '#     ', '#     ', '#     ', '##### ', '#     ', '#     ', '#     ', '#     ', '######'],
    'Z': ['######', '     #', '     #', '    # ', '   #  ', '  #   ', ' #    ', '#     ', '#     ', '######'],
}

# The actual letters from our output
letters = [
    ['#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '######'],  # 1
    ['##### ', '#    #', '#    #', '#    #', '##### ', '#  #  ', '#   # ', '#   # ', '#    #', '#    #'],  # 2
    [' #### ', '#    #', '#     ', '#     ', '#     ', '#  ###', '#    #', '#    #', '#   ##', ' ### #'],  # 3
    ['##### ', '#    #', '#    #', '#    #', '##### ', '#     ', '#     ', '#     ', '#     ', '#     '],  # 4
    ['##### ', '#    #', '#    #', '#    #', '##### ', '#    #', '#    #', '#    #', '#    #', '##### '],  # 5
    ['#    #', '#    #', '#    #', '#    #', '######', '#    #', '#    #', '#    #', '#    #', '#    #'],  # 6
    ['######', '#     ', '#     ', '#     ', '##### ', '#     ', '#     ', '#     ', '#     ', '######'],  # 7
    ['######', '     #', '     #', '    # ', '   #  ', '  #   ', ' #    ', '#     ', '#     ', '######'],  # 8
]

def match_letter(letter_lines):
    """Find which pattern matches best."""
    for char, pattern in PATTERNS.items():
        if len(letter_lines) != len(pattern):
            continue
        # Check if all lines match
        matches = True
        for i in range(len(letter_lines)):
            # Normalize to same length
            l1 = letter_lines[i].ljust(6)
            l2 = pattern[i].ljust(6)
            if l1 != l2:
                matches = False
                break
        if matches:
            return char
    return '?'

# Match each letter
result = ''
for i, letter in enumerate(letters, 1):
    matched = match_letter(letter)
    result += matched
    print(f"Letter {i}: {matched}")

print(f"\nFinal answer: {result}")
