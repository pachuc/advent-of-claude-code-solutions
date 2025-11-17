def calculate_wrapping_paper(l, w, h):
    """Calculate wrapping paper needed for a single present."""
    # Calculate three side areas
    side1 = l * w
    side2 = w * h
    side3 = h * l

    # Surface area
    surface_area = 2 * (side1 + side2 + side3)

    # Slack is the smallest side
    slack = min(side1, side2, side3)

    return surface_area + slack

def main():
    """Main function to process all presents."""
    # Read input
    with open('input.md', 'r') as f:
        lines = f.read().strip().split('\n')

    # Calculate total
    total = 0
    for line in lines:
        if line:  # Skip empty lines
            l, w, h = map(int, line.split('x'))
            total += calculate_wrapping_paper(l, w, h)

    # Output result
    print(total)

if __name__ == "__main__":
    main()
