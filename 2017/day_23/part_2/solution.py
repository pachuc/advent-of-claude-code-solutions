def is_composite(n):
    """
    Check if n is composite (not prime).

    A composite number has factors other than 1 and itself.
    - 0 and 1 are considered composite (not prime by definition)
    - 2 is the only even prime
    - All other even numbers are composite
    - For odd numbers, check divisibility by odd numbers up to sqrt(n)
    """
    if n < 2:
        return True
    if n == 2:
        return False
    if n % 2 == 0:
        return True

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return True
        i += 2

    return False


def count_composites(start, end, step):
    """
    Count composite numbers in range [start, end] with given step size.

    Args:
        start: First value to check
        end: Last value to check (inclusive)
        step: Increment between values

    Returns:
        Number of composite values in the range
    """
    count = 0
    current = start
    while current <= end:
        if is_composite(current):
            count += 1
        current += step
    return count


def main():
    """
    Solve Part 2: Count composites when a=1.

    From analyzing the assembly code:
    - When a=1, initialization sets b=106700, c=123700
    - The program checks numbers from b to c (inclusive) stepping by 17
    - It counts how many are composite (non-prime)
    - The count is stored in register h
    """
    # Parameters extracted from assembly analysis
    b = 106700  # Starting value (from lines 1-6 with a=1)
    c = 123700  # Ending value (from lines 7-8 with a=1)
    step = 17   # Step size (from line 31: sub b -17)

    # Count composite numbers in the range
    result = count_composites(b, c, step)

    # Output the result
    print(result)


if __name__ == "__main__":
    main()
