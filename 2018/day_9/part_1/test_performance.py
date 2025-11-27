from solution import simulate_marble_game
import time

print("Performance test:")
start = time.time()
result = simulate_marble_game(463, 71787)
elapsed = time.time() - start

print(f"Result: {result}")
print(f"Time: {elapsed:.4f} seconds")

if elapsed < 1.0:
    print(f"✓ Performance acceptable (< 1.0 second)")
else:
    print(f"✗ Performance issue: {elapsed:.4f} seconds (target: < 1.0 second)")
