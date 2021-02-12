from constants import DEBUG


class LoadStoreBufferEntry:
    def __init__(self, instruction):
        self._instruction = instruction
        self._busy = False
        self._destination_tag = instruction.rd.getReg()
        self._offset = instruction.offset
        self._source_reg = instruction.rs1.getReg()

    def isBusy(self):
        return self._busy

    def __str__(self):
        return f"<Load Store Entry inst: {self._instruction.dissamble()}, {self._busy}>"


class LoadStoreBuffer:
    def __init__(self, size):
        self._size = size
        self._buffer = [None for _ in range(size)]
        self._is_full = False
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
                print("Entry Failed. Load store station is full")
            return False

        if isinstance(instruction, Instruction):
            entry = LoadStoreBufferEntry(instruction)
        elif not isinstance(instruction, LoadStoreBufferEntry):
            return False

        self._buffer[self._index] = entry
        if DEBUG:
            print(f"Added at LS buffer: {self._index + 1}")

        self.__updateFreeIndex()
        return entry

    def removeEntry(self, entry):
        if not isinstance(entry, LoadStoreBufferEntry):
            return False

        if entry in self._buffer:
            location = self._buffer.index(entry)
            self._buffer[location] = None
            self.__updateFreeIndex()

            if DEBUG:
                print(f"Removed from LS buffer: {location + 1}")
            return True
        else:
            return False

    def getFreeState(self):
        return self._is_full


if __name__ == "__main__":
    from instruction import Instruction

    lw_r10_r2_32 = "000000100000 01010 010 00010 1010011"
    inst = Instruction.segment(lw_r10_r2_32)

    LSBuffer = LoadStoreBuffer(3)

    entry1 = LSBuffer.addEntry(inst)
    entry2 = LSBuffer.addEntry(inst)
    entry3 = LSBuffer.addEntry(inst)
    entry4 = LSBuffer.addEntry(inst)
    LSBuffer.removeEntry(entry2)
    entry5 = LSBuffer.addEntry(inst)
    LSBuffer.removeEntry(entry3)
    entry6 = LSBuffer.addEntry(inst)