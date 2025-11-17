from solution import sum_of_divisors, calculate_presents, find_lowest_house

def test_sum_of_divisors():
    """Test divisor sum calculation"""
    print("Testing sum_of_divisors:")

    tests = [
        (1, 1, [1]),
        (6, 12, [1, 2, 3, 6]),
        (7, 8, [1, 7]),
        (9, 13, [1, 3, 9]),
        (12, 28, [1, 2, 3, 4, 6, 12]),
        (16, 31, [1, 2, 4, 8, 16]),
    ]

    all_passed = True
    for n, expected_sum, divisors in tests:
        result = sum_of_divisors(n)
        status = "PASS" if result == expected_sum else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  n={n}, divisors={divisors}, expected={expected_sum}, got={result} - {status}")

    return all_passed


def test_calculate_presents():
    """Test present calculation for houses"""
    print("\nTesting calculate_presents (from problem examples):")

    tests = [
        (1, 10),   # House 1: divisors [1], sum=1, presents=10
        (2, 30),   # House 2: divisors [1,2], sum=3, presents=30
        (3, 40),   # House 3: divisors [1,3], sum=4, presents=40
        (4, 70),   # House 4: divisors [1,2,4], sum=7, presents=70
        (6, 120),  # House 6: divisors [1,2,3,6], sum=12, presents=120
    ]

    all_passed = True
    for house, expected in tests:
        result = calculate_presents(house)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  House {house}: expected={expected}, got={result} - {status}")

    return all_passed


def test_find_lowest_house():
    """Test finding lowest house with small targets"""
    print("\nTesting find_lowest_house:")

    # Test 1: Target 130 - should find house 8
    # House 8: divisors [1,2,4,8], sum=15, presents=150 >= 130
    # House 7: divisors [1,7], sum=8, presents=80 < 130
    print("  Test 1: Target 130")
    result = find_lowest_house(130)
    presents = calculate_presents(result)
    prev_presents = calculate_presents(result - 1) if result > 1 else 0
    print(f"    Result: House {result} with {presents} presents")
    print(f"    Previous house ({result-1}): {prev_presents} presents")
    test1_pass = result == 8 and presents >= 130 and prev_presents < 130
    print(f"    Status: {'PASS' if test1_pass else 'FAIL'}")

    # Test 2: Target 10 - should find house 1
    print("  Test 2: Target 10")
    result = find_lowest_house(10)
    presents = calculate_presents(result)
    print(f"    Result: House {result} with {presents} presents")
    test2_pass = result == 1 and presents >= 10
    print(f"    Status: {'PASS' if test2_pass else 'FAIL'}")

    # Test 3: Target 11 - should find house 2
    print("  Test 3: Target 11")
    result = find_lowest_house(11)
    presents = calculate_presents(result)
    prev_presents = calculate_presents(result - 1)
    print(f"    Result: House {result} with {presents} presents")
    print(f"    Previous house ({result-1}): {prev_presents} presents")
    test3_pass = result == 2 and presents >= 11 and prev_presents < 11
    print(f"    Status: {'PASS' if test3_pass else 'FAIL'}")

    return test1_pass and test2_pass and test3_pass


if __name__ == "__main__":
    print("="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)

    test1 = test_sum_of_divisors()
    test2 = test_calculate_presents()
    test3 = test_find_lowest_house()

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"sum_of_divisors tests: {'PASS' if test1 else 'FAIL'}")
    print(f"calculate_presents tests: {'PASS' if test2 else 'FAIL'}")
    print(f"find_lowest_house tests: {'PASS' if test3 else 'FAIL'}")
    print(f"\nOverall: {'ALL TESTS PASSED' if all([test1, test2, test3]) else 'SOME TESTS FAILED'}")
