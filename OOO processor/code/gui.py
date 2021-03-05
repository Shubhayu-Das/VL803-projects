#!/usr/bin/env python3
import PySimpleGUI as sg
from dummy import insts, sampleResv, sampleRob, buffer, arf, rat
from constants import LIMIT


class Graphics():
    def __init__(self, machineState=False):
        if machineState:
            self._machine_state = machineState
        else:
            self._machine_state = {
                "Instruction Table": {
                    "contents": insts,
                    "colors": ["lightgreen", "orange", "", "lightyellow"]
                },
                "Reservation Station": {
                    "contents": sampleResv,
                    "colors": []
                },
                "ROB": {
                    "contents": sampleRob,
                    "colors": []
                },
                "Load Store Buffer": {
                    "contents": buffer,
                    "colors": ["lightgreen"]
                },
                "ARF": {
                    "contents": arf,
                    "colors": []
                },
                "RAT": {
                    "contents": rat,
                    "colors": []
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

    def __getTextElement(self, text, fontSize=16):
        return [sg.Text(
            text,
            justification="center",
            pad=((20, 20), (2, 2)),
            font="Times " + str(fontSize),
            text_color="black"
        )]

    def generateLayout(self):
        mainHeading = self.__getTextElement(
            "Tomasulo out-of-order simulation", 24)

        instructions = self._machine_state["Instruction Table"]
        buffer = self._machine_state["Load Store Buffer"]
        reserv = self._machine_state["Reservation Station"]
        ROB = self._machine_state["ROB"]
        ARF = self._machine_state["ARF"]
        RAT = self._machine_state["RAT"]

        bufferHeading = ["Inst.", "Busy",
                         "Dest Tag", "Address offset", "src reg"]
        instructionsHeading = ["Inst", "Issue",
                               "EX start", "EX end", "write to CDB", "Commit"]
        reservationHeading = ["Type", "Instruction", "Busy", "Dest tag",
                              "src tag1", "src tag2", "val 1", "val 2"]
        robHeading = [" Name ", "  Instruction  ", "Dest.", "Value"]
        arfHeading = [f" R{i} " for i in range(0, LIMIT)]
        ratHeading = [f" R{i} " for i in range(0, LIMIT)]

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
        ARFTable = self.__generateTable("ARF", ARF, arfHeading, n_rows=1, key="arf")
        RATTable = self.__generateTable("RAT", RAT, ratHeading, n_rows=1,key="rat")

        displayLayout = [
            mainHeading,
            [sg.HorizontalSeparator(color="black")],
            instructionTable + ROBTable,
            reservationStationTable + loadStoreBufferTable,
            ARFTable + RATTable
        ]

        return displayLayout

    def generateWindow(self):
        sg.theme('Material2')

        return sg.Window(
            'Tomasulo OOO processor sim',
            self.generateLayout(),
            font='Times 14',
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
        data = []
        colors = []

        for register in list(ARFTable.getEntries().values())[:LIMIT]:
            data.append(register.getDisplay())
            colors.append("")

        self._machine_state["ARF"]["contents"] = [data]
        self._machine_state["ARF"]["colors"] = colors

    def __convertRAT(self, RATTable):
        data = []
        colors = []

        for register in list(RATTable.getEntries().values())[:LIMIT]:
            data.append(register.getDisplay())
            colors.append("")

        self._machine_state["RAT"]["contents"] = [data]
        self._machine_state["RAT"]["colors"] = colors


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
                    data.append(str(entry._busy))
                    data.append(entry._dest.getName())

                    if isinstance(entry._src_val1, str):
                        data.append(entry._src_tag1.getDisplay())
                    else:
                        data.append(entry._src_tag1)

                    if isinstance(entry._src_val2, str):
                        data.append(entry._src_tag2.getDisplay())
                    else:
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

    def updateContents(self, window, instructionTable=None, ROB=None, resStats=None, ARF=None, RAT=None):
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

        if RAT:
            self.__convertRAT(RAT)
            window['rat'].update(self._machine_state["RAT"]["contents"])
        


if __name__ == "__main__":

    GUI = Graphics()

    window = GUI.generateWindow()

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
    window.close()
