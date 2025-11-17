import unittest
from solution import (parse_instruction, initialize_grid,
                      process_instruction, calculate_total_brightness)


class TestLightGrid(unittest.TestCase):

    # Unit Tests: Instruction Parsing
    def test_parse_turn_on(self):
        result = parse_instruction("turn on 0,0 through 999,999")
        self.assertEqual(result, ("turn on", 0, 0, 999, 999))

    def test_parse_turn_off(self):
        result = parse_instruction("turn off 499,499 through 500,500")
        self.assertEqual(result, ("turn off", 499, 499, 500, 500))

    def test_parse_toggle(self):
        result = parse_instruction("toggle 0,0 through 999,0")
        self.assertEqual(result, ("toggle", 0, 0, 999, 0))

    def test_parse_invalid(self):
        result = parse_instruction("invalid instruction format")
        self.assertIsNone(result)

    def test_parse_real_input(self):
        result = parse_instruction("turn on 887,9 through 959,629")
        self.assertEqual(result, ("turn on", 887, 9, 959, 629))

    # Unit Tests: Grid Operations
    def test_grid_initialization(self):
        grid = initialize_grid()
        self.assertEqual(len(grid), 1000)
        self.assertEqual(len(grid[0]), 1000)
        self.assertEqual(grid[0][0], 0)
        self.assertEqual(grid[999][999], 0)

    def test_turn_on_single_light(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(calculate_total_brightness(grid), 1)

    def test_brightness_accumulation(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 3)

    def test_turn_off_with_floor(self):
        grid = initialize_grid()
        grid[0][0] = 2
        process_instruction(grid, "turn off", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 1)
        process_instruction(grid, "turn off", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 0)
        process_instruction(grid, "turn off", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 0)  # Should not go negative

    def test_toggle_operation(self):
        grid = initialize_grid()
        process_instruction(grid, "toggle", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 2)
        process_instruction(grid, "toggle", 0, 0, 0, 0)
        self.assertEqual(grid[0][0], 4)

    def test_rectangular_region(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 2, 2)
        # 3x3 rectangle = 9 lights
        self.assertEqual(calculate_total_brightness(grid), 9)

    def test_asymmetric_region_coordinate_system(self):
        """Critical test to verify X=column, Y=row mapping"""
        grid = initialize_grid()
        # Rectangle from X=0 to X=3 (4 wide), Y=0 to Y=1 (2 tall)
        # Should affect 4 columns × 2 rows = 8 lights
        process_instruction(grid, "turn on", 0, 0, 3, 1)
        self.assertEqual(calculate_total_brightness(grid), 8)
        # Verify specific positions: grid[y][x]
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(grid[0][3], 1)
        self.assertEqual(grid[1][0], 1)
        self.assertEqual(grid[1][3], 1)

    def test_coordinate_system_mapping(self):
        """Verify X,Y coordinate mapping to grid[y][x]"""
        grid = initialize_grid()
        # X=5 (column), Y=3 (row) should map to grid[3][5]
        process_instruction(grid, "turn on", 5, 3, 5, 3)
        self.assertEqual(grid[3][5], 1)
        self.assertEqual(grid[5][3], 0)  # Wrong indexing would set this

    def test_inclusive_boundary(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 5, 5, 5, 5)
        self.assertEqual(grid[5][5], 1)
        self.assertEqual(calculate_total_brightness(grid), 1)

    # Integration Tests: Example Cases
    def test_example_1(self):
        """turn on 0,0 through 0,0 should increase brightness by 1"""
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        self.assertEqual(calculate_total_brightness(grid), 1)

    def test_example_2(self):
        """toggle 0,0 through 999,999 should increase brightness by 2,000,000"""
        grid = initialize_grid()
        process_instruction(grid, "toggle", 0, 0, 999, 999)
        self.assertEqual(calculate_total_brightness(grid), 2_000_000)

    def test_sequential_operations(self):
        """Test overlapping regions interact correctly"""
        grid = initialize_grid()

        # Step 1: turn on 0,0 through 2,2 (3×3 = 9 lights at brightness 1)
        process_instruction(grid, "turn on", 0, 0, 2, 2)
        self.assertEqual(calculate_total_brightness(grid), 9)

        # Step 2: toggle 1,1 through 3,3
        process_instruction(grid, "toggle", 1, 1, 3, 3)
        # Overlapping (1,1) to (2,2): 4 lights go from 1→3
        # New region: 5 lights go from 0→2
        # Non-overlapping from step 1: 5 lights stay at 1
        # Total: 4*3 + 5*2 + 5*1 = 12 + 10 + 5 = 27
        self.assertEqual(calculate_total_brightness(grid), 27)

        # Step 3: turn off 0,0 through 1,1
        process_instruction(grid, "turn off", 0, 0, 1, 1)
        # Total decrease: (0,0)→1, (0,1)→1, (1,0)→1, (1,1)→1 = 4
        self.assertEqual(calculate_total_brightness(grid), 23)

    def test_complex_sequence(self):
        """Test combination of all operations"""
        grid = initialize_grid()

        # Step 1: turn on 0,0 through 99,99 (10,000 lights)
        process_instruction(grid, "turn on", 0, 0, 99, 99)
        self.assertEqual(calculate_total_brightness(grid), 10_000)

        # Step 2: toggle 50,50 through 149,149
        process_instruction(grid, "toggle", 50, 50, 149, 149)
        # Overlapping: 50×50 = 2,500 lights go from 1→3 (adds 5,000)
        # New region: 7,500 lights go from 0→2 (adds 15,000)
        # Subtotal: 10,000 + 5,000 + 15,000 = 30,000
        self.assertEqual(calculate_total_brightness(grid), 30_000)

        # Step 3: turn off 75,75 through 124,124
        process_instruction(grid, "turn off", 75, 75, 124, 124)
        # Decrease: 2,500
        self.assertEqual(calculate_total_brightness(grid), 27_500)

    # Edge Case Tests
    def test_full_grid_turn_on(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 999, 999)
        self.assertEqual(calculate_total_brightness(grid), 1_000_000)

    def test_multiple_operations_same_cell(self):
        grid = initialize_grid()
        # Turn on 5 times
        for _ in range(5):
            process_instruction(grid, "turn on", 500, 500, 500, 500)
        self.assertEqual(grid[500][500], 5)

        # Toggle 3 times (add 6)
        for _ in range(3):
            process_instruction(grid, "toggle", 500, 500, 500, 500)
        self.assertEqual(grid[500][500], 11)

        # Turn off 20 times (should floor at 0)
        for _ in range(20):
            process_instruction(grid, "turn off", 500, 500, 500, 500)
        self.assertEqual(grid[500][500], 0)

    def test_corner_coordinates(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 0, 0)
        process_instruction(grid, "turn on", 999, 999, 999, 999)
        process_instruction(grid, "turn on", 999, 0, 999, 0)
        process_instruction(grid, "turn on", 0, 999, 0, 999)
        self.assertEqual(calculate_total_brightness(grid), 4)

    def test_maximum_coordinate_boundary(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 998, 998, 999, 999)
        # 2×2 rectangle
        self.assertEqual(calculate_total_brightness(grid), 4)
        self.assertEqual(grid[998][998], 1)
        self.assertEqual(grid[999][999], 1)

    def test_single_row(self):
        grid = initialize_grid()
        process_instruction(grid, "turn on", 0, 0, 999, 0)
        self.assertEqual(calculate_total_brightness(grid), 1_000)

    def test_order_dependency(self):
        # Sequence A: turn on then off
        grid_a = initialize_grid()
        process_instruction(grid_a, "turn on", 0, 0, 10, 10)
        process_instruction(grid_a, "turn off", 0, 0, 10, 10)
        total_a = calculate_total_brightness(grid_a)

        # Sequence B: turn off then on
        grid_b = initialize_grid()
        process_instruction(grid_b, "turn off", 0, 0, 10, 10)
        process_instruction(grid_b, "turn on", 0, 0, 10, 10)
        total_b = calculate_total_brightness(grid_b)

        # A should be 0, B should be 121
        self.assertEqual(total_a, 0)
        self.assertEqual(total_b, 121)


if __name__ == '__main__':
    unittest.main()
