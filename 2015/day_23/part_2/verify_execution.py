from solution import parse_instructions, simulate

print("Verifying execution trace for Part 2 (a=1, b=0):")
print("=" * 70)

instructions = parse_instructions("input.md")
print(f"Total instructions loaded: {len(instructions)}")
print(f"\nFirst instruction: {instructions[0]}")
print(f"Instruction at PC=22: {instructions[22]}")
print(f"Instruction at PC=41: {instructions[41]}")
print()

# Run with verbose mode for first 20 iterations
class LimitedVerboseSimulator:
    def __init__(self, instructions, limit=20):
        self.instructions = instructions
        self.limit = limit
        self.registers = {"a": 1, "b": 0}
        self.pc = 0
        self.iterations = 0

    def run(self):
        from solution import execute_instruction

        while 0 <= self.pc < len(self.instructions):
            if self.iterations < self.limit:
                print(f"[{self.iterations}] PC={self.pc:2d} | a={self.registers['a']:10d}, b={self.registers['b']:3d} | {self.instructions[self.pc]}")

            self.pc = execute_instruction(self.instructions[self.pc], self.registers, self.pc)
            self.iterations += 1

            if self.iterations == self.limit:
                print(f"... (showing first {self.limit} iterations only)")

            if self.iterations > 1_000_000:
                raise RuntimeError("Exceeded max iterations")

        print(f"\nProgram terminated at PC={self.pc} after {self.iterations} iterations")
        print(f"Final: a={self.registers['a']}, b={self.registers['b']}")
        return self.registers

sim = LimitedVerboseSimulator(instructions, limit=30)
registers = sim.run()

print("\n" + "=" * 70)
print(f"Final answer for Part 2: b = {registers['b']}")
print("=" * 70)

# Also run Part 1 for comparison
print("\nRunning Part 1 (a=0, b=0) for comparison:")
registers_part1 = simulate(instructions, initial_a=0, initial_b=0, verbose=False)
print(f"Part 1 result: b = {registers_part1['b']}")
print(f"Part 2 result: b = {registers['b']}")
print(f"Results are different: {registers_part1['b'] != registers['b']}")
