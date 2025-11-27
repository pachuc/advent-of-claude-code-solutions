from solution import *

# Test Phase 1: Parsing Validation
print("=== Phase 1: Parsing Validation ===")
samples, test_program = parse_input("input.md")
print(f"Number of samples: {len(samples)}")
print(f"Number of test program instructions: {len(test_program)}")
print(f"Sample structure valid: {all(len(s) == 3 for s in samples)}")
print(f"Test program structure valid: {all(len(inst) == 4 for inst in test_program)}")
print()

# Test Phase 2: Opcode Compatibility (using example from problem)
print("=== Phase 2: Opcode Compatibility Test ===")
before = [3, 2, 1, 1]
instruction = [9, 2, 1, 2]
after = [3, 2, 2, 1]
compatible = get_compatible_opcodes(before, instruction, after)
print(f"Compatible opcodes for example: {compatible}")
print(f"Expected: {{'mulr', 'addi', 'seti'}}")
print(f"Match: {compatible == {'mulr', 'addi', 'seti'}}")
print()

# Test Phase 3: Build Possibilities
print("=== Phase 3: Build Opcode Possibilities ===")
possibilities = build_opcode_possibilities(samples)
print(f"All 16 opcode numbers present: {len(possibilities) == 16}")
print(f"All possibility sets non-empty: {all(len(v) > 0 for v in possibilities.values())}")
print()
print("Possibility counts per opcode number:")
for opcode_num in sorted(possibilities.keys()):
    print(f"  Opcode {opcode_num:2d}: {len(possibilities[opcode_num]):2d} possibilities")
print()

# Test Phase 4: Deduce Mapping
print("=== Phase 4: Deduce Opcode Mapping ===")
opcode_map = deduce_opcode_mapping(possibilities)
print(f"All 16 opcode numbers mapped: {len(opcode_map) == 16}")
print(f"All values unique: {len(set(opcode_map.values())) == 16}")
print(f"All values are valid opcodes: {set(opcode_map.values()) == set(ALL_OPCODES)}")
print()
print("Deduced opcode mapping:")
for opcode_num in sorted(opcode_map.keys()):
    print(f"  Opcode {opcode_num:2d} -> {opcode_map[opcode_num]}")
print()

# Test Phase 5: Execute Program
print("=== Phase 5: Execute Test Program ===")
result = execute_program(test_program, opcode_map)
print(f"Final value in register 0: {result}")
print()

# Test Phase 6: Full Integration
print("=== Phase 6: Full Integration Test ===")
result1 = solve("input.md")
result2 = solve("input.md")
print(f"First run result: {result1}")
print(f"Second run result: {result2}")
print(f"Results are consistent: {result1 == result2}")
