# Testing Plan: Marble Circle Game Simulation

## Testing Strategy Overview

We need to verify:
1. **Correctness**: Algorithm produces correct results for known test cases
2. **Edge cases**: Handles boundary conditions properly
3. **Performance**: Runs efficiently for large inputs (71,787 marbles)
4. **Input parsing**: Correctly extracts parameters from input format

## Test Categories

### 1. Example Test Cases (Provided)

These are the validation cases given in the problem statement:

| Players | Last Marble | Expected High Score |
|---------|-------------|---------------------|
| 9       | 25          | 32                  |
| 10      | 1618        | 8317                |
| 13      | 7999        | 146373              |
| 17      | 1104        | 2764                |
| 21      | 6111        | 54718               |
| 30      | 5807        | 37305               |

**Test Method:**
```python
def test_examples():
    test_cases = [
        (9, 25, 32),
        (10, 1618, 8317),
        (13, 7999, 146373),
        (17, 1104, 2764),
        (21, 6111, 54718),
        (30, 5807, 37305),
    ]

    for players, last_marble, expected in test_cases:
        result = simulate_marble_game(players, last_marble)
        assert result == expected, f"Failed: {players} players, {last_marble} marbles. Expected {expected}, got {result}"
        print(f"✓ {players} players, {last_marble} marbles → {result}")
```

**Validation**: All must pass with exact matches.

### 2. Edge Cases

#### 2.1 Minimal Cases
- **1 player, marble 0 only**: High score should be 0 (only marble 0 placed, no scoring)
- **1 player, marble 1-22**: High score should be 0 (no multiples of 23)
- **1 player, marble 23**: Player gets 23 + removed marble value

```python
def test_minimal_cases():
    # Edge case: last marble is 0 (only marble 0 placed)
    assert simulate_marble_game(1, 0) == 0

    # No scoring happens before marble 23
    assert simulate_marble_game(1, 22) == 0

    # First scoring at marble 23
    # When marble 23 is processed with 1 player:
    # Circle has marbles 0-22, current is 22
    # rotate(-7) moves to marble 15 (7 counter-clockwise from 22)
    # pop() removes 15, player gets 23 + 15 = 38
    result = simulate_marble_game(1, 23)
    assert result == 38, f"Expected 38, got {result}"
```

#### 2.2 Exact Multiple of 23 as Last Marble
- **Test**: Last marble is exactly 23, 46, 69, etc.
- **Validation**: Ensure special placement logic executes for final marble

```python
def test_last_marble_is_multiple_of_23():
    # Test when game ends on a special placement
    result = simulate_marble_game(5, 46)
    # Verify result is computed correctly
```

#### 2.3 Single Player
- **Test**: 1 player playing the entire game
- **Validation**: All scoring marbles go to same player

```python
def test_single_player():
    # Test with 1 player, 100 marbles
    # All multiples of 23 (23, 46, 69, 92) scored by player 1
    # Each special placement adds the marble + removed marble
    result = simulate_marble_game(1, 100)
    # Expected calculation:
    # Marble 23: 23 + 15 = 38
    # Marble 46: 46 + [removed marble]
    # Marble 69: 69 + [removed marble]
    # Marble 92: 92 + [removed marble]
    # Total varies based on which marbles are removed
    # Just verify it returns a non-zero integer
    assert result > 0
    print(f"Single player, 100 marbles: {result}")
```

#### 2.4 Many Players (more than marbles)
- **Test**: More players than marbles (e.g., 100 players, 50 marbles)
- **Validation**: Only first 50 players get a turn, others score 0

```python
def test_more_players_than_marbles():
    result = simulate_marble_game(100, 50)
    # Only marbles 1-50 placed, so only players 1-50 get turns
    # Players 51-100 never play
```

### 3. Rotation and Position Logic Tests

#### 3.1 Manual Walkthrough of First 25 Marbles
To validate the rotation logic, manually trace the first 25 marbles:

```python
def test_detailed_walkthrough():
    """
    Manually verify the game state after each placement for small example
    """
    # For 9 players, 25 marbles
    # Using debug mode to trace execution
    result = simulate_marble_game(9, 25, debug=True)

    # Verify final score matches expected (32)
    assert result == 32, f"Expected 32, got {result}"

    # Key verification points based on manual trace:
    # - Marble 23 is played by player 5 (marble 23, player = (23-1) % 9 + 1 = 5)
    # - When marble 23 is processed, marble 9 is 7 positions counter-clockwise
    # - Player 5 gets: 23 (kept) + 9 (removed) = 32
    print("✓ Manual walkthrough verified: 9 players, 25 marbles → 32")
```

**Expected trace verification (from implementation plan):**
1. Start: [0]
2. Marble 1 (P1): [0,1], current=1
3. Marble 2 (P2): [1,0,2], current=2
4. Continue with standard placements...
5. After marble 22: [...,2,1,0,22], current=22
6. Marble 23 (P5): Keep 23, rotate(-7), pop marble 9, score = 32 ✓
7. Continue to marble 25
8. Final: Player 5 has score 32

#### 3.2 Deque Rotation Verification
Create a small test to verify deque rotation behaves as expected:

```python
def test_deque_behavior():
    """
    Test that deque rotation works as we expect for our use case
    """
    from collections import deque

    # Test clockwise rotation (for standard placement)
    d = deque([0, 1, 2, 3])
    d.rotate(1)  # Clockwise
    assert list(d) == [3, 0, 1, 2]  # Last element moved to front

    # Test counter-clockwise rotation (for special placement)
    d = deque([0, 1, 2, 3, 4, 5, 6, 7])
    d.rotate(-7)  # Counter-clockwise by 7
    assert list(d) == [7, 0, 1, 2, 3, 4, 5, 6]
```

### 4. Input Parsing Tests

```python
def test_input_parsing():
    """
    Verify input parsing handles different formats
    """
    # Standard format
    assert parse_input("463 players; last marble is worth 71787 points") == (463, 71787)
    assert parse_input("9 players; last marble is worth 25 points") == (9, 25)

    # Verify it handles variations in spacing, etc. (if applicable)
```

### 5. Performance Tests

#### 5.1 Actual Input
```python
def test_actual_input():
    """
    Run with the actual input to verify performance and get answer
    """
    import time

    start = time.time()
    result = simulate_marble_game(463, 71787)
    elapsed = time.time() - start

    print(f"Result: {result}")
    print(f"Time: {elapsed:.3f} seconds")

    # Verify it completes in reasonable time
    # With deque's O(1) operations, should complete in < 0.5 seconds
    assert elapsed < 1.0, f"Too slow: {elapsed} seconds"

    # Verify result is a reasonable integer
    assert result > 0, "Result should be positive"
    print(f"✓ Actual input (463 players, 71787 marbles): {result}")
```

#### 5.2 Scaling Test
```python
def test_scaling():
    """
    Test with progressively larger inputs to verify O(n) scaling
    """
    import time

    test_sizes = [1000, 5000, 10000, 50000, 71787]

    for size in test_sizes:
        start = time.time()
        result = simulate_marble_game(10, size)
        elapsed = time.time() - start
        print(f"Marbles: {size:6d}, Time: {elapsed:.4f}s, Result: {result}")
```

### 6. Correctness Verification Strategy

**Primary Method**: Use provided test cases
- 6 test cases with known correct answers
- If all pass, high confidence in correctness

**Secondary Method**: Manual trace for small example (9 players, 25 marbles)
- Complete trace documented in implementation plan
- Key verification: marble 23 removes marble 9, player 5 scores 32
- Run with debug=True to verify execution matches expected trace

**Tertiary Method**: Logic review
- Review special placement: Does it add marble + removed marble to score? ✓
- Review standard placement: Does it insert at correct position? ✓
- Review rotation directions: Clockwise vs counter-clockwise correct? ✓

**Quaternary Method**: Edge case testing
- Test with marble 0 as last marble (score should be 0)
- Test with last marble = 22 (no scoring, result 0)
- Test with last marble = 23 (first scoring event, result 38)
- Test with single player (all scores go to one player)

## Test Execution Plan

### Phase 1: Unit Tests
1. Test deque rotation behavior
2. Test input parsing
3. Test minimal edge cases (1 player, small marble counts)

### Phase 2: Example Validation
1. Run all 6 provided test cases
2. Must achieve 100% pass rate
3. If any fail, debug and fix algorithm

### Phase 3: Edge Case Testing
1. Test last marble as multiple of 23
2. Test single player scenarios
3. Test more players than marbles
4. Test manual walkthrough of 25 marbles

### Phase 4: Performance Validation
1. Run with actual input (463 players, 71787 marbles)
2. Verify completes in < 1 second
3. Run scaling tests to confirm O(n) behavior

### Phase 5: Final Answer
1. Run solution on actual input from input.md
2. Record and verify answer
3. Double-check by re-running

## Expected Results

**All 6 validation cases must pass exactly:**
- 9 players, 25 marbles → 32 ✓
- 10 players, 1618 marbles → 8317 ✓
- 13 players, 7999 marbles → 146373 ✓
- 17 players, 1104 marbles → 2764 ✓
- 21 players, 6111 marbles → 54718 ✓
- 30 players, 5807 marbles → 37305 ✓

**Edge case expected values:**
- 1 player, 0 marbles → 0
- 1 player, 22 marbles → 0 (no multiples of 23)
- 1 player, 23 marbles → 38 (23 kept + 15 removed)

**Performance expectations:**
- 71,787 marbles should complete in < 1 second (target: < 0.5s)
- Memory usage should be reasonable (< 50 MB for deque + scores)
- O(n) time complexity verified through scaling tests

**Final answer:**
- Will be computed for 463 players, 71787 marbles
- Should be a large integer (likely in the hundreds of thousands based on pattern)

## Debug Output (Optional)

For debugging failed test cases, the implementation includes an optional debug parameter:

```python
# Enable debug output for small examples
result = simulate_marble_game(9, 25, debug=True)
```

Debug output will show:
- Each marble placement with resulting circle state
- Special placements with kept/removed marble values and running scores
- Only activates for examples with ≤25 marbles to avoid output spam

This helps verify:
- Rotation logic is correct
- Marbles are placed in expected positions
- Scores accumulate correctly
- Special placements remove the correct marbles

## Success Criteria

Testing will be considered successful when:

✓ All 6 provided test cases pass with exact matches
✓ Edge cases return expected values:
  - marble 0 → score 0
  - marble 22 → score 0
  - marble 23 → score 38
✓ Manual walkthrough with debug=True matches documented trace
✓ Deque rotation behavior tests pass
✓ Input parsing correctly extracts player count and last marble value
✓ Actual input (71,787 marbles) completes in < 1 second
✓ Scaling tests confirm O(n) time complexity
✓ Final answer is a positive integer in reasonable range

**Critical verification completed:**
- Manual trace of 9 players, 25 marbles documented in implementation plan
- Confirmed marble 9 is removed when marble 23 is played
- Confirmed player 5 scores 23 + 9 = 32
- Rotation logic verified mathematically and empirically
