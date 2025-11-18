from solution import spin, exchange, partner

def test_spin():
    """Test spin operation"""
    print("Testing spin operation...")

    # Test basic spin
    programs = list('abcde')
    spin(programs, 1)
    assert programs == list('eabcd'), f"Expected eabcd, got {''.join(programs)}"

    # Test multiple spin
    programs = list('abcde')
    spin(programs, 3)
    assert programs == list('cdeab'), f"Expected cdeab, got {''.join(programs)}"

    # Test spin zero
    programs = list('abcde')
    spin(programs, 0)
    assert programs == list('abcde'), f"Expected abcde, got {''.join(programs)}"

    # Test spin entire list (full rotation)
    programs = list('abcde')
    spin(programs, 5)
    assert programs == list('abcde'), f"Expected abcde, got {''.join(programs)}"

    # Test with 16 programs
    programs = list('abcdefghijklmnop')
    spin(programs, 11)
    assert programs[0] == 'f', f"Expected first element 'f', got {programs[0]}"

    print("  ✓ All spin tests passed")

def test_exchange():
    """Test exchange operation"""
    print("Testing exchange operation...")

    # Test basic exchange
    programs = list('eabcd')
    exchange(programs, 3, 4)
    assert programs == list('eabdc'), f"Expected eabdc, got {''.join(programs)}"

    # Test exchange at boundaries
    programs = list('abcde')
    exchange(programs, 0, 4)
    assert programs == list('ebcda'), f"Expected ebcda, got {''.join(programs)}"

    # Test exchange adjacent positions
    programs = list('abcde')
    exchange(programs, 1, 2)
    assert programs == list('acbde'), f"Expected acbde, got {''.join(programs)}"

    # Test exchange same position
    programs = list('abcde')
    exchange(programs, 2, 2)
    assert programs == list('abcde'), f"Expected abcde, got {''.join(programs)}"

    print("  ✓ All exchange tests passed")

def test_partner():
    """Test partner operation"""
    print("Testing partner operation...")

    # Test basic partner swap
    programs = list('baedc')
    partner(programs, 'e', 'b')
    assert programs == list('eabdc'), f"Expected eabdc, got {''.join(programs)}"

    # Test partner swap at boundaries
    programs = list('abcde')
    partner(programs, 'a', 'e')
    assert programs == list('ebcda'), f"Expected ebcda, got {''.join(programs)}"

    # Test partner swap same program
    programs = list('abcde')
    partner(programs, 'c', 'c')
    assert programs == list('abcde'), f"Expected abcde, got {''.join(programs)}"

    # Test partner after position changes
    programs = list('eadbc')
    partner(programs, 'a', 'd')
    assert programs == list('edabc'), f"Expected edabc, got {''.join(programs)}"

    print("  ✓ All partner tests passed")

def test_example_sequence():
    """Test full example from problem"""
    print("Testing example sequence from problem...")

    programs = list('abcde')

    # Step 1: s1
    spin(programs, 1)
    assert programs == list('eabcd'), f"Step 1: Expected eabcd, got {''.join(programs)}"

    # Step 2: x3/4
    exchange(programs, 3, 4)
    assert programs == list('eabdc'), f"Step 2: Expected eabdc, got {''.join(programs)}"

    # Step 3: pe/b
    partner(programs, 'e', 'b')
    assert programs == list('baedc'), f"Step 3: Expected baedc, got {''.join(programs)}"

    print("  ✓ Example sequence test passed")

def test_multiple_spins():
    """Test spin composition"""
    print("Testing multiple spins...")

    programs = list('abcde')
    spin(programs, 2)  # -> ['d', 'e', 'a', 'b', 'c']
    spin(programs, 2)  # -> ['b', 'c', 'd', 'e', 'a']
    assert programs == list('bcdea'), f"Expected bcdea, got {''.join(programs)}"

    print("  ✓ Multiple spins test passed")

def test_complex_sequence():
    """Test complex sequence with all operation types"""
    print("Testing complex sequence...")

    programs = list('abcdef')
    spin(programs, 2)       # -> ['e', 'f', 'a', 'b', 'c', 'd']
    exchange(programs, 1, 4)  # -> ['e', 'c', 'a', 'b', 'f', 'd']
    partner(programs, 'c', 'f')  # -> ['e', 'f', 'a', 'b', 'c', 'd']
    spin(programs, 1)       # -> ['d', 'e', 'f', 'a', 'b', 'c']
    assert programs == list('defabc'), f"Expected defabc, got {''.join(programs)}"

    print("  ✓ Complex sequence test passed")

def test_input_parsing():
    """Test parsing of actual input file"""
    print("Testing input file parsing...")

    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    moves = input_data.split(',')
    moves = [m for m in moves if m]  # Filter empty strings

    assert len(moves) > 1000, f"Expected >1000 moves, got {len(moves)}"
    assert moves[0] == 's11', f"Expected first move to be 's11', got {moves[0]}"

    print(f"  ✓ Input parsing test passed ({len(moves)} moves)")

def test_output_validity(result):
    """Validate final output"""
    print("Validating output...")

    assert len(result) == 16, f"Expected 16 characters, got {len(result)}"
    assert set(result) == set('abcdefghijklmnop'), "Missing or extra characters"
    assert len(set(result)) == 16, "Duplicate characters found"

    print("  ✓ Output validation passed")

def run_all_tests():
    """Run all unit tests"""
    print("="*50)
    print("Running unit tests...")
    print("="*50)

    test_spin()
    test_exchange()
    test_partner()
    test_example_sequence()
    test_multiple_spins()
    test_complex_sequence()
    test_input_parsing()

    print("="*50)
    print("✓ All unit tests passed!")
    print("="*50)

if __name__ == '__main__':
    run_all_tests()
