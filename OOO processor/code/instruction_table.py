from constants import DEBUG, NumCycles

class InstructionTableEntry:
    def __init__(self, instruction, id):
        self._instruction = instruction
        self._id = id
        self._state = None
        self._rs_issue_cycle = None
        self._exec_start = None
        self._exec_complete = None
        self._cdb_write = None
        self._commit = None

    def RS_Start(self, cycle):
        self._state = "RS"
        self._rs_issue_cycle = cycle

    def EX_Start(self, cycle):
        self._state = "EX1"
        self._exec_start = cycle
        self._exec_complete = cycle + NumCycles[self._instruction.disassemble()["command"]] - 1

    def CDB_Write(self, cycle):
        if cycle == self._exec_complete + 1:
            self._state = "CDB"
            self._cdb_write = cycle
        else:
            self._state = self._state[:2] + str(int(self._state[2:]) + 1)

    def Commit(self, cycle):
        self._state = "Done"
        self._commit = cycle

    def next(self, cycle):
        if self._commit:
            return True
        elif self._cdb_write:
            self.Commit(cycle)
        elif self._exec_start:
            self.CDB_Write(cycle)
        elif self._rs_issue_cycle:
            self.EX_Start(cycle)
        else:
            self.RS_Start(cycle)

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

    def __str__(self):
        display = "Instruction\t\t\t\t\t\t\tRS Start Exec Start Exec End CDB Write Commit\n"
        for entry in self._entries:
            display += f"{entry.__str__()}\n"

        return display