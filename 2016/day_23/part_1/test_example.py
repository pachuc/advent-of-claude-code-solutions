from solution import AssembunnyInterpreter

# Test the example from the problem statement
example_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""

interpreter = AssembunnyInterpreter(initial_a=0)  # Start with a=0, first instruction sets it to 2
interpreter.parse_instructions(example_input)
result = interpreter.run()

print(f"Example result: {result}")
print(f"Expected: 3")
print(f"Test passed: {result == 3}")
