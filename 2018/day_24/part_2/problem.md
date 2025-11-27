# Problem Report: Immune System Simulator - Part 2 (Boosted Combat)

## Context from Part 1

In Part 1, we simulated a battle between the **Immune System** and **Infection** armies, where each army consists of multiple groups that fight until only one army remains. In the original scenario (without any boost), the **Infection** won with **22244** total units remaining.

The combat system works as follows:
- Each group has units with specific attributes (hit points, attack damage, attack type, initiative, weaknesses, immunities)
- Combat proceeds in rounds with two phases: target selection and attacking
- Groups select targets based on maximum potential damage, breaking ties by effective power and initiative
- Attacks occur in initiative order (highest first), dealing damage that kills whole units
- Combat continues until one army is eliminated

## Part 2 Objective

We need to **boost the Immune System** to help it win the battle. A boost is an integer value that increases the attack damage of **every Immune System group** by that amount.

The goal is to find the **smallest boost** that allows the Immune System to win, then determine **how many units the Immune System has left** after victory.

## What Changed with the Boost

When applying a boost value `B`:
- Each Immune System group's `attack_damage` is increased by `B`
- This increases each Immune System group's effective power (units × attack_damage)
- The Infection groups remain unchanged
- All other combat rules remain the same

### Example
In the example provided in the puzzle:
- Original attack damages for Immune System: 4507 and 25
- With a boost of 1570: attack damages become 6077 (4507+1570) and 1595 (25+1570)
- With this boost, the Immune System wins with **51 units** remaining

## Input Format

The input format is identical to Part 1:
- Two sections: "Immune System:" and "Infection:"
- Each group described in format:
  ```
  <units> units each with <hit_points> hit points (<modifiers>) with an attack that does <attack_damage> <attack_type> damage at initiative <initiative>
  ```

## Algorithm Requirements

1. **Find the minimum boost:**
   - Start testing with boost values (suggest binary search or incremental search)
   - For each boost value:
     - Apply boost to all Immune System groups' attack damage
     - Simulate the combat with the boosted values
     - Check if Immune System wins

2. **Winning conditions:**
   - Immune System wins if Infection has no units remaining
   - Need to handle potential stalemates (no damage dealt, immunities prevent progress)
   - The smallest boost must result in a clear Immune System victory

3. **Combat simulation:**
   - Use the same combat rules as Part 1
   - Apply the boost before starting simulation
   - Track which army wins and how many units remain

## Expected Output

A single integer: the total number of units the Immune System has remaining after winning the battle with the **smallest possible boost**.

## Important Considerations

- **Minimum boost:** We must find the *smallest* boost value that allows the Immune System to win
- **Stalemates:** Some boost values might cause stalemates (neither side can damage the other due to immunities). These don't count as wins.
- **Optimization:** Binary search is recommended to find the minimum boost efficiently rather than testing every value
- **Validation:** Once a winning boost is found, verify it's truly the minimum by confirming that (boost - 1) does not result in an Immune System victory

## Task Summary

1. Parse the input file (same format as Part 1)
2. Implement a function to apply a boost to Immune System groups
3. Use the Part 1 combat simulator with boosted values
4. Search for the minimum boost that results in Immune System victory
5. Output the number of Immune System units remaining with that minimum boost
