from solution import execute_opcode, count_matching_opcodes, ALL_OPCODES

# Test the example from problem.md
before = [3, 2, 1, 1]
instruction = [9, 2, 1, 2]  # opcode=9, A=2, B=1, C=2
after = [3, 2, 2, 1]

print("Testing example from problem.md:")
print(f"Before:  {before}")
print(f"Instruction: {instruction}")
print(f"After:   {after}")
print()

# Check which opcodes match
_, A, B, C = instruction
matching_opcodes = []
for opcode_name in ALL_OPCODES:
    result = execute_opcode(opcode_name, before, A, B, C)
    if result == after:
        matching_opcodes.append(opcode_name)
        print(f"✓ {opcode_name}: {before} -> {result}")

print()
count = count_matching_opcodes(before, instruction, after)
print(f"Total matching opcodes: {count}")
print(f"Matching opcodes: {matching_opcodes}")
print()

# Expected: mulr, addi, seti (3 opcodes)
expected_opcodes = ['mulr', 'addi', 'seti']
print(f"Expected opcodes: {expected_opcodes}")
print(f"Test passed: {count == 3 and set(matching_opcodes) == set(expected_opcodes)}")
