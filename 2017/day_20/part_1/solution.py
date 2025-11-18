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

def manhattan_distance(vector):
    """Calculate Manhattan distance of a 3D vector"""
    return abs(vector[0]) + abs(vector[1]) + abs(vector[2])

def find_closest_particle(particles):
    """
    Find particle that stays closest to origin in the long term.

    Mathematical basis:
    - Position: p(t) = p₀ + v₀·t + ½a·t²
    - As t → ∞, the t² term dominates
    - Therefore: particle with smallest |a| will be closest
    - Tiebreakers: velocity magnitude (t term), then position magnitude (constant)
    """
    if not particles:
        raise ValueError("No particles found in input")

    candidates = []
    for particle in particles:
        accel_mag = manhattan_distance(particle['a'])
        vel_mag = manhattan_distance(particle['v'])
        pos_mag = manhattan_distance(particle['p'])
        candidates.append((accel_mag, vel_mag, pos_mag, particle['index']))

    closest = min(candidates)
    return closest[3]

def main():
    with open('input.md', 'r') as f:
        lines = f.readlines()

    particles = parse_particles(lines)
    result = find_closest_particle(particles)
    print(result)

if __name__ == '__main__':
    main()
