from constants import DEBUG
from instruction import Instruction


class ReservationStationEntry:
    def __init__(self, instr, ARFTable, ROB, busy=True):
        self._instruction = instr
        self._busy = busy
        self._dest = instr.rd
        self._rob_updated = False

        self._src_val1, self._src_tag1 = self.__getSrcValTag(ARFTable.getRegister(instr.rs1), ROB)
        self._src_val2, self._src_tag2 = self.__getSrcValTag(ARFTable.getRegister(instr.rs2), ROB)       

    def __getSrcValTag(self, source, ROB):
        if source.isBusy():
            if ROB.getValue(source.getLink()) == "NA":
                return "-", source.getLink()
            else:
                return ROB.getValue(source.getLink()), "-"
        else:
            return source.getValue(), "-"

    def isExecuteable(self):
        if self._rob_updated:
            self._rob_updated = False
            return False
        else:
            return (self._src_val1 != "-") and (self._src_val2 != "-")

    def __exec(self):
        command = self._instruction.disassemble()["command"]
        lookup = {
            "ADD": lambda x, y: round(x+y, 2),
            "SUB": lambda x, y: round(x-y, 2),
            "MUL": lambda x, y: round(x*y, 2),
            "DIV": lambda x, y: round(x/y, 2),
        }

        return lookup[command](self._src_val1, self._src_val2)

    def getResult(self):
        return self.__exec()

    def getInstruction(self):
        return self._instruction

    def toggleState(self):
        self._busy = not self._busy

    def isBusy(self):
        return self._busy

    def getDestination(self):
        return self._dest

    def __str__(self):
        return f"""ReservationStationEntry:
                    Instruction: {self._instruction.disassemble()}
                    Busy State: {self._busy}
                    Destination: {self._dest}
                    Source Tag 1: {self._src_tag1}
                    Source Tag 2: {self._src_tag2}
                    Source Value 1: {self._src_val1}
                    Source Value 2: {self._src_val2}
                """


class ReservationStation:
    def __init__(self, inst_type, size):
        self._type = inst_type
        self._is_full = False
        self._size = size
        self._buffer = [None for _ in range(size)]
        self._index = 0
        self._just_freed = False

    def __updateFreeIndex(self, update=False):
        counter = 0
        backup = None

        if update and not self._is_full:
            return

        while(counter < self._size):
            self._index = (self._index + 1) % self._size
            if self._buffer[self._index] is None:
                if self._index == self._just_freed:
                    backup == self._index
                else:
                    break
            counter += 1

        if counter == self._size:
            if backup:
                self._index = backup
            else:
                self._is_full = True
                self._index = -1
        else:
            self._is_full = False

    def addEntry(self, instruction, ARFTable, ROB):
        if self._is_full:
            if DEBUG:
                print("Reservation station is full")
            return False

        if isinstance(instruction, Instruction):
            entry = ReservationStationEntry(instruction, ARFTable, ROB)
        elif isinstance(instruction, ReservationStationEntry):
            entry = instruction
        else:
            return False

        self._buffer[self._index] = entry
        if DEBUG:
            print(f"Added at RS{self._index + 1}")

        self.__updateFreeIndex()
        return True

    def updateEntries(self, robEntry, value, arf):
        for entry in self._buffer:
            if entry:
                if arf.getRegister(entry._instruction.rs1) == robEntry.getDestination():
                    entry._src_val1 = robEntry.getValue()
                    entry._src_tag1 = "-"
                    entry._rob_updated = True

                if arf.getRegister(entry._instruction.rs2) == robEntry.getDestination():
                    entry._src_val2 = robEntry.getValue()
                    entry._src_tag2 = "-"
                    entry._rob_updated = True

    def removeEntry(self, entry):
        if isinstance(entry, Instruction):
            for e in self._buffer:
                if e:
                    if e._instruction.PC == entry.PC:
                        entry = e
                        break

        elif not isinstance(entry, ReservationStationEntry):
            return False

        if entry in self._buffer:
            location = self._buffer.index(entry)
            self._just_freed = location
            self._buffer[location] = None
            self.__updateFreeIndex(update=True)

            if DEBUG:
                print(f"Removed from RS{location + 1}")

            return True
        else:
            return False

    def isBusy(self):
        condition = self._is_full and not (self._index == self._just_freed)
        self._just_freed = False

        return condition

    def getEntries(self):
        return self._buffer

    def __str__(self):
        return f"""Reservation Station for {self._type}.
                    Station Size: {self._size}
                    Busy State: {self.getBusyState()}
                """
