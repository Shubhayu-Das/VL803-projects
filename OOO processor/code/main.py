import copy
import sys
import PySimpleGUI as sg

from arf import ARF
from rat import RAT
from instruction import Instruction

from reservation_station import ReservationStation, ReservationStationEntry
from instruction_table import InstructionTable, InstructionTableEntry
from LS_buffer import LoadStoreBuffer
from rob import ROBTable

import constants
from gui import Graphics

if len(sys.argv) < 2:
    program_src = "build/riscv_program.elf"
else:
    program_src = sys.argv[2]

instructions = []
cycle = 0

ARFTable = ARF(size=10)
RATTable = RAT(size=10)

ADD_RS = ReservationStation(constants.ADD_SUB, size=3)
MUL_RS = ReservationStation(constants.MUL_DIV, size=2)

# LS_Buffer = LoadStoreBuffer(size=3)
ROB = ROBTable(size=8)


# Load in the program
with open(program_src) as binary:
    program = binary.readlines()
    program = [inst.strip() for inst in program]

    for PC, inst in enumerate(program):
        instructions.append(Instruction.segment(inst, ARFTable, PC=PC+1))

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
# Updates all relevant source mappings too
def tryDispatch():
    for i in range(0, len(instructions)):
        entry = instructionTable.getEntry(i)

        if entry.getBusyState() == constants.RunState.NOT_STARTED:
            instruction = entry.getInstruction()
            instruction_type = instruction.disassemble()["command"]

            if instruction_type in ["ADD", "SUB"]:
                if not ADD_RS.getBusyState():
                    if not RATTable.getBusyState():
                        ratRegister = RATTable.addEntry(instruction.rd)

                        ratRegister.setLink(ROB.addEntry(instruction, ratRegister))
                        instruction.rd.setLink(ratRegister)
                        ADD_RS.addEntry(instruction)
                        entry.RS_Start(cycle)
                        break
    
            elif instruction_type in ["MUL", "DIV"]:
                if not MUL_RS.getBusyState():
                    if not RATTable.getBusyState():
                        ratRegister = RATTable.addEntry(instruction.rd)
                        
                        ratRegister.setLink(ROB.addEntry(instruction, ratRegister))
                        instruction.rd.setLink(ratRegister)
                        MUL_RS.addEntry(instruction)
                        entry.RS_Start(cycle)
                        break
    
            elif instruction_type in ["LW", "SW"]:
                pass

# Function to simulate the execution of the process
def tryExecute():
    for RS in [ADD_RS, MUL_RS]:
        for entry in RS.getEntries():
            if entry:                
                it_entry = instructionTable.getEntry(entry._instruction)
                if it_entry.getBusyState() == constants.RunState.RS and entry.isExecuteable():
                        it_entry.EX_Start(cycle)
                        break

def proceedExecuting():
    for RS in [ADD_RS, MUL_RS]:
        for entry in RS.getEntries():
            if entry:                
                it_entry = instructionTable.getEntry(entry._instruction)
                if it_entry.getBusyState() == constants.RunState.EX_START:
                    it_entry.EX_Tick(cycle)

def tryCDBBroadcast():
    for RS in [ADD_RS, MUL_RS]:
        for entry in RS.getEntries():
            if entry:                
                it_entry = instructionTable.getEntry(entry.getInstruction())
                if it_entry.getBusyState() == constants.RunState.EX_END:
                    value = entry.getResult()

                    if value:
                        it_entry.CDB_Write(cycle)
                        
                        robEntry = ROB.updateValue(entry.getInstruction(), value)
                        for RS in [ADD_RS, MUL_RS]:
                            RS.updateEntries(robEntry, value)
                        return

#TODO
def tryCommit():
    entry = ROB.getHead()
    if entry:
        if entry.getValue() != "NA":
            robEntry = ROB.removeEntry()
            RATTable.updateRegister(robEntry.getDestination().getName(), robEntry.getValue(), False, None)

            inst = robEntry.getInstruction()
            instType = inst.disassemble()["command"]

            instructionTable.getEntry(inst).Commit(cycle)
            
            if instType in ["ADD", "SUB"]:
                ADD_RS.removeEntry(inst)
            elif instType in ["MUL", "DIV"]:
                MUL_RS.removeEntry(inst)

def logic_loop():
    global cycle
    cycle += 1
    
    tryCommit()
    tryCDBBroadcast()
    proceedExecuting()
    tryExecute()
    tryDispatch()
    

RUN = False
backwards = 1
historyBuffer = []

GUI = Graphics()
window = GUI.generateWindow()

# Main event loop
while True:
    event, values = window.read(timeout=constants.CYCLE_DURATION)

    if event == sg.WIN_CLOSED:
        break
    elif event == "pause_button":
        if RUN:
            window["pause_button"].update(text="Continue")
        else:
            window["pause_button"].update(text="  Pause  ")
    
        RUN = not RUN

    elif event in ["previous_button", "next_button"] and not RUN:
        if backwards < cycle:
            if event == "previous_button":
                backwards += 1
            elif event == "next_button" and ((cycle - backwards) < len(historyBuffer)):
                backwards -= 1

            index = cycle - backwards

            GUI.updateContents(
                window,
                index + 1,
                historyBuffer[index][0],
                historyBuffer[index][1],
                resStats=historyBuffer[index][2],
                ARF=historyBuffer[index][3],
                RAT=historyBuffer[index][4]
            )
        
    if RUN:
        backwards = 1
        logic_loop()
        
        historyBuffer.append([
            copy.deepcopy(instructionTable),
            copy.deepcopy(ROB),
            {
                constants.ADD_SUB: copy.deepcopy(ADD_RS),
                constants.MUL_DIV: copy.deepcopy(MUL_RS)
            },
            copy.deepcopy(ARFTable),
            copy.deepcopy(RATTable)
        ])
        
        GUI.updateContents(
            window,
            cycle,
            instructionTable,
            ROB,
            resStats={
                constants.ADD_SUB: ADD_RS,
                constants.MUL_DIV: MUL_RS
                },
            ARF=ARFTable,
            RAT=RATTable
        )



window.close()
