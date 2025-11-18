"""Verify the cube coordinate invariant x + y + z = 0 is maintained"""
from solution import DIRECTION_DELTAS, parse_input

def verify_invariant():
    """Check that x + y + z = 0 after every move on actual input"""
    moves = parse_input('input.md')

    x, y, z = 0, 0, 0
    violations = 0

    for i, move in enumerate(moves):
        dx, dy, dz = DIRECTION_DELTAS[move]
        x += dx
        y += dy
        z += dz

        # Check invariant
        if x + y + z != 0:
            print(f"Violation at move {i+1}: ({x}, {y}, {z}), sum = {x+y+z}")
            violations += 1
            if violations > 10:  # Only show first 10 violations
                print("...")
                break

    if violations == 0:
        print(f"✓ Cube coordinate invariant verified for all {len(moves)} moves")
        print(f"  Final position: ({x}, {y}, {z})")
        print(f"  Final sum (should be 0): {x + y + z}")
        return True
    else:
        print(f"✗ Found {violations} violations of the invariant")
        return False

if __name__ == '__main__':
    success = verify_invariant()
    exit(0 if success else 1)
