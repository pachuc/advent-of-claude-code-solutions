from solution import parse_input, verify_delay

# Parse actual input
layers = parse_input('input.md')
print(f"Total layers: {len(layers)}")
print(f"First layer: {layers[0]}")
print(f"Last layer: {layers[-1]}")

answer = 3907994

print(f"\nVerifying answer {answer}...")
print(f"delay={answer} works: {verify_delay(layers, answer)}")
print(f"delay={answer-1} works: {verify_delay(layers, answer-1)}")

# Show which layer catches at answer-1
if not verify_delay(layers, answer-1):
    print(f"\nLayers that catch at delay={answer-1}:")
    from solution import is_caught
    for depth, range_val in layers:
        if is_caught(depth, range_val, answer-1):
            period = 2 * (range_val - 1)
            time = answer - 1 + depth
            print(f"  Layer {depth}: range={range_val}, period={period}, time={time}, {time}%{period}={time%period}")

# Verify all layers are safe at answer
print(f"\nVerifying all layers are safe at delay={answer}:")
all_safe = True
for depth, range_val in layers:
    from solution import is_caught
    if is_caught(depth, range_val, answer):
        print(f"  ERROR: Layer {depth} catches at delay {answer}")
        all_safe = False

if all_safe:
    print("  All layers are safe!")
