#!/usr/bin/env python3
"""
Detailed verification of the complex example: dabAcCaCBAcCcaDA -> dabCBAcaDA
"""

from solution import reacts, react_polymer

def trace_polymer_reaction(polymer):
    """
    Trace through the polymer reaction step-by-step to verify algorithm.
    """
    print(f"Input polymer: '{polymer}'")
    print(f"Length: {len(polymer)}\n")

    stack = []
    step = 0

    for i, unit in enumerate(polymer):
        step += 1
        print(f"Step {step}: Processing '{unit}' (position {i})")

        if stack and reacts(stack[-1], unit):
            popped = stack.pop()
            print(f"  -> Reaction! '{popped}' and '{unit}' destroy each other")
            print(f"  -> Stack after reaction: {stack}")
        else:
            stack.append(unit)
            print(f"  -> No reaction, added '{unit}' to stack")
            print(f"  -> Stack: {stack}")

        print()

    final_polymer = ''.join(stack)
    print(f"Final polymer: '{final_polymer}'")
    print(f"Final length: {len(final_polymer)}")

    return final_polymer

def main():
    print("=" * 70)
    print("COMPLEX EXAMPLE VERIFICATION")
    print("=" * 70)
    print()

    test_polymer = "dabAcCaCBAcCcaDA"
    expected_final = "dabCBAcaDA"
    expected_length = 10

    print("Testing complex example from problem statement:")
    print(f"  Input: '{test_polymer}'")
    print(f"  Expected final: '{expected_final}'")
    print(f"  Expected length: {expected_length}")
    print()
    print("-" * 70)
    print()

    final_polymer = trace_polymer_reaction(test_polymer)

    print()
    print("=" * 70)
    print("VERIFICATION RESULTS")
    print("=" * 70)

    # Verify using the solution function
    result_length, result_polymer = react_polymer(test_polymer, return_polymer=True)

    print(f"Expected: '{expected_final}' (length {expected_length})")
    print(f"Got:      '{result_polymer}' (length {result_length})")
    print()

    if result_polymer == expected_final and result_length == expected_length:
        print("✓ CORRECT! The solution matches the expected output.")
    else:
        print("✗ INCORRECT! The solution does not match expected output.")

        if result_length == expected_length:
            print("  Length matches but final polymer differs.")
        else:
            print(f"  Length mismatch: got {result_length}, expected {expected_length}")

        if result_polymer != expected_final:
            print(f"  Polymer mismatch:")
            print(f"    Expected: '{expected_final}'")
            print(f"    Got:      '{result_polymer}'")

if __name__ == '__main__':
    main()
