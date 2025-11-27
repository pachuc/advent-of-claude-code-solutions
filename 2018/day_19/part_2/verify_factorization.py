#!/usr/bin/env python3
"""
Verify factorization of 10551389 and manually compute divisors
"""

def find_prime_factors(n):
    """Find prime factorization of n"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def get_all_divisors(prime_factors):
    """Generate all divisors from prime factorization"""
    from itertools import combinations

    # Get unique factors with their counts
    factor_counts = {}
    for f in prime_factors:
        factor_counts[f] = factor_counts.get(f, 0) + 1

    # Generate all divisors
    divisors = [1]

    for prime, count in factor_counts.items():
        new_divisors = []
        power = 1
        for _ in range(count):
            power *= prime
            for d in divisors:
                new_divisors.append(d * power)
        divisors.extend(new_divisors)

    return sorted(divisors)


def main():
    n = 10551389

    print("=" * 60)
    print(f"Factorization verification for {n}")
    print("=" * 60)

    # Find prime factors
    factors = find_prime_factors(n)
    print(f"Prime factors: {factors}")

    # Verify factorization
    product = 1
    for f in factors:
        product *= f
    print(f"Product of factors: {product}")
    print(f"Matches original: {product == n}")

    # Get all divisors
    divisors = get_all_divisors(factors)
    print(f"\nAll divisors: {divisors}")
    print(f"Number of divisors: {len(divisors)}")

    # Compute sum
    divisor_sum = sum(divisors)
    print(f"\nSum of divisors: {divisor_sum}")

    # Verify against our function
    from solution import sum_of_divisors
    computed = sum_of_divisors(n)
    print(f"Computed by algorithm: {computed}")
    print(f"Match: {divisor_sum == computed}")

    print("\n" + "=" * 60)
    print(f"Final answer: {divisor_sum}")
    print("=" * 60)


if __name__ == '__main__':
    main()
