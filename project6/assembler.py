import sys
import os

symbols = {
    "R0" : 0,
    "R1" : 1,
    "R2" : 2,
    "R3" : 3,
    "R4" : 4, 
    "R5" : 5, 
    "R6" : 6,
    "R7" : 7,
    "R8" : 8,
    "R9" : 9,
    "R10" : 10,
    "R11" : 11,
    "R12" : 12,
    "R13" : 13,
    "R14" : 14,
    "R15" : 15,
    "SCREEN" : 16384,
    "KBD" : 24576,
    
    "SP" : 0,
    "LCL" : 1,
    "ARG" : 2,
    "THIS" : 3,
    "THAT" : 4
}

# Destination codes
dest_table = {
    None: "000",  # No destination
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

# Computation codes
comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000", "M": "1110000",
    "!D": "0001101",
    "!A": "0110001", "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011", "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

# Jump codes
jump_table = {
    None: "000",  # No jump
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

if len(sys.argv) < 2:
    print("Please provide an .asm file as an argument.")
    print("Usage: python assembler.py filename.asm")
    sys.exit(1)

input_filename = sys.argv[1]

if not input_filename.endswith('.asm'):
    print("Error: Input file must have .asm extension")
    sys.exit(1)

# Prepare output filename
output_filename = input_filename.rsplit('.', 1)[0] + '.hack'

instructions = []
instruction_address = 0
next_available_address = 16

with open(input_filename, 'r') as file:
    for line in file:
        clean_line = line.split("//")[0].strip()
        if clean_line.startswith("(") and clean_line.endswith(")"):
            label = clean_line[1:-1]
            symbols[label] = instruction_address
        elif clean_line and not clean_line.startswith("//"):
            instructions.append(clean_line)
            instruction_address += 1

for i, instruction in enumerate(instructions):
    dest = None
    jump = None
    
    if instruction.startswith("@"):
        s = instruction.split("@")[1].strip()
        
        if s.isdigit():
            dec = int(s)
            AValue = bin(dec)[2:]  # Remove '0b' prefix
            AValue_instruction = AValue.zfill(16)
            instructions[i] = AValue_instruction
        else:
            symbol_address = symbols.get(s)
            
            if symbol_address is None:
                # Symbol not found, add it to the table
                symbols[s] = next_available_address
                next_available_address += 1
                symbol_address = symbols[s]
            
            symbol_address_instruction = bin(symbol_address)[2:].zfill(16)
            instructions[i] = symbol_address_instruction
    else:
        # C-instruction parsing
        if '=' in instruction:
            dest = instruction.split("=")[0]
            if ';' in instruction:
                jump = instruction.split(";")[1]
                comp = instruction.split("=")[1].split(";")[0]
            else:
                comp = instruction.split("=")[1]
                jump = None
        else:
            dest = None
            if ';' in instruction:
                jump = instruction.split(";")[1]
                comp = instruction.split(";")[0]
            else:
                comp = instruction
                jump = None
        
        binary_dest = dest_table[dest]
        binary_comp = comp_table[comp]
        binary_jump = jump_table[jump]
        binary_instruction = "111" + binary_comp + binary_dest + binary_jump
        
        instructions[i] = binary_instruction

with open(output_filename, 'w') as file:
    for instruction in instructions:
        file.write(instruction + '\n')

print(f"Assembled file written to: {output_filename}")
