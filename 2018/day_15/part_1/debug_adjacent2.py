#!/usr/bin/env python3
"""Debug the adjacent combat scenario with more detail"""

from solution import parse_input, execute_round, simulate_combat, calculate_outcome

test_input = """#####
#GE##
#####"""

grid, units = parse_input(test_input)

goblin = units[0]
elf = units[1]

print(f"Initial state:")
print(f"  Goblin at ({goblin.x}, {goblin.y}), HP: {goblin.hp}")
print(f"  Elf at ({elf.x}, {elf.y}), HP: {elf.hp}")
print()

# Use simulate_combat
rounds = simulate_combat(grid, units)
outcome = calculate_outcome(rounds, units)

print(f"Completed rounds: {rounds}")
print(f"Goblin HP: {goblin.hp if goblin.alive else 'dead'}")
print(f"Elf HP: {elf.hp if elf.alive else 'dead'}")
print(f"Outcome: {outcome}")
print()
print(f"Expected per test plan: 66 rounds, Goblin with 2 HP, outcome = 132")
print(f"Actual: {rounds} rounds, Goblin with {goblin.hp if goblin.alive else 0} HP, outcome = {outcome}")
