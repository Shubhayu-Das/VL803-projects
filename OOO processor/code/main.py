'''
MIT Licensed by Shubhayu Das, copyright 2021

Developed for Processor Architecture course assignment 1 - Tomasulo Out-Of-Order Machine

This file contains the main logic, that combines individual blocks into a cohesive whole
'''

import os
import sys
import copy
import PySimpleGUI as sg

# Import all the functional components
from register_bank import RegisterBank as ARF
from instruction import Instruction
from reservation_station import ReservationStation, ReservationStationEntry
from instruction_table import InstructionTable, InstructionTableEntry
from ls_buffer import LoadStoreBuffer
from rob import ROBTable

# Import the other custom components
import constants
from gui import Graphics


# Load in the program, if no program file is provided
if len(sys.argv) < 2 or not os.path.exists(sys.argv[2]):
    program_src = "build/riscv_program.elf"
else:
    program_src = sys.argv[2]

# Choose a data sourse
if len(sys.argv) < 3 or not os.path.exists(sys.argv[3]):
    data_mem_src = "data_memory.dat"
else:
    data_mem_src = sys.argv[3]


# Global variables that are needed throughout here
instructions = []
PC = 0
next_event = False

# Creating objects of the functional components
ARFTable = ARF(size=10, init=[12, 16, 45, 5, 3, 4, 1, 2, 2, 3])

ADD_RS = ReservationStation(constants.ADD_SUB, size=3)
MUL_RS = ReservationStation(constants.MUL_DIV, size=2)

LS_Buffer = LoadStoreBuffer(size=3, memoryFile=data_mem_src)
ROB = ROBTable(size=8)


# Load in the program and create the instruction table accordingly
# The instruction table is NOT a functional component of the Tomasulo machine
with open(program_src) as binary:
    program = binary.readlines()
    program = [inst.strip() for inst in program]

    for local_PC, inst in enumerate(program):
        instructions.append(Instruction.segment(inst, PC=local_PC+1))

instructionTable = InstructionTable(size=min(10, len(instructions)))

for instruction in instructions:
    instructionTable.add_entry(instruction)


#-------------------------------------------------------------------------------#
# Functions to implement each stage of the pipeline
#-------------------------------------------------------------------------------#


# Function to try and dispatch next instruction if corresponding RS is free
# Updates all relevant source mappings too
def tryDispatch():
    global next_event
    for it_entry in instructionTable.get_entries():
        if it_entry.get_state() == constants.RunState.NOT_STARTED:
            instruction = it_entry.get_inst()
            instruction_type = instruction.disassemble()["command"]

            RS = None

            if instruction_type in ["ADD", "SUB"]:
                RS = ADD_RS
            elif instruction_type in ["MUL", "DIV"]:
                RS = MUL_RS
            elif instruction_type in ["LW", "SW"]:
                RS = LS_Buffer

            if RS:
                if not RS.is_busy():
                    if RS.add_entry(instruction, ARFTable):
                        destination = ARFTable.get_register(it_entry._instruction.rd)
                        destination.set_link(ROB.add_entry(it_entry._instruction, destination))

                        it_entry.rs_issue(PC)
                        next_event = True

                    break


# Function to simulate the execution of the process. This includes dispatching
# instructions and handling their execution steps
def tryExecute():
    global next_event
    for RS in [LS_Buffer, ADD_RS, MUL_RS]:
        for rs_entry in RS.get_entries():
            if rs_entry:
                it_entry = instructionTable.get_entry(rs_entry._instruction)

                if it_entry.get_state() == constants.RunState.RS and rs_entry.is_executeable():                    
                    it_entry.ex_start(PC)
                    it_entry.update_result(rs_entry.get_result())
                    RS.remove_entry(rs_entry.get_inst())

                    next_event = True
                    break

    for it_entry in instructionTable.get_entries():
        if it_entry.get_state() == constants.RunState.EX_START:
            it_entry.ex_tick(PC)


# Function to perform the CDB broadcast, when an instruction has completed executing
def tryCDBBroadcast():
    global next_event
    for it_entry in instructionTable.get_entries():
        if it_entry.get_state() == constants.RunState.EX_END:
            it_entry.cdb_write(PC)
            
            value = it_entry.get_result()
            robEntry = ROB.update_value(it_entry.get_inst(), value)

            if robEntry:
                for RS in [ADD_RS, MUL_RS]:
                    RS.updateEntries(ARFTable, robEntry)

            next_event = True
            return


# Function to commit the result of an instruction, if it has completed CDB broadcast
# and is at the tail of the ROB
def tryCommit():
    global next_event
    for it_entry in instructionTable.get_entries():
        if it_entry.get_state() == constants.RunState.COMMIT:
            continue
        elif it_entry.get_state() == constants.RunState.CDB:
            robEntry = ROB.remove_entry()
            if robEntry:
                it_entry.commit(PC)
                ARFTable.update_register(robEntry)

            next_event = True
        break


# Function to call all the above function, while updating the program counter
def logic_loop():
    global PC, ADD_RS, MUL_RS, instructionTable, ROB, ARFTable, LS_Buffer, next_event
    PC += 1
    
    if constants.DEBUG:
        print(PC)
    
    # Execute each of the steps in reverse-pipeline order
    # The reverse order is to make sure that the previous instruction completes its stages
    tryCommit()
    tryCDBBroadcast()
    tryExecute()
    tryDispatch()

    # Update the changes into the history buffer
    historyBuffer.append([
        copy.deepcopy(instructionTable),
        copy.deepcopy(ROB),
        {
            constants.ADD_SUB: copy.deepcopy(ADD_RS),
            constants.MUL_DIV: copy.deepcopy(MUL_RS)
        },
        copy.deepcopy(ARFTable),
        copy.deepcopy(LS_Buffer),
        copy.deepcopy(next_event)
    ])
    

#-------------------------------------------------------------------------------#
# GUI related things, with event loop, which updates the processor in every clock PC
#-------------------------------------------------------------------------------#

RUN = False
backwards = 0
historyBuffer = []
frameDuration = constants.CYCLE_DURATION

GUI = Graphics()
window = GUI.generateWindow()

# Main event loop
while True:
    event, values = window.read(timeout=frameDuration)
    done = False

    if event == sg.WIN_CLOSED:
        break

    elif event == "About":
        RUN = False
        window["pause_button"].update(text="Continue")

        GUI.generateAboutPopup()

    elif event == "Instructions":
        RUN = False
        window["pause_button"].update(text="Continue")

        GUI.generateInstructionPopup()

    elif event == "pause_button":
        if RUN:
            window["pause_button"].update(text="Continue")
        else:
            window["pause_button"].update(text="  Pause  ")
    
        RUN = not RUN

    elif event in ["previous_button", "next_button"] and not RUN:

        if backwards < PC and event == "previous_button":
            backwards += 1
        if backwards < PC and event == "next_button":
            backwards -= 1

        index = PC - backwards

        if index < len(historyBuffer) and index != 0:
            GUI.updateContents(
                window,
                index + 1,
                historyBuffer[index][0],
                historyBuffer[index][1],
                resStats=historyBuffer[index][2],
                ARF=historyBuffer[index][3],
                LS_Buffer=historyBuffer[index][4]
            )

            done = True

    elif event == "next_event_button":
        if RUN:
            while not next_event:
                logic_loop()
            next_event = False
      
    if RUN or (not RUN and not done and event in ["next_button", "next_event_button"]):
        # Reset the history/step controls
        if backwards > 1:
            index = PC - backwards

            if event == "next_event_button":
                while not historyBuffer[index][5]:
                    backwards -= 1
                    index = PC - backwards

            GUI.updateContents(
                window,
                index + 1,
                historyBuffer[index][0],
                historyBuffer[index][1],
                resStats=historyBuffer[index][2],
                ARF=historyBuffer[index][3],
                LS_Buffer=historyBuffer[index][4]
            )

            backwards -= 1

        else:
            if event == "next_event_button":
                while not next_event:
                    logic_loop()
                next_event = False
            
            # Run the processor for one clock cycle
            logic_loop()
            
            # Render the contents to the GUI
            GUI.updateContents(
                window,
                PC,
                instructionTable,
                ROB,
                {
                    constants.ADD_SUB: ADD_RS,
                    constants.MUL_DIV: MUL_RS
                },
                ARFTable,
                LS_Buffer
            )

window.close()