from solution import find_minimum_container_ways

def test_all():
    tests = [
        # (containers, target, expected, description)
        ([150, 50, 30, 20], 150, 1, "Single container equals target"),
        ([25, 25, 10, 15], 25, 2, "Multiple single containers"),
        ([1] * 10, 5, 252, "Many containers (C(10,5))"),
        ([10, 10, 5, 5], 15, 4, "Duplicate values"),
        ([50, 30, 20, 10], 110, 1, "All containers needed"),
    ]
    
    all_passed = True
    for containers, target, expected, description in tests:
        result = find_minimum_container_ways(containers, target)
        passed = result == expected
        all_passed = all_passed and passed
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {description}")
        if not passed:
            print(f"  Expected: {expected}, Got: {result}")
    
    print()
    if all_passed:
        print("All edge case tests PASSED!")
    else:
        print("Some tests FAILED!")
    
    return all_passed

test_all()
