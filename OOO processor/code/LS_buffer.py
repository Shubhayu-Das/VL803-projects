from constants import DEBUG
from instruction import Instruction


class LoadStoreBufferEntry:
    def __init__(self, instr, ARFTable, ROB):
        self._instruction = instr
        self._busy = False
        self._dest = instr.rd
        self._offset = 4*int(instr.offset, 2)
        self._src_reg = ARFTable.getRegister(instr.rs1)

    def isExecuteable(self):
        return not self._src_reg.isBusy()

    def isBusy(self):
        return self._busy

    def getInstruction(self):
        return self._instruction

    def getResult(self):
        return 1

    def __str__(self):
        return f"<LW/SW buffer entry: {self._instruction.dissamble()}, {self._busy}>"


class LoadStoreBuffer:
    def __init__(self, size, memory):
        self._size = size
        self._buffer = [None for _ in range(size)]
        self._is_full = False
        self._index = 0
        self._memory = memory
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

    def addEntry(self, instr, ARFTable, ROB):
        if self._is_full:
            if DEBUG:
                print("Entry Failed. Load store station is full")
            return False

        if isinstance(instr, Instruction):
            entry = LoadStoreBufferEntry(instr, ARFTable, ROB)

        self._buffer[self._index] = entry
        if DEBUG:
            print(f"Added at LS buffer: {self._index + 1}")

        self.__updateFreeIndex()
        return entry

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
        return self._is_full

    def getEntries(self):
        return self._buffer

    def __str__(self):
        return f"<LW/SW Buffer>"