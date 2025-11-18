"""
Verification script for actual input
"""

from solution import parse_input, simulate_virus


def verify_actual():
    """Verify actual input processing."""
    print("Verifying actual input...")

    # Parse actual input
    infected_nodes, center = parse_input('input.md')

    print(f"Grid center position: {center}")
    print(f"Initial infected nodes count: {len(infected_nodes)}")
    print()

    # Run simulation
    result = simulate_virus(infected_nodes, center, 10000)
    print(f"Result after 10,000 bursts: {result} infections")


if __name__ == '__main__':
    verify_actual()
