# Implementation Plan - Day 19 Part 2

## Problem Analysis

Part 2 modifies Part 1 by initializing register 0 to 1 instead of 0. This seemingly small change causes the program to follow a different code path during initialization, which builds a much larger target number in register 4.

### Key Insight: What the Program Computes (VERIFIED)

**Algorithm Verification Performed:**
Using Part 1's known answer (1056), we have confirmed that the program computes the **sum of all divisors** of a number N stored in register 4:
- Part 1: r4 = 989, sum_of_divisors(989) = 1056 ✓
- Part 2: r4 = 10551389 (much larger!)

**Assembly Structure (from input.md):**
1. **Line 0**: Jump to initialization (`addi 3 16 3` jumps to line 17, since IP register is 3)
2. **Lines 2-16**: Nested loops implementing divisor checking and summation
3. **Lines 18-27**: Base initialization (builds initial value in register 4)
4. **Lines 28-36**: Extended initialization when r0=1 (significantly increases register 4)
5. **Line 1, then line 37**: Entry to main loop after initialization completes

**Main Algorithm (lines 2-16):**
- Outer loop: r5 iterates from 1 to N (register 4)
- Inner loop: r2 iterates from 1 to N (register 4)
- Check if r5 * r2 == N (lines 4-5: `mulr 5 2 1; eqrr 1 4 1`)
- If yes, add r5 to register 0 (line 8: `addr 5 0 0`)
- This effectively finds all divisors of N and sums them

**Performance Issue:**
- For Part 1 (r0=0), register 4 = 989 (small enough for direct simulation)
- For Part 2 (r0=1), register 4 = 10551389 (would require ~10^14 operations)
- Direct simulation would require O(N²) operations - impractical for large N

## Implementation Strategy

### Chosen Approach: Run Initialization, Then Optimize

This hybrid approach balances correctness (by using actual initialization) with efficiency (by optimizing the main computation).

**Step 1: Verify Algorithm Using Part 1 (CRITICAL)**
Before implementing Part 2, validate our understanding:
1. Run Part 1 initialization with r0=0
2. Extract target value from register 4 when stable
3. Compute sum_of_divisors(target)
4. Verify it equals 1056 (Part 1's known answer)
5. Only proceed if verification passes

**Step 2: Extract Target Number N for Part 2**
1. Reuse Part 1's CPU simulator code
2. Modify initial state: `registers[0] = 1`
3. Run the program with iteration limit (~100 iterations sufficient based on analysis)
4. Detect when register 4 stabilizes:
   - Track when r4 stops changing
   - Wait for 10 consecutive iterations with stable r4
   - Verify r4 > 0 before accepting
5. When stable, capture the value in register 4 (this is N)
6. Exit simulation early

**Step 3: Compute Sum of Divisors Efficiently**
1. Implement efficient divisor summation algorithm
2. Only iterate from 1 to sqrt(N) to find divisor pairs
3. For each i where N % i == 0:
   - Add i to sum
   - If i != N/i, also add N/i to sum (avoiding double-count for perfect squares)
4. Return the sum as the final answer

**Time Complexity:** O(sqrt(N)) instead of O(N²)
- For N = 10,551,389: sqrt(N) ≈ 3,248 iterations instead of 111 billion iterations

## Detailed Implementation Steps

### Step 1: Code Setup
- Copy `part_1_solution.py` as base
- Keep all opcode functions and parsing logic unchanged
- Add new functions for target extraction and divisor sum computation

### Step 2: Implement Target Extraction Function
```python
def extract_target_number(ip_register, instructions, initial_r0):
    """
    Run initialization until register 4 stabilizes, then return its value.

    Returns: (target_number, iterations_used)
    """
    registers = [initial_r0, 0, 0, 0, 0, 0]
    ip = 0
    opcode_functions = create_opcode_functions()

    # Track r4 stability
    r4_stable_count = 0
    last_r4 = 0
    max_iterations = 1000  # Generous limit

    for iteration in range(max_iterations):
        # Check halt condition
        if ip < 0 or ip >= len(instructions):
            raise RuntimeError(f"Program halted during initialization at IP={ip}")

        # Execute one instruction
        registers[ip_register] = ip
        opcode, A, B, C = instructions[ip]
        opcode_functions[opcode](registers, A, B, C)
        ip = registers[ip_register] + 1

        # Check if r4 changed
        if registers[4] != last_r4:
            last_r4 = registers[4]
            r4_stable_count = 0
        else:
            r4_stable_count += 1

        # If r4 stable for 10 iterations and positive, we're done
        if r4_stable_count >= 10 and registers[4] > 0:
            return registers[4], iteration

    raise RuntimeError(f"Register 4 did not stabilize within {max_iterations} iterations")
```

### Step 3: Implement Efficient Divisor Sum
```python
def sum_of_divisors(n):
    """
    Compute sum of all divisors of n (including 1 and n)
    Time complexity: O(sqrt(n))

    Algorithm:
    - Iterate from 1 to sqrt(n)
    - For each i that divides n, add both i and n/i to the sum
    - Handle perfect squares carefully to avoid double-counting
    """
    if n <= 0:
        return 0

    divisor_sum = 0
    i = 1

    # Iterate up to sqrt(n)
    while i * i <= n:
        if n % i == 0:
            divisor_sum += i  # Add the smaller divisor
            # Add the paired divisor if it's different (avoid double-count for perfect squares)
            if i != n // i:
                divisor_sum += n // i
        i += 1

    return divisor_sum
```

### Step 4: Add Algorithm Verification Function
```python
def verify_algorithm_with_part1(ip_register, instructions):
    """
    Verify our algorithm interpretation using Part 1's known answer.
    Returns True if verification passes, False otherwise.
    """
    # Extract target for Part 1 (r0=0)
    target_part1, _ = extract_target_number(ip_register, instructions, initial_r0=0)

    # Compute sum of divisors
    result = sum_of_divisors(target_part1)

    # Should equal 1056 (Part 1's known answer)
    if result == 1056:
        print(f"Algorithm verified: sum_of_divisors({target_part1}) = {result} ✓")
        return True
    else:
        print(f"Algorithm verification FAILED: sum_of_divisors({target_part1}) = {result}, expected 1056")
        return False
```

### Step 5: Main Program Flow
```python
def main():
    # Read and parse input
    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    # CRITICAL: Verify algorithm using Part 1 first
    if not verify_algorithm_with_part1(ip_register, instructions):
        raise RuntimeError("Algorithm verification failed - aborting")

    # Extract target number for Part 2 (r0=1)
    target_number, iterations = extract_target_number(
        ip_register, instructions, initial_r0=1
    )

    print(f"Extracted target: {target_number} (after {iterations} iterations)")

    # Compute answer efficiently
    result = sum_of_divisors(target_number)

    print(result)
```

## Algorithm Complexity Analysis

### Part 1 Approach (Direct Simulation)
- **Time Complexity:** O(I) where I is number of instructions executed
- For Part 1 with small N: I ≈ O(N²) but N is small (~1000)
- **Works fine for Part 1**

### Part 2 Naive Simulation
- **Time Complexity:** O(N²) where N is the target number in register 4
- For Part 2, N could be 10,000,000+ → 10^14 operations
- **Impractical: Would take hours/days**

### Part 2 Optimized Approach
- **Time Complexity:** O(sqrt(N))
- For N = 10,000,000 → ~3162 iterations
- **Practical: Milliseconds**

## Edge Cases to Consider

1. **Algorithm Verification Failure:** Our interpretation could be wrong
   - Mitigation: **Verify with Part 1 first** before proceeding to Part 2
   - If verification fails, fall back to direct simulation or re-analyze assembly

2. **Target Number Extraction Fails:** If initialization takes more iterations than expected
   - Mitigation: Use generous iteration limit (1000 iterations)
   - Add detailed error message showing current state if timeout occurs

3. **Register 4 Never Stabilizes:** Program behavior differs from analysis
   - Mitigation: Track r4 changes and detect stability (10 consecutive unchanged iterations)
   - If not stable after 1000 iterations, raise clear error for investigation

4. **Perfect Square Handling:** Common bug in divisor enumeration
   - For n = k², ensure sqrt(n) is only counted once
   - Mitigation: Check `if i != n // i` before adding paired divisor
   - Test with perfect squares: 16, 25, 100, etc.

5. **Integer Overflow:** Python handles big integers natively, not a concern
   - But validate target is reasonable (positive, less than 10^10)

## Testing Strategy

See `test_plan.md` for comprehensive testing approach.

## Summary

The implementation will:
1. **Verify algorithm** using Part 1's known answer (sum_of_divisors(989) should equal 1056)
2. **Reuse** Part 1's CPU simulator infrastructure (opcodes, parsing, execution)
3. **Extract target** by running initialization with r0=1 until register 4 stabilizes
4. **Compute efficiently** using sum_of_divisors with O(sqrt(N)) algorithm
5. **Return result** as the final answer

This approach:
- **Validates correctness** before proceeding (using Part 1 as a test case)
- **Balances accuracy** (by using actual initialization) with **efficiency** (by optimizing computation)
- **Handles edge cases** with stability detection and verification steps
- **Provides clear error messages** if assumptions don't hold

**Expected Result for Part 2:** sum_of_divisors(10551389) = 10915260
