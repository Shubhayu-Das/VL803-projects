import PySimpleGUI as sg
import time

from arf import ARF
from rat import RAT
from instruction import Instruction

from reservation_station import ReservationStation, ReservationStationEntry
from instruction_table import InstructionTable, InstructionTableEntry
from LS_buffer import LoadStoreBuffer
from rob import ROBTable

import constants
from gui import Graphics

program_src = "riscv_binary.elf"
instructions = []
cycle = 0

ARFTable = ARF()
RATTable = RAT()

ADD_RS = ReservationStation(constants.ADD_SUB, size=3)
MUL_RS = ReservationStation(constants.MUL_DIV, size=2)

# LS_Buffer = LoadStoreBuffer(size=3)
ROB = ROBTable(size=8)

# reservStationEntries = []
# LSBufferEntries = []

# Load in the program
with open(program_src) as binary:
    program = binary.readlines()
    program = [inst.strip() for inst in program]

    for inst in program:
        instructions.append(Instruction.segment(inst, ARFTable))

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


# Function to try and dispatch next instruction if corresponding RS is free
def tryDispatch():
    for i in range(0, len(instructions)):
        entry = instructionTable.getEntry(i)

        if entry.getState() == constants.RunState.NOT_STARTED:
            instruction = entry.getInstruction()
            instruction_type = instruction.disassemble()["command"]

            if instruction_type in ["ADD", "SUB"]:
                if not ADD_RS.getState():
                    if not RATTable.getState():
                        ratRegister = RATTable.addEntry(instruction.rd)
                        instruction.rd.setLink(ratRegister)
                        ratRegister.setLink(ROB.addEntry(instruction))
                        ADD_RS.addEntry(instruction)
                        entry.RS_Start(cycle)
                        break
    
            elif instruction_type in ["MUL", "DIV"]:
                if not MUL_RS.getState():
                    if not RATTable.getState():
                        ratRegister = RATTable.addEntry(instruction.rd)
                        instruction.rd.setLink(ratRegister)
                        ratRegister.setLink(ROB.addEntry(instruction))
                        MUL_RS.addEntry(instruction)
                        entry.RS_Start(cycle)
                        break
    
            elif instruction_type in ["LW", "SW"]:
                pass

# Function to get the sources and update the dependencies

def logic_loop():
    tryDispatch()

    



GUI = Graphics()
counter = 0
window = GUI.generateWindow()

# Main event loop
while True:
    event, values = window.read(timeout=200)
    if event == sg.WIN_CLOSED:
        break

    counter += 1
    if counter % 10 == 0:
        cycle += 1
        # next(instructionTable._entries[4], cycle)
        logic_loop()
        
        GUI.updateContents(
            window,
            instructionTable,
            ROB,
            resStats={
                constants.ADD_SUB: ADD_RS,
                constants.MUL_DIV: MUL_RS
                },
            ARF=ARFTable,
            RAT=RATTable
        )
     
    # time.sleep(100)


window.close()
