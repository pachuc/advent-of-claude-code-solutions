#!/usr/bin/env python3
"""
Verification test suite for Day 25 Part 2
This tests all critical requirements from the test plan
"""

import unittest
import io
import sys
import time
from solution import solve_part2


class TestDay25Part2Verification(unittest.TestCase):
    """Comprehensive verification test suite"""

    def capture_stdout(self, func):
        """Helper to capture stdout from a function"""
        captured = io.StringIO()
        sys.stdout = captured
        func()
        sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_1_1_execution_completes(self):
        """Test 1.1: Verify function executes without errors"""
        try:
            solve_part2()
            # If we get here, no exception was raised
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"solve_part2() raised an exception: {e}")

    def test_2_1_returns_value(self):
        """Test 2.1: Verify function returns a value"""
        result = solve_part2()
        self.assertIsNotNone(result, "Function should return a value, not None")
        self.assertIsInstance(result, str, "Return value should be a string")

    def test_2_2_return_value_content(self):
        """Test 2.2: Verify return value indicates milestone"""
        result = solve_part2()
        keywords = ["50th", "Star", "Completion", "Milestone", "Complete"]
        has_keyword = any(kw in result for kw in keywords)
        self.assertTrue(has_keyword,
                       f"Return value should contain milestone keywords. Got: {result}")

    def test_1_3_output_critical_elements(self):
        """Test 1.3: Verify output contains all critical elements"""
        output = self.capture_stdout(solve_part2)

        # Critical check 1: Reference to Part 2
        has_part2_ref = "Day 25 Part 2" in output or "Part 2" in output
        self.assertTrue(has_part2_ref,
                       "Output must reference 'Day 25 Part 2' or 'Part 2'")

        # Critical check 2: Mention of star count
        has_star_count = ("50 stars" in output or
                         "49 stars" in output or
                         "50th star" in output)
        self.assertTrue(has_star_count,
                       "Output must mention '50 stars' or '49 stars' or '50th star'")

        # Critical check 3: States this is not computational
        output_lower = output.lower()
        has_not_computational = "not a computational puzzle" in output_lower
        self.assertTrue(has_not_computational,
                       "Output must state 'not a computational puzzle'")

    def test_1_3_output_important_elements(self):
        """Test 1.3: Verify output contains important elements"""
        output = self.capture_stdout(solve_part2)
        output_lower = output.lower()

        # Important check 1: Milestone/completion/congratulations
        has_milestone_words = any(word in output_lower
                                 for word in ["milestone", "completion", "congratulations"])

        # Important check 2: Reference to previous puzzles or requirements
        has_requirements = any(word in output_lower
                              for word in ["previous", "required"])

        has_important = has_milestone_words or has_requirements
        self.assertTrue(has_important,
                       "Output should mention milestone/completion/congratulations "
                       "or reference previous/required puzzles")

    def test_4_1_no_computation_output(self):
        """Test 4.1: Verify no computational results in output"""
        output = self.capture_stdout(solve_part2)

        # Should not contain large numbers (codes are typically > 10000)
        import re
        large_numbers = re.findall(r'\b\d{5,}\b', output)
        self.assertEqual(len(large_numbers), 0,
                        f"Output should not contain large numbers (codes). Found: {large_numbers}")

    def test_6_1_has_docstring(self):
        """Test 6.1: Verify function has documentation"""
        self.assertIsNotNone(solve_part2.__doc__,
                            "Function should have a docstring")

        docstring_lower = solve_part2.__doc__.lower()
        has_explanation = ("milestone" in docstring_lower or
                          "not a computational" in docstring_lower)
        self.assertTrue(has_explanation,
                       "Docstring should explain milestone nature or "
                       "that it's not computational")

    def test_5_1_execution_time(self):
        """Test 5.1: Verify instant execution (O(1) performance)"""
        start = time.time()
        solve_part2()
        end = time.time()

        execution_time = end - start
        self.assertLess(execution_time, 0.1,
                       f"Execution should take < 0.1s. Took {execution_time:.4f}s")


def run_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("Running Day 25 Part 2 Verification Tests")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDay25Part2Verification)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
        print("✓ Solution correctly handles Day 25 Part 2 milestone")
        return True
    else:
        print("✗ SOME TESTS FAILED")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
