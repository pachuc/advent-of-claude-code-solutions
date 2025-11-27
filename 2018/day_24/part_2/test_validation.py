import re
from typing import List, Dict, Set, Tuple, Optional

DEBUG = False

def log(message):
    if DEBUG:
        print(message)

class Group:
    """Represents a combat group in the battle."""

    def __init__(self, group_id: int, army: str, units: int, hit_points: int,
                 attack_damage: int, attack_type: str, initiative: int,
                 weaknesses: Set[str] = None, immunities: Set[str] = None):
        self.id = group_id
        self.army = army
        self.units = units
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses if weaknesses else set()
        self.immunities = immunities if immunities else set()

    def effective_power(self) -> int:
        """Calculate the effective power of this group."""
        return self.units * self.attack_damage

    def calculate_damage_to(self, defender: 'Group') -> int:
        """Calculate damage this group would deal to another group."""
        # If defender is immune to our attack type, deal no damage
        if self.attack_type in defender.immunities:
            return 0

        base_damage = self.effective_power()

        # If defender is weak to our attack type, deal double damage
        if self.attack_type in defender.weaknesses:
            return base_damage * 2

        # Otherwise, deal normal damage
        return base_damage

    def take_damage(self, damage: int) -> int:
        """
        Apply damage to this group and remove killed units.
        Returns the number of units killed.
        """
        units_killed = damage // self.hit_points
        units_killed = min(units_killed, self.units)  # Can't kill more units than we have
        self.units -= units_killed
        return units_killed

    def is_alive(self) -> bool:
        """Check if this group still has units."""
        return self.units > 0

    def __repr__(self):
        return f"Group {self.id} ({self.army}): {self.units} units, EP={self.effective_power()}, init={self.initiative}"


def parse_modifiers(modifier_text: str) -> Tuple[Set[str], Set[str]]:
    """
    Parse the modifier section (weaknesses and immunities).
    Returns (weaknesses, immunities) as sets.
    """
    weaknesses = set()
    immunities = set()

    if not modifier_text:
        return weaknesses, immunities

    # Split by semicolon to separate weak/immune sections
    sections = modifier_text.split(';')

    for section in sections:
        section = section.strip()
        if 'weak to' in section:
            # Extract damage types after "weak to"
            types_text = section.split('weak to')[1].strip()
            types = [t.strip() for t in types_text.split(',')]
            weaknesses.update(types)
        elif 'immune to' in section:
            # Extract damage types after "immune to"
            types_text = section.split('immune to')[1].strip()
            types = [t.strip() for t in types_text.split(',')]
            immunities.update(types)

    return weaknesses, immunities


def parse_input(filename: str) -> Tuple[List[Group], List[Group]]:
    """Parse the input file and return lists of groups for each army."""
    with open(filename, 'r') as f:
        content = f.read()

    # Split into sections
    sections = content.split('\n\n')
    immune_section = sections[0]
    infection_section = sections[1]

    immune_groups = []
    infection_groups = []

    # Regex pattern to parse each line
    pattern = r'(\d+) units each with (\d+) hit points (?:\(([^)]+)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)'

    # Parse Immune System groups
    immune_lines = immune_section.split('\n')[1:]  # Skip header
    for i, line in enumerate(immune_lines):
        line = line.strip()
        if not line:
            continue

        match = re.match(pattern, line)
        if match:
            units = int(match.group(1))
            hit_points = int(match.group(2))
            modifiers = match.group(3)
            attack_damage = int(match.group(4))
            attack_type = match.group(5)
            initiative = int(match.group(6))

            weaknesses, immunities = parse_modifiers(modifiers)

            group = Group(i + 1, "Immune System", units, hit_points,
                         attack_damage, attack_type, initiative,
                         weaknesses, immunities)
            immune_groups.append(group)

    # Parse Infection groups
    infection_lines = infection_section.split('\n')[1:]  # Skip header
    for i, line in enumerate(infection_lines):
        line = line.strip()
        if not line:
            continue

        match = re.match(pattern, line)
        if match:
            units = int(match.group(1))
            hit_points = int(match.group(2))
            modifiers = match.group(3)
            attack_damage = int(match.group(4))
            attack_type = match.group(5)
            initiative = int(match.group(6))

            weaknesses, immunities = parse_modifiers(modifiers)

            group = Group(i + 1, "Infection", units, hit_points,
                         attack_damage, attack_type, initiative,
                         weaknesses, immunities)
            infection_groups.append(group)

    return immune_groups, infection_groups


def apply_boost(immune_groups: List[Group], boost: int) -> List[Group]:
    """
    Apply boost to immune groups' attack damage in-place.
    Returns the modified list.
    """
    for group in immune_groups:
        group.attack_damage += boost
    return immune_groups


def target_selection(immune_groups: List[Group], infection_groups: List[Group]) -> Dict[Group, Group]:
    """
    Execute target selection phase.
    Returns dictionary mapping attacker -> defender.
    """
    # Combine all alive groups
    all_groups = [g for g in immune_groups + infection_groups if g.is_alive()]

    # Sort groups by effective power (desc), then initiative (desc)
    all_groups.sort(key=lambda g: (-g.effective_power(), -g.initiative))

    targets = {}
    targeted_groups = set()

    for attacker in all_groups:
        # Get enemy groups
        if attacker.army == "Immune System":
            enemies = [g for g in infection_groups if g.is_alive()]
        else:
            enemies = [g for g in immune_groups if g.is_alive()]

        # Filter out already targeted groups
        available_enemies = [e for e in enemies if e not in targeted_groups]

        # Calculate damage to each potential target
        valid_targets = []
        for enemy in available_enemies:
            damage = attacker.calculate_damage_to(enemy)
            if damage > 0:  # Only consider targets we can actually damage
                valid_targets.append((enemy, damage))

        if not valid_targets:
            continue  # No valid targets for this attacker

        # Select target with highest damage, break ties by effective power, then initiative
        target = max(valid_targets, key=lambda t: (t[1], t[0].effective_power(), t[0].initiative))

        targets[attacker] = target[0]
        targeted_groups.add(target[0])

        log(f"  {attacker.army} group {attacker.id} targets {target[0].army} group {target[0].id} for {target[1]} damage")

    return targets


def attack_phase(targets: Dict[Group, Group]) -> int:
    """
    Execute attack phase.
    Returns the number of units killed this round.
    """
    # Sort attackers by initiative (descending)
    attackers = sorted(targets.keys(), key=lambda g: -g.initiative)

    total_units_killed = 0

    for attacker in attackers:
        # Check if attacker is still alive
        if not attacker.is_alive():
            continue

        defender = targets[attacker]

        # Calculate damage with current effective power
        damage = attacker.calculate_damage_to(defender)

        # Apply damage
        units_before = defender.units
        units_killed = defender.take_damage(damage)
        total_units_killed += units_killed

        log(f"  {attacker.army} group {attacker.id} attacks {defender.army} group {defender.id}, killing {units_killed} units")

    return total_units_killed


def simulate_combat(immune_groups: List[Group], infection_groups: List[Group]) -> Tuple[str, int]:
    """
    Simulate the entire combat.
    Returns (winning_army_name, total_units_remaining).
    """
    round_num = 0

    while True:
        round_num += 1
        log(f"\n=== Round {round_num} ===")

        # Filter out dead groups
        immune_groups = [g for g in immune_groups if g.is_alive()]
        infection_groups = [g for g in infection_groups if g.is_alive()]

        # Check termination conditions
        immune_units = sum(g.units for g in immune_groups)
        infection_units = sum(g.units for g in infection_groups)

        log(f"Immune System: {immune_units} units in {len(immune_groups)} groups")
        log(f"Infection: {infection_units} units in {len(infection_groups)} groups")

        if not immune_groups and not infection_groups:
            return "Stalemate", 0
        if not immune_groups:
            return "Infection", infection_units
        if not infection_groups:
            return "Immune System", immune_units

        # Target selection phase
        log("Target selection:")
        targets = target_selection(immune_groups, infection_groups)

        if not targets:
            # No valid targets (stalemate due to immunities)
            log("No valid targets - stalemate!")
            return "Stalemate", immune_units + infection_units

        # Attack phase
        log("Attacks:")
        units_killed = attack_phase(targets)

        if units_killed == 0:
            # Stalemate - no damage dealt
            log("No units killed - stalemate!")
            return "Stalemate", immune_units + infection_units

        log(f"Total units killed this round: {units_killed}")


def find_minimum_boost() -> int:
    """
    Find the minimum boost that allows Immune System to win.
    Uses binary search to find the optimal boost value.
    """
    left = 1
    right = 10000  # Conservative upper bound

    while left < right:
        mid = (left + right) // 2

        # Parse fresh groups for simulation (combat mutates groups)
        immune_groups, infection_groups = parse_input("input.md")

        # Apply boost to immune system (modifies in-place)
        apply_boost(immune_groups, mid)

        # Simulate combat (returns 2-tuple from Part 1)
        winner, units = simulate_combat(immune_groups, infection_groups)

        if winner == "Immune System":
            # This boost works, try smaller
            right = mid
        else:
            # This boost doesn't work (Infection wins or stalemate), try larger
            left = mid + 1

    # Validate that we found a winning boost
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, left)
    winner, units = simulate_combat(immune_groups, infection_groups)

    if winner != "Immune System":
        raise ValueError(f"No winning boost found in range [1, {right}]. Try increasing upper bound.")

    # left is now the minimum boost
    return left


def main():
    # Find minimum boost using binary search
    min_boost = find_minimum_boost()
    print(f"Minimum boost found: {min_boost}")

    # Test with boost - 1 (should NOT win)
    print(f"\nTesting with boost {min_boost - 1}:")
    immune, infection = parse_input("input.md")
    apply_boost(immune, min_boost - 1)
    winner, units = simulate_combat(immune, infection)
    print(f"  Winner: {winner}, Units: {units}")
    if winner == "Immune System":
        print(f"  ERROR: Boost {min_boost - 1} should not win!")
    else:
        print(f"  PASS: Boost {min_boost - 1} does not win (as expected)")

    # Test with min_boost (should win)
    print(f"\nTesting with boost {min_boost}:")
    immune, infection = parse_input("input.md")
    apply_boost(immune, min_boost)
    winner, units = simulate_combat(immune, infection)
    print(f"  Winner: {winner}, Units: {units}")
    if winner == "Immune System":
        print(f"  PASS: Boost {min_boost} wins with {units} units")
    else:
        print(f"  ERROR: Boost {min_boost} should win!")

    # Test with boost + 1 (should also win)
    print(f"\nTesting with boost {min_boost + 1}:")
    immune, infection = parse_input("input.md")
    apply_boost(immune, min_boost + 1)
    winner, units = simulate_combat(immune, infection)
    print(f"  Winner: {winner}, Units: {units}")
    if winner == "Immune System":
        print(f"  PASS: Boost {min_boost + 1} wins (as expected)")
    else:
        print(f"  ERROR: Boost {min_boost + 1} should win!")

    print(f"\n=== FINAL ANSWER: {units} units ===")


if __name__ == "__main__":
    main()
