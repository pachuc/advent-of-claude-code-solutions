def parse_address(address):
    """
    Parse an IPv7 address into supernet and hypernet sequences.
    Returns: (supernet_sequences, hypernet_sequences)

    Supernet sequences are outside brackets.
    Hypernet sequences are inside brackets [].
    """
    supernets = []
    hypernets = []
    current_sequence = ""
    inside_brackets = False

    for char in address:
        if char == '[':
            # Save current supernet sequence if non-empty
            if current_sequence:
                supernets.append(current_sequence)
            current_sequence = ""
            inside_brackets = True
        elif char == ']':
            # Save current hypernet sequence if non-empty
            if current_sequence:
                hypernets.append(current_sequence)
            current_sequence = ""
            inside_brackets = False
        else:
            current_sequence += char

    # Don't forget the last sequence if it exists
    if current_sequence:
        if inside_brackets:
            hypernets.append(current_sequence)
        else:
            supernets.append(current_sequence)

    return supernets, hypernets


def find_abas(sequence):
    """
    Find all ABA patterns in a sequence.

    An ABA is a three-character sequence where:
    - First and third characters are the same
    - Middle character is different from the outer characters

    Examples: 'xyx', 'aba', 'eke' are valid ABAs
    'aaa' is NOT valid (middle must differ)

    Returns: Set of ABA patterns found in the sequence
    """
    abas = set()

    # Sliding window of size 3
    for i in range(len(sequence) - 2):
        window = sequence[i:i+3]
        # Check if it's a valid ABA pattern
        if window[0] == window[2] and window[0] != window[1]:
            abas.add(window)

    return abas


def aba_to_bab(aba):
    """
    Convert an ABA pattern to its corresponding BAB pattern.

    For an ABA of form XYX, the corresponding BAB is YXY.

    Examples:
    - 'aba' -> 'bab'
    - 'xyx' -> 'yxy'
    - 'eke' -> 'kek'
    - 'zbz' -> 'bzb'
    """
    outer = aba[0]
    middle = aba[1]
    return middle + outer + middle


def supports_ssl(address):
    """
    Check if an IPv7 address supports SSL (super-secret listening).

    SSL is supported if:
    1. At least one ABA exists in supernet sequences (outside brackets)
    2. The corresponding BAB exists in hypernet sequences (inside brackets)

    Examples from problem.md:
    - aba[bab]xyz -> True (aba -> bab match)
    - xyx[xyx]xyx -> False (xyx -> yxy, but only xyx in hypernet)
    - aaa[kek]eke -> True (eke -> kek match, aaa invalid)
    - zazbz[bzb]cdb -> True (zbz -> bzb match)
    """
    supernets, hypernets = parse_address(address)

    # Find all ABAs in all supernet sequences
    all_abas = set()
    for supernet in supernets:
        all_abas.update(find_abas(supernet))

    # Find all BABs (which are also ABA patterns) in all hypernet sequences
    all_babs = set()
    for hypernet in hypernets:
        all_babs.update(find_abas(hypernet))

    # Check for correspondence - if any ABA's corresponding BAB exists in hypernets
    for aba in all_abas:
        corresponding_bab = aba_to_bab(aba)
        if corresponding_bab in all_babs:
            return True

    return False


def main():
    """
    Main function to process input and count SSL-supporting addresses.
    """
    count = 0

    with open('input.md', 'r') as f:
        for line in f:
            address = line.strip()
            if address and supports_ssl(address):
                count += 1

    print(count)


if __name__ == "__main__":
    main()
