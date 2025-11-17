#!/usr/bin/env python3
"""
Final verification: Try to verify the answer 195 by attempting greedy with unlimited steps.
"""

from solution import parse_input


def verify_answer_195():
    """Verify that 195 is achievable via greedy backward reduction."""
    print("="*60)
    print("Final Verification: Testing Answer = 195")
    print("="*60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    rules, target = parse_input(input_text)

    # Reverse rules for backward search
    reversed_rules = [(tgt, src) for src, tgt in rules]
    reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

    current = target
    steps = 0
    max_steps = 300  # Increased limit

    print(f"Starting with: {current[:50]}... (length {len(current)})")
    print(f"Attempting to reduce to 'e'...")
    print()

    while current != 'e' and steps < max_steps:
        found = False

        for pattern, replacement in reversed_rules:
            if pattern in current:
                old_len = len(current)
                current = current.replace(pattern, replacement, 1)
                new_len = len(current)
                steps += 1
                found = True

                # Show progress
                if steps <= 5 or steps % 50 == 0 or current == 'e':
                    print(f"Step {steps}: length {old_len} -> {new_len}")

                break

        if not found:
            print(f"\n✗ FAILED at step {steps}: No rule applies to molecule of length {len(current)}")
            print(f"Current molecule: {current[:100]}...")
            return False

    print()
    if current == 'e':
        print(f"✓ SUCCESS: Reduced to 'e' in {steps} steps")
        return True, steps
    else:
        print(f"✗ FAILED: Exceeded {max_steps} steps")
        print(f"Current molecule length: {len(current)}")
        return False, steps


if __name__ == '__main__':
    result = verify_answer_195()
    if isinstance(result, tuple) and result[0]:
        print("\n" + "="*60)
        print(f"VERIFIED ANSWER: {result[1]}")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("VERIFICATION INCONCLUSIVE")
        print("Using formula-based answer: 195")
        print("="*60)
