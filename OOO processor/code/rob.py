from collections import defaultdict

from constants import DEBUG
from instruction import Instruction
from register_bank import RegisterBank


class ROBEntry:
    def __init__(self, inst, destination, value, name=""):
        self._name = name
        self._inst = inst
        self._dest = destination
        self._value = value

    def setValue(self, new_val):
        self._value = new_val

    def getValue(self):
        return self._value

    def getName(self):
        return self._name

    def getDestination(self):
        return self._dest

    def getInstruction(self):
        return self._inst

    def __str__(self):
        return f"{self._name}, inst={self._inst}, val={self._value}, dest={self._dest}"


class ROBTable(RegisterBank):
    def __init__(self, size=8):
        self._tail = 1
        self._head = 1
        self._bank = defaultdict(None, {})

        for i in range(1, size+1):
            self._bank.update({f"ROB{i}": None})

    def addEntry(self, inst):
        if self._bank[f"ROB{self._head}"]:
            if DEBUG:
                print("ROB FULL")
            return False

        addr = f"ROB{self._head}"

        new_entry = ROBEntry(
            inst=inst,
            destination=inst.rd,
            value="NA",
            name=addr
        )

        self._bank[addr] = new_entry
        self._head += 1

        if self._head > len(self._bank):
            self._head = 1

        if DEBUG:
            print(f"ADDED to ROB @ {new_entry}")

        return addr

    def updateValue(self, inst, value):
        for entry in list(self._bank.values()):
            if entry:
                if entry.getInstruction().PC == inst.PC:
                    entry.setValue(value)
                    return entry

    def removeEntry(self):
        if not self._bank[f"ROB{self._tail}"]:
            if DEBUG:
                print("ROB EMPTY")
            return False
        
        removedValue = self._bank[f"ROB{self._tail}"]
        self._bank[f"ROB{self._tail}"] = None
        self._tail += 1

        if self._tail > len(self._bank):
            self._tail = 1

        if DEBUG:
            print(f"REMOVED from ROB @ {removedValue}")
        return removedValue

    def getHead(self):
        return self._bank[f"ROB{self._tail}"]

    def getEntries(self):
        return self._bank


if __name__ == "__main__":
    rob = ROBTable(2)

    entry1 = ROBEntry("ADD R1, R2, R3", "RAT.R3", 10, name="1")
    entry2 = ROBEntry("ADD R1, R2, R3", "RAT.R4", 10, name="2")
    entry3 = ROBEntry("ADD R1, R2, R3", "RAT.R5", 10, name="3")

    rob.addEntry(entry1)
    rob.addEntry(entry1)
    rob.addEntry(entry2)
    rob.addEntry(entry1)
    rob.removeEntry()
    rob.addEntry(entry1)
    rob.addEntry(entry1)