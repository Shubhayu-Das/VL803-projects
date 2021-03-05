import re
from constants import DEBUG


def splitOperands(program):
    program = [inst for inst in program if not inst.startswith(";")]
    program = [re.split(",|\ ", inst.strip()) for inst in program]
    program = [[word.upper().replace('X', '') for word in inst if word] for inst in program]

    return program

def pad(number, n):
    number = number[2:]
    while len(number) < n:
        number = "0" + number

    return number

def assembler(filename):
    program = []
    assembly = []
    mapping = {
        "ADD": {
            "funct7": "0000000",
            "funct3": "000",
            "opcode": "0110011"
        },
        "SUB": {
            "funct7": "0100000",
            "funct3": "000",
            "opcode": "0110011"
        },
        "MUL": {
            "funct7": "0000001",
            "funct3": "000",
            "opcode": "0110011"
        },
        "DIV": {
            "funct7": "0000001",
            "funct3": "100",
            "opcode": "0110011"
        },
        "LW": {
            "funct3": "010",
            "opcode": "1010011"
        },
    }

    with open(filename) as sourceCode:
        program = (sourceCode.readlines())

    program = splitOperands(program)
    for i, inst in enumerate(program):
        if "LW" in inst:
            offset, rs1 = inst[2].split('(')

            offset = pad(bin(int(offset)), 12)
            rs1 = pad(bin(int(rs1.replace(')', ''))), 5)
            rd = pad(bin(int(inst[1])), 5)

            assembly.append(offset + rs1 + mapping["LW"]["funct3"] + rd + mapping["LW"]["opcode"])
        else:
            rd = pad(bin(int(inst[1])), 5)
            rs1 = pad(bin(int(inst[2])), 5)
            rs2 = pad(bin(int(inst[3])), 5)
            
            assembly.append(mapping[inst[0]]["funct7"] + rs2 + rs1 + mapping[inst[0]]["funct3"] + rd + mapping[inst[0]]["opcode"])
            

    if DEBUG:
        from instruction import Instruction
        for inst in assembly:
            print(f"{Instruction.segment(inst).disassemble()} - {inst}")

    with open("riscv_binary.elf", 'w') as destFile:
        for idx, inst in enumerate(assembly):
            destFile.write(inst)
            if idx < len(assembly) - 1:
                destFile.write("\n")


assembler("riscv_program.asm")