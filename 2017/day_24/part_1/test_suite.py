#!/usr/bin/env python3
"""Comprehensive test suite for bridge builder solution."""

from solution import solve

def run_test(test_name, components, expected):
    """Run a single test and report results."""
    result = solve(components)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {test_name}: Expected {expected}, got {result}")
    return passed

# Track results
total_tests = 0
passed_tests = 0

print("Running comprehensive test suite...\n")

# Test 1: Example from problem statement
total_tests += 1
if run_test("Test 1: Example case",
            [(0,2), (2,2), (2,3), (3,4), (3,5), (0,1), (10,1), (9,10)],
            31):
    passed_tests += 1

# Test 2: Linear chain
total_tests += 1
if run_test("Test 2: Linear chain",
            [(0,1), (1,2), (2,3), (3,4)],
            20):
    passed_tests += 1

# Test 3: Multiple starting options
total_tests += 1
if run_test("Test 3: Multiple starting options",
            [(0,1), (0,10), (10,5)],
            25):
    passed_tests += 1

# Test 4: Branching paths
total_tests += 1
if run_test("Test 4: Branching paths",
            [(0,2), (2,3), (2,5), (3,1), (5,10)],
            24):
    passed_tests += 1

# Test 5: Component with same ports
total_tests += 1
if run_test("Test 5: Same ports (5/5)",
            [(0,5), (5,5), (5,3)],
            23):
    passed_tests += 1

# Test 6: Single component
total_tests += 1
if run_test("Test 6: Single component",
            [(0,7)],
            7):
    passed_tests += 1

# Test 7: No valid bridge
total_tests += 1
if run_test("Test 7: No valid bridge",
            [(5,7), (3,4), (10,11)],
            0):
    passed_tests += 1

# Test 8: All components have port 0
total_tests += 1
if run_test("Test 8: All components port 0",
            [(0,5), (0,3), (0,10)],
            10):
    passed_tests += 1

# Test 9: Circular potential
total_tests += 1
if run_test("Test 9: Circular potential",
            [(0,1), (1,2), (2,1), (1,3)],
            11):
    passed_tests += 1

# Test 10: Empty input
total_tests += 1
if run_test("Test 10: Empty input",
            [],
            0):
    passed_tests += 1

# Test 11: Component 0/0
total_tests += 1
if run_test("Test 11: Component 0/0",
            [(0,0), (0,5), (5,3)],
            13):
    passed_tests += 1

print(f"\n{'='*50}")
print(f"Test Results: {passed_tests}/{total_tests} tests passed")
print(f"{'='*50}")

if passed_tests == total_tests:
    print("SUCCESS: All tests passed!")
else:
    print(f"FAILURE: {total_tests - passed_tests} test(s) failed")
