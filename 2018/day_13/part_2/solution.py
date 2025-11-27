class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.intersection_count = 0
        self.removed = False  # New attribute for Part 2

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, {self.direction}, removed={self.removed})"


def parse_input(filename):
    """Parse the input file to extract track and carts."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove newlines but preserve the structure
    lines = [line.rstrip('\n') for line in lines]

    # Find max width
    max_width = max(len(line) for line in lines) if lines else 0

    # Pad lines to same width
    lines = [line.ljust(max_width) for line in lines]

    # Create track grid
    track = [list(line) for line in lines]

    # Extract carts
    carts = []
    cart_chars = {'^': 'UP', 'v': 'DOWN', '<': 'LEFT', '>': 'RIGHT'}
    cart_to_track = {'^': '|', 'v': '|', '<': '-', '>': '-'}

    for y, line in enumerate(track):
        for x, char in enumerate(line):
            if char in cart_chars:
                direction = cart_chars[char]
                carts.append(Cart(x, y, direction))
                # Replace cart with underlying track
                track[y][x] = cart_to_track[char]

    return track, carts


def turn_left(direction):
    """Turn left from current direction."""
    turns = {'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT', 'RIGHT': 'UP'}
    return turns[direction]


def turn_right(direction):
    """Turn right from current direction."""
    turns = {'UP': 'RIGHT', 'RIGHT': 'DOWN', 'DOWN': 'LEFT', 'LEFT': 'UP'}
    return turns[direction]


def apply_curve(direction, curve):
    """Apply curve transformation to direction."""
    if curve == '/':
        # / curve transformations
        transforms = {'UP': 'RIGHT', 'RIGHT': 'UP', 'DOWN': 'LEFT', 'LEFT': 'DOWN'}
    elif curve == '\\':
        # \ curve transformations
        transforms = {'UP': 'LEFT', 'LEFT': 'UP', 'DOWN': 'RIGHT', 'RIGHT': 'DOWN'}
    else:
        return direction

    return transforms[direction]


def get_direction_delta(direction):
    """Get the x,y delta for a direction."""
    deltas = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    return deltas[direction]


def move_cart(cart, track):
    """Move cart one step and update its direction based on track."""
    # Get movement delta
    dx, dy = get_direction_delta(cart.direction)

    # Move cart
    cart.x += dx
    cart.y += dy

    # Get track type at new position
    track_char = track[cart.y][cart.x]

    # Update direction based on track type
    if track_char == '/':
        cart.direction = apply_curve(cart.direction, '/')
    elif track_char == '\\':
        cart.direction = apply_curve(cart.direction, '\\')
    elif track_char == '+':
        # Intersection - apply turn pattern
        turn_action = cart.intersection_count % 3
        if turn_action == 0:
            # Turn left
            cart.direction = turn_left(cart.direction)
        elif turn_action == 1:
            # Go straight
            pass
        elif turn_action == 2:
            # Turn right
            cart.direction = turn_right(cart.direction)
        cart.intersection_count += 1
    # Else: straight track (- or |), no direction change


def simulate(track, carts):
    """Simulate cart movement until only one cart remains."""
    tick = 0
    while True:
        # Sort all carts by position (top to bottom, left to right)
        # Keep removed carts in the list for stable indices
        carts.sort(key=lambda c: (c.y, c.x))

        # Track positions where collisions occurred this tick
        # This handles multi-cart pile-ups correctly
        collision_positions = set()

        # Move each cart in order
        for i in range(len(carts)):
            # Skip if this cart was already removed
            if carts[i].removed:
                continue

            # Move the cart
            move_cart(carts[i], track)

            # Get current position
            pos = (carts[i].x, carts[i].y)

            # Check if this cart landed on a position where a collision happened this tick
            # This handles 3+ cart pile-ups: if Cart A and B collided at (5,5),
            # and Cart C later moves to (5,5), Cart C should also be removed
            if pos in collision_positions:
                carts[i].removed = True
                continue

            # Check for collisions with other active carts
            for j in range(len(carts)):
                if i != j and not carts[j].removed:
                    if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        # Collision! Remove both carts and mark position
                        carts[i].removed = True
                        carts[j].removed = True
                        collision_positions.add(pos)
                        break  # Stop checking, this cart is removed

        # Check termination condition
        active_carts = [c for c in carts if not c.removed]
        if len(active_carts) == 1:
            return (active_carts[0].x, active_carts[0].y)
        elif len(active_carts) == 0:
            raise Exception("No carts remaining!")

        tick += 1


def solve():
    """Main solve function."""
    track, carts = parse_input('input.md')
    last_x, last_y = simulate(track, carts)
    return f"{last_x},{last_y}"


if __name__ == "__main__":
    result = solve()
    print(result)
