from solution import sum_of_divisors

result = 786240

# Find all divisors
def get_all_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

divisors = get_all_divisors(result)
divisor_sum = sum_of_divisors(result)

print(f"House {result} analysis:")
print(f"  Number of divisors: {len(divisors)}")
print(f"  Sum of divisors: {divisor_sum}")
print(f"  Presents received: {divisor_sum * 10}")
print()
print(f"  First 20 divisors: {divisors[:20]}")
print(f"  Last 20 divisors: {divisors[-20:]}")
print()

# Check if it's highly composite
print(f"  Factorization of {result}:")
n = result
factors = []
d = 2
temp = n
while d * d <= temp:
    while temp % d == 0:
        factors.append(d)
        temp //= d
    d += 1
if temp > 1:
    factors.append(temp)
print(f"    {result} = {' × '.join(map(str, factors))}")
