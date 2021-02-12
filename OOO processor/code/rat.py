from register import Register

class RATRegister(Register):
    def __init__(self, val=0, name="", valid=True, link=None):
        super(RATRegister, self).__init__(val, name, valid, link)

    def __str__(self):
        return f"RAT.R{self._name}"


class RAT:
    R0  = RATRegister(val=0, name=bin(0))
    R1  = RATRegister(val=0, name=bin(1))
    R2  = RATRegister(val=0, name=bin(2))
    R3  = RATRegister(val=0, name=bin(3))
    R4  = RATRegister(val=0, name=bin(4))
    R5  = RATRegister(val=0, name=bin(5))
    R6  = RATRegister(val=0, name=bin(6))
    R7  = RATRegister(val=0, name=bin(7))
    R8  = RATRegister(val=0, name=bin(8))
    R9  = RATRegister(val=0, name=bin(9))
    R10 = RATRegister(val=0, name=bin(10))
    R11 = RATRegister(val=0, name=bin(11))
    R12 = RATRegister(val=0, name=bin(12))
    R13 = RATRegister(val=0, name=bin(13))
    R14 = RATRegister(val=0, name=bin(14))
    R15 = RATRegister(val=0, name=bin(15))
    R16 = RATRegister(val=0, name=bin(16))
    R17 = RATRegister(val=0, name=bin(17))
    R18 = RATRegister(val=0, name=bin(18))
    R19 = RATRegister(val=0, name=bin(19))
    R20 = RATRegister(val=0, name=bin(20))
    R21 = RATRegister(val=0, name=bin(21))
    R22 = RATRegister(val=0, name=bin(22))
    R23 = RATRegister(val=0, name=bin(23))
    R24 = RATRegister(val=0, name=bin(24))
    R25 = RATRegister(val=0, name=bin(25))
    R26 = RATRegister(val=0, name=bin(26))
    R27 = RATRegister(val=0, name=bin(27))
    R28 = RATRegister(val=0, name=bin(28))
    R29 = RATRegister(val=0, name=bin(29))
    R30 = RATRegister(val=0, name=bin(30))
    R31 = RATRegister(val=0, name=bin(31))
    R32 = RATRegister(val=0, name=bin(32))


if __name__ == "__main__":
    from rob import ROBEntry
    from arf import ARF
    from instruction import Instruction

    add_r9_r20_r21 = "0000 0001 0101 1010 0000 0100 1011 0011"
    inst = Instruction.segment(add_r9_r20_r21)

    rob1 = ROBEntry(inst, "ROB1")

    print(f"Initial RAT.R32: {RAT.R32.getValue()}")
    RAT.R32.link(rob1)
    RAT.R32.setValue(10)
    print(f"Linked RAT.R32: {RAT.R32.getValue()}")
    print(f"Actual RAT.R32 value: {RAT.R32._value}")
    print(f"ROB1 value: {rob1._value}")

    ARF.R32.link(RAT.R32)
    print(f"ARF.R32 value: {ARF.R32.getValue()}")
    print(f"Actual ARF.R32 value: {ARF.R32._value}")