#!/usr/bin/env python3
import PySimpleGUI as sg
from constants import LIMIT, NumCycles, GUI_FONTSIZE


class Graphics():
    def __init__(self, machineState=None):
        if machineState:
            self._machine_state = machineState
        else:
            self._machine_state = {
                "Instruction Table": {
                    "contents": [[""]*6]*5,
                    "colors": []
                },
                "Reservation Station": {
                    "contents": [["ADD/SUB", "", "", "", "", "", "", ""]]*3 + [["MUL/DIV", "", "", "", "", "", "", ""]]*2,
                    "colors": []
                },
                "ROB": {
                    "contents": [[""]*4]*2,
                    "colors": []
                },
                "Load Store Buffer": {
                    "contents": [[""]*5]*2,
                    "colors": []
                },
                "ARF": {
                    "contents": [f" R{i} " for i in range(0, LIMIT)],
                    "colors": []
                },
                "metadata": {
                    "cycle": 0
                }
            }

    def __generateTable(self, title, data, headings, n_rows=5, key="table"):
        row_contents = data["contents"]
        row_colors = list(enumerate(data["colors"]))
        hide_vertical_scroll = True

        if len(row_contents) > n_rows:
            hide_vertical_scroll = False
        
        table = sg.Table(
            values=row_contents,
            headings=headings,
            hide_vertical_scroll=hide_vertical_scroll,
            def_col_width=8,
            row_height=40,
            justification="center",
            num_rows=n_rows,
            row_colors=row_colors,
            alternating_row_color="lightgrey",
            text_color="black",
            key=key
        )

        return [sg.Frame(
            title=title,
            layout=[[table]],
            title_location=sg.TITLE_LOCATION_TOP,
        )]

    def __getTextElement(self, text, fontSize=16, justification="center"):
        return [sg.Text(
            text,
            justification=justification,
            pad=((20, 20), (2, 2)),
            font="Times " + str(fontSize),
            text_color="black"
        )]

    def generateLayout(self):
        mainHeading = self.__getTextElement(
            "Tomasulo out-of-order simulation", 24)


        cycleNumber = [sg.Frame(
            title="Current Cycle",
            layout=[[sg.Text(
            text=self._machine_state["metadata"]["cycle"],
            key="cycle_number",
            size=(3,1),
            text_color="black",
            font=f"Times {GUI_FONTSIZE+2}",
        )]],
            title_location=sg.TITLE_LOCATION_TOP,
            element_justification = "center",
        )]

        instructions = self._machine_state["Instruction Table"]
        buffer = self._machine_state["Load Store Buffer"]
        reserv = self._machine_state["Reservation Station"]
        ROB = self._machine_state["ROB"]
        ARF = self._machine_state["ARF"]
        nCycles = {
            "contents": [[inst, cycles] for inst, cycles in NumCycles.items()],
            "colors": []
        }

        bufferHeading = [" Instruction ", "Busy",
                         "Dest Tag", "Address offset", "src reg"]
        instructionsHeading = ["Instruction", "Issue",
                               "EX start", "EX end", "write to CDB", "Commit"]
        reservationHeading = ["Type", "Instruction", "Busy", "Dest tag",
                              "src tag1", "src tag2", "val 1", "val 2"]
        robHeading = [" Name ", "  Instruction  ", " Dest. ", "  Value  "]
        arfHeading = ["Reg", "   Value   ", "Mapping", "Busy"]
        cycleHeading = ["Instr.", "No. of cycles"]

        instructionTable = self.__generateTable(
            "Instruction Queue",
            instructions,
            instructionsHeading,
            n_rows=7,
            key="inst_table"
        )
        loadStoreBufferTable = self.__generateTable(
            "Load Store Buffer", buffer, bufferHeading, n_rows=2, key="ls_buffer_table")
        reservationStationTable = self.__generateTable(
            "Reservation Station", reserv, reservationHeading, key="reserve_station")
        ROBTable = self.__generateTable("ROB", ROB, robHeading, n_rows=8, key="rob")
        ARFTable = self.__generateTable("ARF", ARF, arfHeading, n_rows=LIMIT, key="arf")
        CycleInfoTable = self.__generateTable("No. of Cycles", nCycles, cycleHeading, n_rows=len(NumCycles),key="num_cycles")

        pauseButton = [sg.Button(
            button_text="  Start  ",
            key="pause_button"
        )]

        nextButton = [sg.Button(
            button_text="Next",
            key="next_button"
        )]

        prevButton = [sg.Button(
            button_text="Prev",
            key="previous_button"
        )]

        controlPanel = [sg.Frame(
            title="Control Panel",
            layout=[pauseButton, nextButton + prevButton],
            title_location=sg.TITLE_LOCATION_TOP
        )]

        col1 = [sg.Column(
            [cycleNumber, CycleInfoTable, controlPanel],
            key="layout_col1"
        )]

        col2 = [sg.Column(
            [instructionTable, [sg.Column([loadStoreBufferTable, reservationStationTable])]],
            grab=True,
            element_justification="center",
            key="layout_col2"
        )]

        col3 = [sg.Column(
            [ARFTable, ROBTable],
            grab=True,
            element_justification="center",
            expand_x=True,
            key="layout_col3"
        )]
        
        displayLayout = [
            mainHeading,
            [sg.HorizontalSeparator(color="black")],
            col1 + col2 + col3
        ]

        return displayLayout

    def generateWindow(self):
        sg.theme('Material2')

        return sg.Window(
            'Tomasulo OOO processor sim',
            self.generateLayout(),
            font=f"Times {GUI_FONTSIZE}",
            size=sg.Window.get_screen_size(),
            element_padding=(10, 10),
            margins=(20, 20),
            text_justification="center",
            resizable=True,
            element_justification="center",
        ).finalize()

    def __convertInstructionTable(self, instructionTable):
        insts = []
        colors = []
        for entry in instructionTable._entries:
            data = []
            
            data.append(entry._instruction.strDisassembled())
            data.append(str(entry._rs_issue_cycle))
            data.append(str(entry._exec_start))
            data.append(str(entry._exec_complete))
            data.append(str(entry._cdb_write))
            data.append(str(entry._commit))

            insts.append(data)
            colors.append("")

        self._machine_state["Instruction Table"]["contents"] = insts
        self._machine_state["Instruction Table"]["colors"] = colors

    def __convertARF(self, ARFTable):
        insts = []
        colors = []

        for register in list(ARFTable.getEntries().values())[:LIMIT]:
            data = []

            data.append(register.getName())
            data.append(register.getValue())
            data.append(register.getLink() if register.getLink() else "-")
            data.append(str(register.isBusy())[0])

            insts.append(data)
            colors.append("")

        self._machine_state["ARF"]["contents"] = insts
        self._machine_state["ARF"]["colors"] = colors

    def __convertROB(self, rob):
        insts = []
        colors = []
        for name, entry in rob.getEntries().items():
            data = []
            if entry == None:
                data = [name] + [""] * 3
            else:
                data.append(name)
                data.append(entry.getInstruction().strDisassembled())
                data.append(entry.getDestination().getName())
                data.append(entry.getValue())

            insts.append(data)
            colors.append("")

        self._machine_state["ROB"]["contents"] = insts
        self._machine_state["ROB"]["colors"] = colors

    def __convertReservationStation(self, resStats):
        insts = []
        colors = []
        for name, resStat in resStats.items():
            for entry in resStat._buffer:
                data = []
                if entry:
                    data.append(name)
                    data.append(entry._instruction.strDisassembled())
                    
                    data.append(str(entry._busy)[0])
                    data.append(entry._dest)

                    data.append(entry._src_tag1)
                    data.append(entry._src_tag2)
                    
                    data.append(str(entry._src_val1))
                    data.append(str(entry._src_val2))
                else:
                    data = [name] + [""] * 7
                    data[2] = False

                insts.append(data)
                colors.append("")

        self._machine_state["Reservation Station"]["contents"] = insts
        self._machine_state["Reservation Station"]["colors"] = colors

    def __convertLSBuffer(self, LW_SW):
        insts = []
        colors = []
        for entry in LW_SW.getEntries():
            data = []
            if entry:
                data.append(entry.getInstruction().strDisassembled())
                
                data.append(str(entry.isBusy())[0])
                data.append(entry._dest)

                data.append(f"{4*entry._offset}+{entry._src_reg.getName()}")
                data.append(entry._src_reg.getName())

            else:
                data = [""] * 5

            insts.append(data)
            colors.append("")

        self._machine_state["Load Store Buffer"]["contents"] = insts
        self._machine_state["Load Store Buffer"]["colors"] = colors

    def updateContents(self, window, cycle, instructionTable=None, ROB=None, resStats=None, ARF=None, LS_Buffer=None):
        self._machine_state["metadata"]["cycle"] = cycle
        window["cycle_number"].update(value=self._machine_state["metadata"]["cycle"])

        if instructionTable:
            self.__convertInstructionTable(instructionTable)
            window['inst_table'].update(self._machine_state["Instruction Table"]["contents"])
        
        if ROB:
            self.__convertROB(ROB)
            window['rob'].update(self._machine_state["ROB"]["contents"])

        if resStats:
            self.__convertReservationStation(resStats)
            window['reserve_station'].update(self._machine_state["Reservation Station"]["contents"])

        if ARF:
            self.__convertARF(ARF)
            window['arf'].update(self._machine_state["ARF"]["contents"])

        if LS_Buffer:
            self.__convertLSBuffer(LS_Buffer)
            window['ls_buffer_table'].update(self._machine_state["Load Store Buffer"]["contents"])
        

if __name__ == "__main__":

    GUI = Graphics()

    window = GUI.generateWindow()

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
    window.close()
