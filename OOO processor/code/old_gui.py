#!/usr/bin/env python3
import PySimpleGUI as sg
from dummy import insts, sampleResv, sampleRob, buffer, arf, rat


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
                "RoB": {
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
        
        n_rows = min(n_rows, len(row_contents))

        table = sg.Table(
            values=row_contents,
            headings=headings,
            hide_vertical_scroll=hide_vertical_scroll,
            def_col_width=8,
            max_col_width=14,
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
            key=key+"_frame"
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
        RoB = self._machine_state["RoB"]
        ARF = self._machine_state["ARF"]
        RAT = self._machine_state["RAT"]

        bufferHeading = ["Inst.", "Busy",
                         "Dest Tag", "Address offset", "src reg"]
        instructionsHeading = ["Inst", "Issue",
                               "EX start", "EX end", "write to CDB", "Commit"]
        reservationHeading = ["Type", "Instruction", "Busy", "Dest tag",
                              "src tag1", "src tag2", "val 1", "val 2"]
        robHeading = ["Type", "Dest", "Value"]
        arfHeading = [f" R{i} " for i in range(1, 11)]
        ratHeading = [f" R{i} " for i in range(1, 11)]

        self.instructionTable = self.__generateTable(
            "Instruction Queue",
            instructions,
            instructionsHeading,
            n_rows=6,
            key="inst_table"
        )
        self.loadStoreBufferTable = self.__generateTable(
            "Load Store Buffer", buffer, bufferHeading, key="ls_buffer_table")
        self.reservationStationTable = self.__generateTable(
            "Reservation Station", reserv, reservationHeading)
        self.RoBTable = self.__generateTable("ROB", RoB, robHeading)
        self.ARFTable = self.__generateTable("ARF", ARF, arfHeading)
        self.RATTable = self.__generateTable("RAT", RAT, ratHeading)

        displayLayout = [
            mainHeading,
            [sg.HorizontalSeparator(color="black")],
            self.instructionTable,
            self.reservationStationTable + self.RoBTable,
            self.loadStoreBufferTable,
            self.ARFTable + self.RATTable
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
        for entry in instructionTable._entries:
            data = []
            instruction = entry._instruction.disassemble()
            if "offset" in instruction.keys():
                last = instruction["offset"] 
            else:
                last = instruction["rs2"]
            
            data.append(f"{instruction['command']} {instruction['rd']}, {instruction['rs1']}, {last}")
            data.append(str(entry._rs_issue_cycle))
            data.append(str(entry._exec_start))
            data.append(str(entry._exec_complete))
            data.append(str(entry._cdb_write))
            data.append(str(entry._commit))

            insts.append(data)

        self._machine_state["Instruction Table"]["contents"] = insts

    def updateContents(self, window, instructionTable):
        self.__convertInstructionTable(instructionTable)
        window['inst_table_frame'].update(self._machine_state["Instruction Table"]["contents"])


if __name__ == "__main__":

    GUI = Graphics()

    window = GUI.generateWindow()
    event, values = window.read()
