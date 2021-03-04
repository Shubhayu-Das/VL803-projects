from constants import DEBUG
from instruction import Instruction


class ReservationStationEntry:
    def __init__(self, instr, busy=True):
        self._instruction = instr
        self._busy = busy
        self._dest = instr.rd

        self._src_val1, self._src_tag1 = self.__getValSrc(instr.rs1)
        self._src_val2, self._src_tag2 = self.__getValSrc(instr.rs2)       

    def __getValSrc(self, source):
        if not source.getLink():
            return source.getValue(), "-"
        else:
            return "-", source.getSource()

    def toggleState(self):
        self._busy = not self._busy

    def isBusy(self):
        return self._busy

    def destination(self):
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

    def __updateFreeIndex(self):
        counter = 0
        while(counter < self._size):
            self._index = (self._index + 1) % self._size
            if self._buffer[self._index] is None:
                break
            counter += 1

        if counter == self._size:
            self._is_full = True
            self._index = -1
        else:
            self._is_full = False

    def addEntry(self, instruction):
        if self._is_full:
            if DEBUG:
                print("Reservation station is full")
            return False

        if isinstance(instruction, Instruction):
            entry = ReservationStationEntry(instruction)
        elif isinstance(instruction, ReservationStationEntry):
            entry = instruction
        else:
            return False

        self._buffer[self._index] = entry
        if DEBUG:
            print(f"Added at RS{self._index + 1}")

        self.__updateFreeIndex()
        return True

    def removeEntry(self, entry):
        if not isinstance(entry, ReservationStationEntry):
            return False

        if entry in self._buffer:
            location = self._buffer.index(entry)
            self._buffer[location] = None
            self.__updateFreeIndex()

            if DEBUG:
                print(f"Removed from RS{location + 1}")
            return True
        else:
            return False

    def getState(self):
        return self._is_full

    def __str__(self):
        return f"""Reservation Station for {self._type}.
                    Station Size: {self._size}
                    Busy State: {self.getBusyState()}
                """


if __name__ == "__main__":
    from instruction import Instruction
    from constants import ADD_SUB

    add_r9_r20_r21 = "0000 0001 0101 1010 0000 0100 1011 0011"
    inst = Instruction.segment(add_r9_r20_r21)

    addResvStation = ReservationStation(ADD_SUB, 3)

    entry1 = addResvStation.addEntry(inst)
    entry2 = addResvStation.addEntry(inst)
    entry3 = addResvStation.addEntry(inst)
    entry4 = addResvStation.addEntry(inst)
    addResvStation.removeEntry(entry2)
    entry5 = addResvStation.addEntry(inst)
    addResvStation.removeEntry(entry3)
    entry6 = addResvStation.addEntry(inst)
