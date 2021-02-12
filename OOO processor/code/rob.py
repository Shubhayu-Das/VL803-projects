from exceptions import AlreadyExistsException
from constants import DEBUG
from instruction import Instruction


class ROBEntry:
    def __init__(self, instruction, name=""):
        self._instruction = instruction
        self._destination = instruction.rd
        self._value = None
        self._name = name

        instruction.rd.link(self)

    def setName(self, name):
        self._name = name

    def getReg(self):
        return self

    def getValue(self):
        if self._value is not None:
            return self._value
        else:
            return self

    def setValue(self, val):
        self._value = val

    def __str__(self):
        return f"<ROB Entry {self._name}, instr: {self._instruction.disassemble()}, dest: {self._destination}, value: {self._value}>"


class ROBTable:
    def __init__(self, size=3):
        self._head = 0
        self._tail = 0
        self._is_full = False
        self._size = size

        self._entries = [None for i in range(1, size + 1)]

    def addEntry(self, instruction):
        if isinstance(instruction, Instruction):
            entry = ROBEntry(instruction)
        else:
            if DEBUG:
                print("Can only enter instructions into ROBTable")
            return False

        if self._is_full:
            if DEBUG:
                print("ROB is full, entry not made")
            return False
        else:
            entry.setName(f"ROB{self._tail + 1}")

            self._entries[self._tail] = entry
            if DEBUG:
                print(f"Added {entry} to ROB at {self._tail}")
                
            self._tail = (self._tail + 1) % self._size
            if self._tail == self._head:
                self._is_full = True

            return entry

    def removeEntry(self):
        entry = self._entries[self._head]
        self._entries[self._head] = None

        if DEBUG:
            print(f"Removed {entry} from ROB at {self._head}")
        
        self._head = (self._head + 1) % self._size
        if self._head != self._tail:
            self._is_full = False
        
        return entry


if __name__ == "__main__":
    from arf import ARF
    from instruction import Instruction

    ARF.R9.setValue(9)
    ARF.R20.setValue(20)
    ARF.R21.setValue(21)
    add_r9_r20_r21 = "0000 0001 0101 1010 0000 0100 1011 0011"
    inst = Instruction.segment(add_r9_r20_r21)

    rob = ROBTable()

    entry = rob.addEntry(inst)

    print(ARF.R9.getReg())
    entry.setValue(10)
    ARF.R9.unlink()
    print(ARF.R9.getValue())
    print()

    rob.addEntry(inst)
    rob.removeEntry()
    rob.addEntry(inst)
    rob.addEntry(inst)
    rob.addEntry(inst)
    rob.removeEntry()
    rob.removeEntry()
    rob.addEntry(inst)
