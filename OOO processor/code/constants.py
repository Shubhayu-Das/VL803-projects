class NumCycles:
    ADD = 1
    SUB = 1
    LW = 5
    MUL = 10
    DIV = 40


class Register:
    R1 = "00001"
    R2 = "00010"
    R3 = "00011"
    R4 = "00100"
    R5 = "00101"
    R6 = "00110"
    R7 = "00111"
    R8 = "01000"
    R9 = "01001"
    R10 = "01010"


class ARF(Register):
    pass


class RAT(Register):
    pass


class ROB:
    ROB1 = "ROB1"
    ROB2 = "ROB2"
    ROB3 = "ROB3"
    ROB4 = "ROB4"
    ROB5 = "ROB5"
    ROB6 = "ROB6"
    ROB7 = "ROB7"
    ROB8 = "ROB8"


ADD_SUB = "ADD/SUB"
MUL_DIV = "MUL/DIV"


if __name__ == "__main__":
    print(f"{ARF.R1}")