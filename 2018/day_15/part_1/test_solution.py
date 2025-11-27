from solution import *


def test_parse_input():
    """Test parsing"""
    input_text = """#######
#.G.E.#
#######"""
    grid, units = parse_input(input_text)

    assert len(units) == 2
    assert units[0].type == 'G'
    assert units[0].x == 2 and units[0].y == 1
    assert units[1].type == 'E'
    assert units[1].x == 4 and units[1].y == 1
    print("✓ Parse input test passed")


def test_reading_order():
    """Test reading order sorting"""
    units = [
        Unit(5, 2, 'G'),
        Unit(1, 1, 'E'),
        Unit(3, 1, 'G'),
        Unit(2, 3, 'E')
    ]

    sorted_units = sort_units(units)
    positions = [(u.x, u.y) for u in sorted_units]
    assert positions == [(1, 1), (3, 1), (5, 2), (2, 3)]
    print("✓ Reading order test passed")


def test_adjacent_combat():
    """Test scenario where units start adjacent"""
    input_text = """#####
#GE##
#####"""
    grid, units = parse_input(input_text)

    rounds = simulate_combat(grid, units)
    living = [u for u in units if u.alive]

    # Both start with 200 HP, deal 3 damage
    # After 67 rounds: both at 2 HP (200 - 67*3 = -1, but actually 2 HP)
    # Actually: Round 1: 197, Round 2: 194, ..., Round 66: 2 HP each
    # Round 67: G(2) attacks E(2->-1), E dies
    # Round 68 starts: G finds no targets, ends mid-round
    # So 67 complete rounds
    assert rounds == 67, f"Expected 67 rounds, got {rounds}"
    assert len(living) == 1, f"Expected 1 survivor, got {len(living)}"
    assert living[0].type == 'G'
    assert living[0].hp == 2

    outcome = calculate_outcome(rounds, units)
    assert outcome == 134, f"Expected outcome 134, got {outcome}"
    print("✓ Adjacent combat test passed")


def test_move_and_attack():
    """Test a unit can move and attack in same turn"""
    input_text = """#####
#G.E#
#####"""
    grid, units = parse_input(input_text)

    goblin = units[0]
    elf = units[1]

    # Execute one round
    execute_round(units, grid)

    # Goblin should have moved to (2, 1) and attacked
    assert goblin.x == 2 and goblin.y == 1, f"Goblin at ({goblin.x}, {goblin.y})"
    assert elf.hp == 197, f"Elf HP: {elf.hp}"
    assert goblin.hp == 197, f"Goblin HP: {goblin.hp}"
    print("✓ Move and attack test passed")


def test_bfs_pathfinding():
    """Test BFS returns correct distances"""
    input_text = """#######
#.....#
#.###.#
#.....#
#######"""
    grid, units = parse_input(input_text)

    distances = bfs_distances(grid, 1, 1)

    assert distances[(1, 1)] == 0
    assert distances[(2, 1)] == 1
    assert distances[(1, 2)] == 1
    assert distances[(5, 3)] == 6
    assert (2, 2) not in distances  # Wall
    print("✓ BFS pathfinding test passed")


def run_all_tests():
    """Run all tests"""
    print("Running tests...\n")

    test_parse_input()
    test_reading_order()
    test_bfs_pathfinding()
    test_move_and_attack()
    test_adjacent_combat()

    print("\n✓ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
