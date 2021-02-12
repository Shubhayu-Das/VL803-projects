class LoadStoreBufferEntry:
    def __init__(self, instruction):
        self._instruction = instruction
        self._busy = False
        self._destination_tag = instruction.rd
        self._offset = instruction.offset
        self._source_reg = instruction.rs1

    def isBusy(self):
        return self._busy

    def __str__(self):
        return f"<Load Store Entry> {self._instruction.dissamble()}, {self._busy}"


class LoadStoreBuffer:
    def __init__(self, size):
        self._size = size
        self._buffer = [None for _ in range(size)]
        self._is_full = False
        self._index = 0

    def addEntry(self, instruction):
        if self._is_full:
            return False

        if isinstance(instruction, Instruction):
            entry = LoadStoreBufferEntry(instruction)
        elif not isinstance(instruction, LoadStoreBufferEntry):
            return False

        self._buffer[self._index] = entry

        self._index = (self._index + 1) % self._size


if __name__ == "__main__":
    from instruction import Instruction

    lw_r10_r2_32 = "000000100000 01010 010 00010 1010011"
    inst = Instruction.segment(lw_r10_r2_32)
    print(isinstance(inst, Instruction))