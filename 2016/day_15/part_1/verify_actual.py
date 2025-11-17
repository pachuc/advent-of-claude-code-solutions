"""Manual verification of the actual input solution"""

T = 203660

# Disc #1 has 13 positions; at time=0, it is at position 10.
disc1_arrival = T + 1  # 203661
disc1_position = (10 + disc1_arrival) % 13
print(f"Disc 1 at time {disc1_arrival}: (10 + {disc1_arrival}) % 13 = {disc1_position}")

# Disc #2 has 17 positions; at time=0, it is at position 15.
disc2_arrival = T + 2  # 203662
disc2_position = (15 + disc2_arrival) % 17
print(f"Disc 2 at time {disc2_arrival}: (15 + {disc2_arrival}) % 17 = {disc2_position}")

# Disc #3 has 19 positions; at time=0, it is at position 17.
disc3_arrival = T + 3  # 203663
disc3_position = (17 + disc3_arrival) % 19
print(f"Disc 3 at time {disc3_arrival}: (17 + {disc3_arrival}) % 19 = {disc3_position}")

# Disc #4 has 7 positions; at time=0, it is at position 1.
disc4_arrival = T + 4  # 203664
disc4_position = (1 + disc4_arrival) % 7
print(f"Disc 4 at time {disc4_arrival}: (1 + {disc4_arrival}) % 7 = {disc4_position}")

# Disc #5 has 5 positions; at time=0, it is at position 0.
disc5_arrival = T + 5  # 203665
disc5_position = (0 + disc5_arrival) % 5
print(f"Disc 5 at time {disc5_arrival}: (0 + {disc5_arrival}) % 5 = {disc5_position}")

# Disc #6 has 3 positions; at time=0, it is at position 1.
disc6_arrival = T + 6  # 203666
disc6_position = (1 + disc6_arrival) % 3
print(f"Disc 6 at time {disc6_arrival}: (1 + {disc6_arrival}) % 3 = {disc6_position}")

print()
all_zero = all([
    disc1_position == 0,
    disc2_position == 0,
    disc3_position == 0,
    disc4_position == 0,
    disc5_position == 0,
    disc6_position == 0
])

if all_zero:
    print("✓ All discs are at position 0 when the capsule arrives!")
else:
    print("✗ Some discs are not at position 0")
