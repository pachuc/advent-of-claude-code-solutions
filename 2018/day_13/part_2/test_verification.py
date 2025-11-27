"""Verification script to check that first collision matches Part 1 answer."""

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.intersection_count = 0
        self.removed = False

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, {self.direction}, removed={self.removed})"


def parse_input(filename):
    """Parse the input file to extract track and carts."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.rstrip('\n') for line in lines]
    max_width = max(len(line) for line in lines) if lines else 0
    lines = [line.ljust(max_width) for line in lines]
    track = [list(line) for line in lines]

    carts = []
    cart_chars = {'^': 'UP', 'v': 'DOWN', '<': 'LEFT', '>': 'RIGHT'}
    cart_to_track = {'^': '|', 'v': '|', '<': '-', '>': '-'}

    for y, line in enumerate(track):
        for x, char in enumerate(line):
            if char in cart_chars:
                direction = cart_chars[char]
                carts.append(Cart(x, y, direction))
                track[y][x] = cart_to_track[char]

    return track, carts


def turn_left(direction):
    turns = {'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT', 'RIGHT': 'UP'}
    return turns[direction]


def turn_right(direction):
    turns = {'UP': 'RIGHT', 'RIGHT': 'DOWN', 'DOWN': 'LEFT', 'LEFT': 'UP'}
    return turns[direction]


def apply_curve(direction, curve):
    if curve == '/':
        transforms = {'UP': 'RIGHT', 'RIGHT': 'UP', 'DOWN': 'LEFT', 'LEFT': 'DOWN'}
    elif curve == '\\':
        transforms = {'UP': 'LEFT', 'LEFT': 'UP', 'DOWN': 'RIGHT', 'RIGHT': 'DOWN'}
    else:
        return direction
    return transforms[direction]


def get_direction_delta(direction):
    deltas = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    return deltas[direction]


def move_cart(cart, track):
    dx, dy = get_direction_delta(cart.direction)
    cart.x += dx
    cart.y += dy
    track_char = track[cart.y][cart.x]

    if track_char == '/':
        cart.direction = apply_curve(cart.direction, '/')
    elif track_char == '\\':
        cart.direction = apply_curve(cart.direction, '\\')
    elif track_char == '+':
        turn_action = cart.intersection_count % 3
        if turn_action == 0:
            cart.direction = turn_left(cart.direction)
        elif turn_action == 1:
            pass
        elif turn_action == 2:
            cart.direction = turn_right(cart.direction)
        cart.intersection_count += 1


def simulate_with_logging(track, carts):
    """Simulate cart movement with collision logging."""
    tick = 0
    first_collision = None
    collision_count = 0

    while True:
        carts.sort(key=lambda c: (c.y, c.x))
        collision_positions = set()

        for i in range(len(carts)):
            if carts[i].removed:
                continue

            move_cart(carts[i], track)
            pos = (carts[i].x, carts[i].y)

            if pos in collision_positions:
                carts[i].removed = True
                collision_count += 1
                if first_collision is None:
                    first_collision = pos
                print(f"Tick {tick}: Cart pile-up at {pos[0]},{pos[1]}")
                continue

            for j in range(len(carts)):
                if i != j and not carts[j].removed:
                    if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        carts[i].removed = True
                        carts[j].removed = True
                        collision_positions.add(pos)
                        collision_count += 1
                        if first_collision is None:
                            first_collision = pos
                            print(f"Tick {tick}: FIRST COLLISION at {pos[0]},{pos[1]}")
                        else:
                            print(f"Tick {tick}: Collision at {pos[0]},{pos[1]}")
                        break

        active_carts = [c for c in carts if not c.removed]
        if len(active_carts) == 1:
            print(f"\nSimulation complete!")
            print(f"Total collisions: {collision_count}")
            print(f"First collision: {first_collision[0]},{first_collision[1]}")
            print(f"Last cart remaining at: {active_carts[0].x},{active_carts[0].y}")
            return (active_carts[0].x, active_carts[0].y)
        elif len(active_carts) == 0:
            raise Exception("No carts remaining!")

        tick += 1


if __name__ == "__main__":
    track, carts = parse_input('input.md')
    print(f"Initial cart count: {len(carts)}")
    result = simulate_with_logging(track, carts)
    print(f"\nAnswer: {result[0]},{result[1]}")
