from solution import parse_instructions, execute


def run_test(name, input_str, expected):
    """Run a single test case."""
    instructions = parse_instructions(input_str.strip().split('\n'))
    result = execute(instructions)
    if result == expected:
        print(f"✓ {name}: PASS (result={result})")
        return True
    else:
        print(f"✗ {name}: FAIL (expected {expected}, got {result})")
        return False


def main():
    """Run all test cases."""
    passed = 0
    total = 0

    # Test 1: Example from Problem Statement
    total += 1
    test1 = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    if run_test("Test 1: Example from problem", test1, 42):
        passed += 1

    # Test 2: Copy Register to Register
    total += 1
    test2 = """cpy 10 a
cpy a b
cpy b c"""
    if run_test("Test 2: Copy register to register", test2, 10):
        passed += 1

    # Test 3: Jump with Zero (No Jump)
    total += 1
    test3 = """cpy 0 a
jnz a 5
inc a
inc a
inc a"""
    if run_test("Test 3: Jump with zero (no jump)", test3, 3):
        passed += 1

    # Test 4: Backward Jump (Loop)
    total += 1
    test4 = """cpy 5 a
dec a
jnz a -1"""
    if run_test("Test 4: Backward jump (loop)", test4, 0):
        passed += 1

    # Test 5: Nested Loops (Simple Multiplication)
    total += 1
    test5 = """cpy 3 a
cpy 2 b
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec c
jnz c -5"""
    if run_test("Test 5: Nested loops", test5, 9):
        passed += 1

    # Test 6: Jump Past End of Program
    total += 1
    test6 = """cpy 5 a
jnz a 10
inc a"""
    if run_test("Test 6: Jump past end of program", test6, 5):
        passed += 1

    # Test 7: All Registers Used
    total += 1
    test7 = """cpy 1 a
cpy 2 b
cpy 3 c
cpy 4 d
inc a
inc b
inc c
inc d"""
    if run_test("Test 7: All registers used", test7, 2):
        passed += 1

    # Test 8: Decrement Below Zero
    total += 1
    test8 = """cpy 0 a
dec a
dec a"""
    if run_test("Test 8: Decrement below zero", test8, -2):
        passed += 1

    # Test 9: Jump with Register Offset
    total += 1
    test9 = """cpy 2 b
cpy 1 a
jnz a b
inc a
inc a"""
    if run_test("Test 9: Jump with register offset", test9, 1):
        passed += 1

    # Summary
    print("\n" + "="*50)
    print(f"Tests passed: {passed}/{total}")
    if passed == total:
        print("All tests PASSED! ✓")
    else:
        print(f"Some tests FAILED ({total - passed} failures)")
    print("="*50)


if __name__ == '__main__':
    main()
