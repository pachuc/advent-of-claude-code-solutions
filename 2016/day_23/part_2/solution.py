class AssembunnyInterpreter:
    def __init__(self, initial_a=12, optimize=True):
        """Initialize the interpreter with register values."""
        self.registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
        self.instructions = []
        self.pc = 0  # Program counter
        self.modified_instructions = set()  # Track toggled instructions
        self.optimize = optimize  # Enable/disable optimization
        self.optimization_count = 0  # Track how many times optimization is applied

    def parse_instructions(self, input_text):
        """Parse input text into a list of instructions."""
        self.instructions = []
        for line in input_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            opcode = parts[0]
            arg1 = parts[1] if len(parts) > 1 else None
            arg2 = parts[2] if len(parts) > 2 else None
            self.instructions.append([opcode, arg1, arg2])

    def is_register(self, value):
        """Check if a value is a valid register name."""
        return value in ['a', 'b', 'c', 'd']

    def get_value(self, arg):
        """Get the value of an argument (either register value or literal)."""
        if self.is_register(arg):
            return self.registers[arg]
        else:
            return int(arg)

    def execute_cpy(self, x, y):
        """Execute cpy x y: copy value x to register y."""
        if not self.is_register(y):
            # Invalid instruction, skip
            self.pc += 1
            return
        self.registers[y] = self.get_value(x)
        self.pc += 1

    def execute_inc(self, x):
        """Execute inc x: increment register x."""
        if not self.is_register(x):
            # Invalid instruction, skip
            self.pc += 1
            return
        self.registers[x] += 1
        self.pc += 1

    def execute_dec(self, x):
        """Execute dec x: decrement register x."""
        if not self.is_register(x):
            # Invalid instruction, skip
            self.pc += 1
            return
        self.registers[x] -= 1
        self.pc += 1

    def execute_jnz(self, x, y):
        """Execute jnz x y: jump y instructions if x is not zero."""
        if self.get_value(x) != 0:
            offset = self.get_value(y)
            self.pc += offset
        else:
            self.pc += 1

    def execute_tgl(self, x):
        """Execute tgl x: toggle instruction at offset x."""
        offset = self.get_value(x)
        target = self.pc + offset

        # Check if target is within bounds
        if target < 0 or target >= len(self.instructions):
            self.pc += 1
            return

        # Mark instruction as modified BEFORE toggling
        self.modified_instructions.add(target)

        # Toggle the instruction
        instr = self.instructions[target]
        opcode = instr[0]

        # Check if it's a one-argument or two-argument instruction
        if instr[2] is None:
            # One-argument instruction
            if opcode == 'inc':
                self.instructions[target][0] = 'dec'
            else:
                # Any other one-arg instruction (including dec, tgl) becomes inc
                self.instructions[target][0] = 'inc'
        else:
            # Two-argument instruction
            if opcode == 'jnz':
                self.instructions[target][0] = 'cpy'
            else:
                # Any other two-arg instruction (including cpy) becomes jnz
                self.instructions[target][0] = 'jnz'

        self.pc += 1

    def try_optimize_multiplication(self):
        """
        Detect and optimize multiplication pattern at current PC.
        Pattern (6 instructions starting at pc):
          cpy b c
          inc a
          dec c
          jnz c -2
          dec d
          jnz d -5

        This computes: a += b * d, then sets c=0 and d=0
        """
        pc = self.pc

        # Check if we have enough instructions ahead
        if pc + 6 > len(self.instructions):
            return False

        # Check pattern hasn't been modified by tgl
        for i in range(pc, pc + 6):
            if i in self.modified_instructions:
                return False

        # Match the specific pattern
        pattern = [
            ('cpy', 'b', 'c'),  # pc+0
            ('inc', 'a', None), # pc+1
            ('dec', 'c', None), # pc+2
            ('jnz', 'c', '-2'), # pc+3
            ('dec', 'd', None), # pc+4
            ('jnz', 'd', '-5')  # pc+5
        ]

        for i, (expected_op, expected_arg1, expected_arg2) in enumerate(pattern):
            instr = self.instructions[pc + i]
            if instr[0] != expected_op or instr[1] != expected_arg1:
                return False
            # Convert to string for comparison to handle both string and int arguments
            if expected_arg2 is not None and str(instr[2]) != str(expected_arg2):
                return False

        # Apply optimization: a += b * d, c = 0, d = 0
        b_val = self.registers['b']
        d_val = self.registers['d']
        self.registers['a'] += b_val * d_val
        self.registers['c'] = 0
        self.registers['d'] = 0
        self.pc += 6  # Skip entire pattern
        self.optimization_count += 1

        return True

    def run(self):
        """Execute the program and return the final value of register a."""
        while 0 <= self.pc < len(self.instructions):
            # Try optimization before executing normal instructions
            if self.optimize and self.try_optimize_multiplication():
                continue

            instr = self.instructions[self.pc]
            opcode = instr[0]
            arg1 = instr[1]
            arg2 = instr[2]

            if opcode == 'cpy':
                self.execute_cpy(arg1, arg2)
            elif opcode == 'inc':
                self.execute_inc(arg1)
            elif opcode == 'dec':
                self.execute_dec(arg1)
            elif opcode == 'jnz':
                self.execute_jnz(arg1, arg2)
            elif opcode == 'tgl':
                self.execute_tgl(arg1)
            else:
                # Unknown opcode, treat as no-op
                self.pc += 1

        return self.registers['a']


def main():
    """Main function to run the interpreter."""
    # Read input from file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Create interpreter with a=12 and optimization enabled
    interpreter = AssembunnyInterpreter(initial_a=12)
    interpreter.parse_instructions(input_text)
    result = interpreter.run()

    print(result)


if __name__ == '__main__':
    main()
