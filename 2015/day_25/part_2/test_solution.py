import unittest
import io
import sys
from solution import solve_part2


class TestDay25Part2(unittest.TestCase):
    """Test suite for Day 25 Part 2 - Milestone Acknowledgment"""

    def capture_stdout(self, func):
        """Helper to capture stdout from a function"""
        captured = io.StringIO()
        sys.stdout = captured
        func()
        sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_returns_value(self):
        """Test 2.1: Verify function returns a value"""
        result = solve_part2()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_return_value_content(self):
        """Test 2.2: Verify return value indicates milestone"""
        result = solve_part2()
        keywords = ["50th", "Star", "Completion", "Milestone", "Complete"]
        self.assertTrue(any(kw in result for kw in keywords))

    def test_output_contains_key_phrases(self):
        """Test 1.3: Verify output contains key milestone phrases"""
        output = self.capture_stdout(solve_part2)

        # Critical checks - ALL must pass
        critical_checks = [
            "Day 25 Part 2" in output or "Part 2" in output,
            "50 stars" in output or "49 stars" in output or "50th star" in output,
            "not a computational puzzle" in output.lower()
        ]

        # Important checks - at least one must pass
        important_checks = [
            any(word in output.lower() for word in ["milestone", "completion", "congratulations"]),
            any(word in output.lower() for word in ["previous", "required"])
        ]

        self.assertTrue(all(critical_checks),
                       f"Output missing critical elements: {critical_checks}")
        self.assertTrue(any(important_checks),
                       f"Output missing important elements: {important_checks}")

    def test_no_computation_output(self):
        """Test 4.1: Verify no computational results in output"""
        output = self.capture_stdout(solve_part2)

        # Should not contain large numbers (codes are typically > 10000)
        import re
        large_numbers = re.findall(r'\b\d{5,}\b', output)
        self.assertEqual(len(large_numbers), 0,
                        f"Output contains suspicious numbers: {large_numbers}")

    def test_execution_completes(self):
        """Test 1.1: Verify function executes without errors"""
        try:
            solve_part2()
        except Exception as e:
            self.fail(f"solve_part2() raised an exception: {e}")

    def test_has_docstring(self):
        """Test 6.1: Verify function has documentation"""
        self.assertIsNotNone(solve_part2.__doc__)
        docstring_lower = solve_part2.__doc__.lower()
        self.assertTrue(
            "milestone" in docstring_lower or
            "not a computational" in docstring_lower,
            "Docstring doesn't explain milestone nature"
        )


if __name__ == '__main__':
    unittest.main()
