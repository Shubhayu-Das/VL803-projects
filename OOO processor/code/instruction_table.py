from constants import DEBUG, NumCycles, RunState
from instruction import Instruction


class InstructionTableEntry:
    def __init__(self, instruction, id):
        self._instruction = instruction
        self._id = id
        self._state = RunState.NOT_STARTED
        self._rs_issue_cycle = ""
        self._exec_start = ""
        self._exec_complete = ""
        self._cdb_write = ""
        self._commit = ""
        self._counter = 0
        self._max_ticks = NumCycles[instruction.disassemble()["command"]] - 1

    def RS_Start(self, cycle):
        self._state = RunState.RS
        self._rs_issue_cycle = cycle

    def EX_Start(self, cycle):
        self._state = RunState.EX_START
        self._exec_start = cycle
        self.EX_Tick(cycle)

    def EX_Tick(self, cycle):
        if self._counter == self._max_ticks:
            self._exec_complete = cycle
            self._state = RunState.EX_END
        else:
            self._counter += 1

    def CDB_Write(self, cycle):
        self._state = RunState.CDB
        self._cdb_write = cycle

    def Commit(self, cycle):
        self._state = RunState.COMMIT
        self._commit = cycle

    def getBusyState(self):
        return self._state

    def getInstruction(self):
        return self._instruction

    def __str__(self):
        return f"{self._instruction.disassemble()}\t\t{self._rs_issue_cycle} {self._exec_start} {self._exec_complete} {self._cdb_write} {self._commit}"


class InstructionTable:
    def __init__(self, size):
        self._size = size
        self._index = 0
        self._entries = [None for _ in range(size)]

    def addEntry(self, instruction):
        self._entries[self._index] = InstructionTableEntry(instruction, self._index)

        self._index += 1

    def getEntry(self, index):
        if isinstance(index, Instruction):
            for entry in self._entries:
                if entry.getInstruction().PC == index.PC:
                    return entry
        else:
            return self._entries[index]

    def __str__(self):
        display = "Instruction\t\t\t\t\t\t\tRS Start Exec Start Exec End CDB Write Commit\n"
        for entry in self._entries:
            display += f"{entry.__str__()}\n"

        return display