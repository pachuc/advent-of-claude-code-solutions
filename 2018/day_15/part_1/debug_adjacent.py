#!/usr/bin/env python3
"""Debug the adjacent combat scenario"""

from solution import parse_input, execute_round

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

round_num = 0
while True:
    round_num += 1
    print(f"Round {round_num} starts:")
    print(f"  Before: Goblin HP={goblin.hp}, Elf HP={elf.hp}")

    # Execute the round
    complete = execute_round(units, grid)

    print(f"  After: Goblin HP={goblin.hp if goblin.alive else 'dead'}, Elf HP={elf.hp if elf.alive else 'dead'}")
    print(f"  Round complete: {complete}")

    if not complete:
        print(f"\nCombat ended mid-round {round_num}")
        print(f"Completed rounds: {round_num - 1}")
        break

    # Check if anyone died
    if not goblin.alive or not elf.alive:
        print(f"\nCombat ended after round {round_num}")
        print(f"Completed rounds: {round_num}")
        break

    if round_num > 70:
        print(f"\nStopping at round {round_num} to prevent infinite loop")
        break

print()
print("Final state:")
if goblin.alive:
    print(f"  Goblin survived with {goblin.hp} HP")
if elf.alive:
    print(f"  Elf survived with {elf.hp} HP")

print()
print("Analysis:")
print(f"  Expected: 66 completed rounds (combat ends mid-round 67)")
print(f"  Expected winner: Goblin with 2 HP")
print(f"  Expected outcome: 66 × 2 = 132")
