# Test Plan: Santa and Robo-Santa Gift Delivery

## Testing Strategy
Verify the solution works correctly by testing against provided examples, edge cases, and the actual input.

## Test Categories

### 1. Example Test Cases (from problem statement)

#### Test 1.1: `^v`
- **Input**: `^v`
- **Expected Output**: 3
- **Reasoning**:
  - Start: Both at (0,0) - 1 house
  - Santa moves north: (0,1) - 1 new house
  - Robo-Santa moves south: (0,-1) - 1 new house
  - Total: 3 unique houses
- **Purpose**: Basic alternating movement in opposite directions

#### Test 1.2: `^>v<`
- **Input**: `^>v<`
- **Expected Output**: 3
- **Reasoning**:
  - Start: Both at (0,0)
  - Santa: (0,0) → (0,1) → (0,0)
  - Robo-Santa: (0,0) → (1,0) → (0,0)
  - Unique houses: (0,0), (0,1), (1,0)
- **Purpose**: Both returning to origin, tests duplicate handling

#### Test 1.3: `^v^v^v^v^v`
- **Input**: `^v^v^v^v^v`
- **Expected Output**: 11
- **Reasoning**:
  - Santa moves north 5 times: (0,0), (0,1), (0,2), (0,3), (0,4), (0,5)
  - Robo-Santa moves south 5 times: (0,0), (0,-1), (0,-2), (0,-3), (0,-4)
  - Starting position (0,0) counted once
  - Total: 11 unique houses
- **Purpose**: Repeated movements in opposite directions

### 2. Edge Case Tests

#### Test 2.1: Empty String
- **Input**: `""`
- **Expected Output**: 1
- **Reasoning**: Only the starting house (0,0) is visited
- **Purpose**: Minimal input case

#### Test 2.2: Single Character (Santa only)
- **Input**: `^`
- **Expected Output**: 2
- **Reasoning**:
  - Start: (0,0)
  - Santa moves: (0,1)
  - Robo-Santa doesn't move (no odd index)
- **Purpose**: Odd number of moves (only Santa moves)

#### Test 2.3: All Same Direction
- **Input**: `>>>>`
- **Expected Output**: 3
- **Reasoning**:
  - Start: (0,0) - visited by both
  - Index 0 (Santa): > → (1,0)
  - Index 1 (Robo-Santa): > → (1,0) [already visited]
  - Index 2 (Santa): > → (2,0)
  - Index 3 (Robo-Santa): > → (2,0) [already visited]
  - Unique: (0,0), (1,0), (2,0) = 3 houses
- **Purpose**: Parallel movement in same direction, both follow identical path

#### Test 2.4: Complex Revisiting Pattern
- **Input**: `>v<^>v<^`
- **Expected Output**: 4
- **Reasoning**:
  - Index 0 (Santa): > → (0,0) to (1,0)
  - Index 1 (Robo-Santa): v → (0,0) to (0,-1)
  - Index 2 (Santa): < → (1,0) to (0,0) [already visited]
  - Index 3 (Robo-Santa): ^ → (0,-1) to (0,1)
  - Index 4 (Santa): > → (0,0) to (1,0) [already visited]
  - Index 5 (Robo-Santa): v → (0,1) to (0,0) [already visited]
  - Index 6 (Santa): < → (1,0) to (0,0) [already visited]
  - Index 7 (Robo-Santa): ^ → (0,0) to (0,1) [already visited]
  - Unique houses: {(0,0), (1,0), (0,-1), (0,1)} = 4 houses
- **Purpose**: Circular patterns with extensive revisiting

#### Test 2.5: Diverging Paths
- **Input**: `><><`
- **Expected Output**: 5
- **Reasoning**:
  - Start: (0,0)
  - Index 0 (Santa): > → (0,0) to (1,0)
  - Index 1 (Robo-Santa): < → (0,0) to (-1,0)
  - Index 2 (Santa): > → (1,0) to (2,0)
  - Index 3 (Robo-Santa): < → (-1,0) to (-2,0)
  - Unique: (0,0), (1,0), (-1,0), (2,0), (-2,0) = 5 houses
- **Purpose**: Testing diverging paths in opposite directions

#### Test 2.6: Long Straight Line (Performance Test)
- **Input**: `^` * 1000 (1000 north movements)
- **Expected Output**: 501
- **Reasoning**:
  - Santa moves north 500 times: (0,0) → (0,1) → ... → (0,500)
  - Robo-Santa moves north 500 times: (0,0) → (0,1) → ... → (0,500)
  - Both follow identical path
  - Unique: 501 positions from (0,0) to (0,500)
- **Purpose**: Verify performance with long input and test identical path deduplication

### 3. Actual Input Test

#### Test 3.1: Full Input File
- **Input**: Content from `input.md`
- **Expected Output**: To be calculated by solution
- **Method**:
  1. Run the solution on actual input
  2. Verify output is a reasonable number with the following bounds:
     - Minimum: ceil(len(input)/2) + 1 (both follow similar paths)
     - Maximum: len(input) + 1 (all positions unique)
  3. Check that the answer is a positive integer
  4. If this is an Advent of Code problem, verify against the platform's expected answer
  5. Document the final answer for future reference
- **Purpose**: Validate against actual problem input

## Testing Execution Plan

### Phase 1: Unit Tests
1. Create a test file `test_solution.py`
2. Implement test functions for each example case
3. Implement test functions for edge cases
4. Use assertions to verify expected outputs
5. Run all tests and ensure they pass

### Phase 2: Manual Verification
1. Pick 2-3 edge cases to manually trace:
   - Empty string test (Test 2.1)
   - Single character test (Test 2.2)
   - One example case (Test 1.1: `^v`)
2. Manually trace through the algorithm step-by-step
3. Verify the positions visited match expectations
4. Confirm set correctly deduplicates positions

### Phase 3: Actual Input
1. Run solution on `input.md`
2. Record the output
3. Verify output is reasonable:
   - Positive integer
   - Between ceil(len(input)/2) + 1 and len(input) + 1 (inclusive)
   - Greater than 1 (at least starting position)
4. Verify against expected answer if available from problem source

### Phase 4: Performance Verification
1. Measure execution time on actual input
2. Should complete in under 1 second for ~8000 character input
3. Verify no memory issues or excessive memory usage

## Verification Checklist

- [ ] All example cases pass
- [ ] Empty string handled correctly
- [ ] Single character handled correctly
- [ ] Same direction movements work
- [ ] Overlapping paths deduplicated correctly
- [ ] Actual input produces a reasonable result
- [ ] Solution runs efficiently (< 1 second)
- [ ] Code is readable and well-commented

## Expected Issues and Mitigations

### Issue 1: Off-by-one errors in indexing
- **Mitigation**: Carefully verify even (0,2,4...) vs odd (1,3,5...) indexing
- **Test**: Example 1.1 should catch this immediately

### Issue 2: Forgetting to add starting position
- **Mitigation**: Initialize visited set with (0,0) before loop
- **Test**: Empty string test should return 1, not 0

### Issue 3: Mutable position in set
- **Mitigation**: Always convert list positions to tuples when adding to set
- **Test**: Any test with revisiting will fail if this is wrong

### Issue 4: Wrong coordinate system
- **Mitigation**: Clearly define x=horizontal, y=vertical, north=+y
- **Test**: Example cases provide clear expected outcomes

## Success Criteria
1. All provided examples produce correct output
2. Edge cases handled gracefully
3. Actual input produces a valid result
4. Code runs efficiently on large input
5. Solution is clear and maintainable
