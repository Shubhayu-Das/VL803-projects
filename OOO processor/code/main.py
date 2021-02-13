import PySimpleGUI as sg

from arf import ARF
from rat import RAT
from instruction import Instruction

from reservation_station import ReservationStation, ReservationStationEntry
from instruction_table import InstructionTable, InstructionTableEntry
from LS_buffer import LoadStoreBuffer

import constants
from gui import Graphics

program_src = "riscv_binary.elf"

program = []
instructions = []

cycle = 0

ADD_ReservationStation = ReservationStation(constants.ADD_SUB, size=3)
MUL_ReservationStation = ReservationStation(constants.MUL_DIV, size=2)

LS_Buffer = LoadStoreBuffer(size=3)

reservStationEntries = []
LSBufferEntries = []
instructions = []
GUI = Graphics()

# Load in the program
with open(program_src) as binary:
    program = binary.readlines()
    program = [inst.strip() for inst in program]

for inst in program:
    instructions.append(Instruction.segment(inst))

if constants.DEBUG:
    print("Instructions loaded and parsed")
    for inst in instructions:
        print(inst.disassemble())

instructionTable = InstructionTable(size=len(instructions))

for instruction in instructions:
    instructionTable.addEntry(instruction)

if constants.DEBUG:
    print("\nAll instructions added to instruction queue")
    print(instructionTable)

print(instructionTable._entries[1])

counter = 0
window = GUI.generateWindow()
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    counter += 1
    if counter % 1 == 0:
        cycle += 1
        instructionTable._entries[1].next(cycle)
        GUI.updateContents(window, instructionTable)

window.close()
print(instructionTable)
