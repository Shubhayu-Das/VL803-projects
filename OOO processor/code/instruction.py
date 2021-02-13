'''
The following instructions are (going to be) supported by this program
             31:25   24:20  19:15   14:12  11:7   6:0
instruction - funct7 - rs2 - rs1 - funct3 - rd - opcode
    ADD      0000000 - src2 - src1 - 000 - dest - 0110011
    SUB      0100000 - src2 - src1 - 000 - dest - 0110011
    LW        offset[31:20] - src1 - 010 - dest - 1010011

    MUL      0000001 - src2 - src1 - 000 - dest - 0110011
    DIV      0000001 - src2 - src1 - 100 - dest - 0110011

ADD/SUB/MUL/DIV rd, rs1, rs2

References: 
1. RV32I - https://github.com/riscv/riscv-opcodes/blob/master/opcodes-rv32i
2. RV32M - https://github.com/riscv/riscv-opcodes/blob/master/opcodes-rv32m
'''
from arf import ARF
from rat import RAT


class Instruction:
    I_TYPE = "J"
    M_TYPE = "M"

    def __init__(self, funct7="0000000", rs2="00000", rs1="00000",
                 rd="00000", funct3="000", opcode="0000000", hasOffset=False):
        self.rs2 = None
        self.offset = None
        self.funct7 = None

        if hasOffset:
            self.offset = funct7 + rs2
        else:
            self.funct7 = funct7
            self.rs2 = ARF.getReg(rs2)

        self.hasOffset = hasOffset
        self.rs1 = ARF.getReg(rs1)
        self.rd = ARF.getReg(rd)
        self.funct3 = funct3
        self.opcode = opcode
        self.type = self.decodeType(funct7, opcode)

    def decodeType(self, funct7, opcode):
        if funct7 == "0000001" and opcode != "1010011":
            return Instruction.M_TYPE
        else:
            return Instruction.I_TYPE

    def disassemble(self):
        command = ""
        rs1 = self.rs1.__str__()
        rd = self.rd.__str__()

        if self.hasOffset:
            offset = int(self.offset, 2)
            if self.opcode == "1010011" and self.funct3 == "010":
                command = "LW"
            else:
                return -1

            return {
                "command": command,
                "rd": rd,
                "rs1": rs1,
                "offset": offset
            }
            
        else:
            rs2 = self.rs2.__str__()

            if self.opcode == "0110011":
                if self.funct3 == "000":
                    if self.funct7 == "0000000":
                        command = "ADD"
                    elif self.funct7 == "0100000":
                        command = "SUB"
                    elif self.funct7 == "0000001":
                        command = "MUL"
                    else:
                        return -1
                elif self.funct3 == "100":
                    if self.funct7 == "0000001":
                        command = "DIV"
                    else:
                        return -1

            return {
                "command": command,
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2
            }

    @classmethod
    def segment(self, instruction):
        instruction = instruction.replace(" ", "")
        if len(instruction) != 32:
            return -1

        funct7 = instruction[0:7]
        rs2 = instruction[7:12]
        rs1 = instruction[12:17]
        funct3 = instruction[17:20]
        rd = instruction[20:25]
        opcode = instruction[25:32]
        hasOffset = False

        # If we encounter a load word
        if funct3 == "010" and opcode == "1010011":
            hasOffset = True

        return Instruction(
            funct7=funct7,
            rs2=rs2,
            rs1=rs1,
            rd=rd,
            funct3=funct3,
            opcode=opcode,
            hasOffset=hasOffset
        )

    def __str__(self):
        if self.hasOffset:
            return f"<{self.type}-Instruction offset:{self.offset} rs1:{self.rs1} funct3:{self.funct3} rd:{self.rd} opcode:{self.opcode}>"
        else:
            return f"<{self.type}-Instruction funct7:{self.funct7} rs2:{self.rs2} rs1:{self.rs1} funct3:{self.funct3} rd:{self.rd} opcode:{self.opcode}>"


if __name__ == "__main__":
    add_r9_r20_r21 = "0000 0001 0101 1010 0000 0100 1011 0011"
    lw_r10_r2_32 = "000000100000 01010 010 00010 1010011"
    inst = Instruction.segment(add_r9_r20_r21)
    print(inst)
    print(inst.disassemble())
