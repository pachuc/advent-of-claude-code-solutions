from solution import execute_instruction

def test_opcodes():
    """Test all 16 opcodes with known inputs and expected outputs"""

    tests_passed = 0
    tests_total = 0

    # Addition tests
    print("Testing Addition opcodes...")
    registers = [0, 5, 3, 0, 0, 0]
    execute_instruction('addr', 1, 2, 3, registers)
    assert registers[3] == 8, f"addr failed: expected 8, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  addr: PASSED")

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('addi', 1, 10, 2, registers)
    assert registers[2] == 15, f"addi failed: expected 15, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  addi: PASSED")

    # Multiplication tests
    print("\nTesting Multiplication opcodes...")
    registers = [0, 4, 5, 0, 0, 0]
    execute_instruction('mulr', 1, 2, 3, registers)
    assert registers[3] == 20, f"mulr failed: expected 20, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  mulr: PASSED")

    registers = [0, 7, 0, 0, 0, 0]
    execute_instruction('muli', 1, 3, 2, registers)
    assert registers[2] == 21, f"muli failed: expected 21, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  muli: PASSED")

    # Bitwise AND tests
    print("\nTesting Bitwise AND opcodes...")
    registers = [0, 0b1111, 0b1010, 0, 0, 0]
    execute_instruction('banr', 1, 2, 3, registers)
    assert registers[3] == 0b1010, f"banr failed: expected {0b1010}, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  banr: PASSED")

    registers = [0, 123, 0, 0, 0, 0]
    execute_instruction('bani', 1, 456, 2, registers)
    assert registers[2] == 72, f"bani failed: expected 72, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  bani: PASSED")

    # Bitwise OR tests
    print("\nTesting Bitwise OR opcodes...")
    registers = [0, 0b1100, 0b0011, 0, 0, 0]
    execute_instruction('borr', 1, 2, 3, registers)
    assert registers[3] == 0b1111, f"borr failed: expected {0b1111}, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  borr: PASSED")

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('bori', 1, 10, 2, registers)
    assert registers[2] == 15, f"bori failed: expected 15, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  bori: PASSED")

    # Assignment tests
    print("\nTesting Assignment opcodes...")
    registers = [0, 42, 0, 0, 0, 0]
    execute_instruction('setr', 1, 999, 2, registers)
    assert registers[2] == 42, f"setr failed: expected 42, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  setr: PASSED")

    registers = [0, 0, 0, 0, 0, 0]
    execute_instruction('seti', 99, 999, 3, registers)
    assert registers[3] == 99, f"seti failed: expected 99, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  seti: PASSED")

    # Greater-than tests
    print("\nTesting Greater-than opcodes...")
    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('gtir', 10, 1, 2, registers)
    assert registers[2] == 1, f"gtir (10 > 5) failed: expected 1, got {registers[2]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('gtir', 3, 1, 2, registers)
    assert registers[2] == 0, f"gtir (3 > 5) failed: expected 0, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  gtir: PASSED")

    registers = [0, 15, 0, 0, 0, 0]
    execute_instruction('gtri', 1, 10, 2, registers)
    assert registers[2] == 1, f"gtri (15 > 10) failed: expected 1, got {registers[2]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('gtri', 1, 10, 2, registers)
    assert registers[2] == 0, f"gtri (5 > 10) failed: expected 0, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  gtri: PASSED")

    registers = [0, 10, 5, 0, 0, 0]
    execute_instruction('gtrr', 1, 2, 3, registers)
    assert registers[3] == 1, f"gtrr (10 > 5) failed: expected 1, got {registers[3]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 5, 10, 0, 0, 0]
    execute_instruction('gtrr', 1, 2, 3, registers)
    assert registers[3] == 0, f"gtrr (5 > 10) failed: expected 0, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  gtrr: PASSED")

    # Equality tests
    print("\nTesting Equality opcodes...")
    registers = [0, 10, 0, 0, 0, 0]
    execute_instruction('eqir', 10, 1, 2, registers)
    assert registers[2] == 1, f"eqir (10 == 10) failed: expected 1, got {registers[2]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('eqir', 10, 1, 2, registers)
    assert registers[2] == 0, f"eqir (10 == 5) failed: expected 0, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  eqir: PASSED")

    registers = [0, 10, 0, 0, 0, 0]
    execute_instruction('eqri', 1, 10, 2, registers)
    assert registers[2] == 1, f"eqri (10 == 10) failed: expected 1, got {registers[2]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 5, 0, 0, 0, 0]
    execute_instruction('eqri', 1, 10, 2, registers)
    assert registers[2] == 0, f"eqri (5 == 10) failed: expected 0, got {registers[2]}"
    tests_total += 1
    tests_passed += 1
    print("  eqri: PASSED")

    registers = [0, 7, 7, 0, 0, 0]
    execute_instruction('eqrr', 1, 2, 3, registers)
    assert registers[3] == 1, f"eqrr (7 == 7) failed: expected 1, got {registers[3]}"
    tests_total += 1
    tests_passed += 1

    registers = [0, 7, 8, 0, 0, 0]
    execute_instruction('eqrr', 1, 2, 3, registers)
    assert registers[3] == 0, f"eqrr (7 == 8) failed: expected 0, got {registers[3]}"
    tests_total += 1
    tests_passed += 1
    print("  eqrr: PASSED")

    print(f"\n{'='*50}")
    print(f"All {tests_passed}/{tests_total} opcode tests PASSED!")
    print(f"{'='*50}")

if __name__ == "__main__":
    test_opcodes()
