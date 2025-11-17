from solution import sum_numbers
import json


# Test provided examples and critical edge cases
test_cases = [
    # Provided examples
    ('[1,2,3]', 6),
    ('{"a":2,"b":4}', 6),
    ('[[[3]]]', 3),
    ('{"a":{"b":4},"c":-1}', 3),
    ('{"a":[-1,1]}', 0),
    ('[-1,{"a":1}]', 0),
    ('[]', 0),
    ('{}', 0),

    # CRITICAL: Boolean handling (bool is subclass of int in Python!)
    ('[true, false, 5]', 5),
    ('{"a":true, "b":false, "c":3}', 3),
    ('[1, true, 2, false]', 3),

    # Float handling
    ('[1.5, 2.5]', 4.0),
    ('{"a":3.14, "b":2}', 5.14),
    ('[1, 2.5, -3.5]', 0.0),

    # Mixed types
    ('["string", 5, true, null, 10]', 15),
    ('[1, "text", 2.5, true, false, null, 3]', 6.5),

    # Negative numbers
    ('[-5, -10, -3]', -18),
    ('[5, -5]', 0),

    # Complex nested
    ('[1, [2, {"a":3, "b":[4, 5]}], 6]', 21),
]

print("Running tests...")
passed = 0
failed = 0

for json_str, expected in test_cases:
    data = json.loads(json_str)
    result = sum_numbers(data)
    # Use approximate equality for floats
    is_correct = abs(result - expected) < 0.0001 if isinstance(expected, float) else result == expected
    status = "PASS" if is_correct else "FAIL"

    if is_correct:
        passed += 1
    else:
        failed += 1

    print(f"[{status}] Input: {json_str[:40]:40} | Expected: {expected:8} | Got: {result:8}")

print(f"\nResults: {passed} passed, {failed} failed")

if failed == 0:
    print("\nAll tests passed! ✓")
else:
    print(f"\n{failed} test(s) failed! ✗")
