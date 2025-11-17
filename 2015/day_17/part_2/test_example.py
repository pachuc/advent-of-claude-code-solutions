from solution import find_minimum_container_ways

# Test with the example from problem statement
containers = [20, 15, 10, 5, 5]
target = 25
result = find_minimum_container_ways(containers, target)
print(f"Example test: containers = {containers}, target = {target}")
print(f"Result: {result}")
print(f"Expected: 3")
print(f"Test: {'PASS' if result == 3 else 'FAIL'}")
