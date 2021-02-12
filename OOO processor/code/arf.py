from register import Register


class ARFRegister(Register):
    def __init__(self, val=0, name="", valid=True, link=None):
        super(ARFRegister, self).__init__(val, name, valid, link)

    def __str__(self):
        return f"ARF.R{self._name}"


class ARF:
    R0  = ARFRegister(val=0, name=bin(0))
    R1  = ARFRegister(val=0, name=bin(1))
    R2  = ARFRegister(val=0, name=bin(2))
    R3  = ARFRegister(val=0, name=bin(3))
    R4  = ARFRegister(val=0, name=bin(4))
    R5  = ARFRegister(val=0, name=bin(5))
    R6  = ARFRegister(val=0, name=bin(6))
    R7  = ARFRegister(val=0, name=bin(7))
    R8  = ARFRegister(val=0, name=bin(8))
    R9  = ARFRegister(val=0, name=bin(9))
    R10 = ARFRegister(val=0, name=bin(10))
    R11 = ARFRegister(val=0, name=bin(11))
    R12 = ARFRegister(val=0, name=bin(12))
    R13 = ARFRegister(val=0, name=bin(13))
    R14 = ARFRegister(val=0, name=bin(14))
    R15 = ARFRegister(val=0, name=bin(15))
    R16 = ARFRegister(val=0, name=bin(16))
    R17 = ARFRegister(val=0, name=bin(17))
    R18 = ARFRegister(val=0, name=bin(18))
    R19 = ARFRegister(val=0, name=bin(19))
    R20 = ARFRegister(val=0, name=bin(20))
    R21 = ARFRegister(val=0, name=bin(21))
    R22 = ARFRegister(val=0, name=bin(22))
    R23 = ARFRegister(val=0, name=bin(23))
    R24 = ARFRegister(val=0, name=bin(24))
    R25 = ARFRegister(val=0, name=bin(25))
    R26 = ARFRegister(val=0, name=bin(26))
    R27 = ARFRegister(val=0, name=bin(27))
    R28 = ARFRegister(val=0, name=bin(28))
    R29 = ARFRegister(val=0, name=bin(29))
    R30 = ARFRegister(val=0, name=bin(30))
    R31 = ARFRegister(val=0, name=bin(31))
    R32 = ARFRegister(val=0, name=bin(32))

    @classmethod
    def getReg(self, binary):
        regNo = int(binary, 2)
        if regNo >= 0 and regNo <= 32:
            return eval(f"ARF.R{regNo}")
        else:
            return False


if __name__ == "__main__":
    print(f"Decoded register: {ARF.getReg('00100')}")

    from rat import RAT

    print("Initial ARF.R32: ", ARF.R32.getReg())
    print("Linking ARF.R32 to RAT.R30")
    ARF.R32.link(RAT.R30)
    print("ARF.R32 after linking: ", ARF.R32.getReg())
    
    ARF.R32.setValue(32)

    print(f"\nValue in RAT.R30: {RAT.R30.getValue()}")
    print(f"Value in ARF.R32: {ARF.R32._value}")
    print(f"Value read when called for ARF.R32: {ARF.R32.getValue()}")

    ARF.R32.unlink()
    ARF.R32.setValue(ARF.R32.getValue())
    print(ARF.R32.getReg())
    print(f"Value in ARF.R32: {ARF.R32._value}")
