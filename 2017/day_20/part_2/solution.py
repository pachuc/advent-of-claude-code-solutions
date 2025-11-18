import re

def parse_particles(lines):
    """Parse input lines into particle data structures"""
    particles = []
    for index, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue

        # Extract all numbers (including negatives)
        numbers = list(map(int, re.findall(r'-?\d+', line)))

        # Basic validation: ensure we have exactly 9 numbers (3 for p, 3 for v, 3 for a)
        assert len(numbers) == 9, f"Expected 9 numbers on line {index}, got {len(numbers)}"

        # First 3 are position, next 3 are velocity, last 3 are acceleration
        particle = {
            'index': index,
            'p': tuple(numbers[0:3]),
            'v': tuple(numbers[3:6]),
            'a': tuple(numbers[6:9])
        }
        particles.append(particle)
    return particles

def update_particle(particle):
    """
    Update particle velocity and position for one tick.

    Order matters (per problem spec):
    1. v += a  (update velocity by acceleration)
    2. p += v  (update position by NEW velocity)
    """
    # Unpack current state
    px, py, pz = particle['p']
    vx, vy, vz = particle['v']
    ax, ay, az = particle['a']

    # Step 1: Update velocity
    vx += ax
    vy += ay
    vz += az

    # Step 2: Update position with NEW velocity
    px += vx
    py += vy
    pz += vz

    # Return updated particle
    return {
        'index': particle['index'],
        'p': (px, py, pz),
        'v': (vx, vy, vz),
        'a': (ax, ay, az)
    }

def detect_collisions(particles):
    """
    Detect all particles that collide (share same position).

    Returns: set of particle indices that should be removed
    """
    # Map position -> list of particle indices at that position
    position_map = {}

    for particle in particles:
        pos = particle['p']
        if pos not in position_map:
            position_map[pos] = []
        position_map[pos].append(particle['index'])

    # Find all positions with 2+ particles (collisions)
    indices_to_remove = set()
    for pos, particle_indices in position_map.items():
        if len(particle_indices) >= 2:
            # ALL particles at this position are destroyed
            indices_to_remove.update(particle_indices)

    return indices_to_remove

def simulate_with_collisions(particles, max_ticks_without_collision=50):
    """
    Simulate particle system with collision removal.

    Args:
        particles: List of particle dictionaries
        max_ticks_without_collision: Number of ticks without collision before termination (default: 50)

    Returns: number of particles remaining after all collisions resolved
    """
    particles = list(particles)  # Make a copy to avoid modifying original

    # CRITICAL: Check for initial collisions (particles starting at same position)
    # This must happen BEFORE the first update
    indices_to_remove = detect_collisions(particles)
    if indices_to_remove:
        particles = [p for p in particles if p['index'] not in indices_to_remove]

    # If all particles destroyed initially, return early
    if len(particles) == 0:
        return 0

    # Track ticks without collisions for termination
    ticks_without_collision = 0
    MAX_ITERATIONS = 1000  # Safety limit to prevent infinite loops

    for iteration in range(MAX_ITERATIONS):
        # Step 1: Update all particles simultaneously
        particles = [update_particle(p) for p in particles]

        # Step 2: Detect collisions
        indices_to_remove = detect_collisions(particles)

        # Step 3: Remove colliding particles
        if indices_to_remove:
            particles = [p for p in particles if p['index'] not in indices_to_remove]
            ticks_without_collision = 0  # Reset counter
        else:
            ticks_without_collision += 1

        # Step 4: Check termination conditions
        if len(particles) == 0:
            return 0

        if ticks_without_collision >= max_ticks_without_collision:
            # No collisions for N ticks - system has stabilized
            return len(particles)

    # If we reach max iterations, the system should have stabilized by now
    # This is a safety measure in case of bugs
    raise RuntimeError(f"Simulation did not converge after {MAX_ITERATIONS} iterations")

def main():
    # Read input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse particles
    particles = parse_particles(lines)

    # Run simulation
    result = simulate_with_collisions(particles)

    # Output result
    print(result)

if __name__ == '__main__':
    main()
