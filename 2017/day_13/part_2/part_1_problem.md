# Problem Report: Firewall Packet Scanner

## Objective
Calculate the total severity of getting caught by security scanners while traversing through a firewall.

## Context
A packet needs to travel through a multi-layer firewall. Each layer has a security scanner that oscillates back and forth. The packet moves at a constant rate of one layer per picosecond. If the packet enters a layer when the scanner is at the top position, it gets caught.

## Input Format
The input is a list of firewall layers with the format:
```
depth: range
```

Where:
- **depth**: The position of the layer in the firewall (0-indexed)
- **range**: The number of positions the scanner covers in that layer (the height of the layer)

Notes:
- Not all depth positions have layers (there can be gaps)
- Each layer has a thickness of exactly 1
- Layers are listed with their depth and range values

Example input:
```
0: 3
1: 2
4: 4
6: 4
```

## Scanner Behavior
- Each scanner starts at position 0 (top) at picosecond 0
- Scanners move one position per picosecond
- Scanners oscillate: they move down to the bottom, then back up to the top, repeatedly
- For a layer with range `r`, the scanner visits positions: 0, 1, 2, ..., r-1, r-2, ..., 1, 0, 1, ... (repeating)
- All scanners move simultaneously

## Packet Movement
- The packet starts before layer 0
- At picosecond 0, the packet enters layer 0
- The packet moves one layer forward per picosecond
- Movement sequence: packet enters layer, then scanners move

## Caught Condition
- The packet is caught if a scanner is at position 0 (top) when the packet enters that layer
- If a scanner moves to position 0 after the packet has already entered, the packet is NOT caught

## Severity Calculation
For each layer where the packet is caught:
- **Severity of that layer** = depth × range

The **total severity** is the sum of all individual layer severities.

Example calculation:
- Caught at layer 0 (range 3): severity = 0 × 3 = 0
- Caught at layer 6 (range 4): severity = 6 × 4 = 24
- **Total severity** = 0 + 24 = 24

## Expected Output
A single integer representing the total severity of the trip through the firewall.

## Algorithm Requirements
1. Parse the input to extract depth and range for each layer
2. For each layer with a scanner, determine the scanner's position when the packet enters that layer
3. Check if the scanner is at position 0 when the packet enters (packet enters layer at picosecond = depth)
4. If caught, calculate severity (depth × range) and add to total
5. Return the total severity
