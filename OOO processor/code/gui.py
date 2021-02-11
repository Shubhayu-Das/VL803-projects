import PySimpleGUI as sg


class Graphics():
    def __init__(self):
        pass

    def __generateTable(self, title, data, headings, n_rows=5, hide_vertical_scroll=True):
        row_contents = data["contents"]
        row_colors = list(enumerate(data["colors"]))

        table = sg.Table(
            values=row_contents,
            headings=headings,
            hide_vertical_scroll=hide_vertical_scroll,
            def_col_width=8,
            max_col_width=14,
            justification="center",
            num_rows=n_rows,
            row_colors=row_colors,
            background_color="lightgrey",
            text_color="black"
        )

        return [sg.Frame(
            title=title,
            layout=[[table]],
            title_location=sg.TITLE_LOCATION_TOP
        )]

    def __getTextElement(self, text, fontSize=16):
        return [sg.Text(
            text,
            justification="center",
            pad=((20, 20), (2, 2)),
            font="Times " + str(fontSize),
            text_color="black"
        )]

    def generateLayout(self, machineState):
        mainHeading = self.__getTextElement(
            "Tomasulo out-of-order simulation", 24)

        instructions = machineState["Instruction Table"]
        buffer = machineState["Load Store Buffer"]
        reserv = machineState["Reservation Station"]
        RoB = machineState["RoB"]
        ARF = machineState["ARF"]
        RAT = machineState["RAT"]

        bufferHeading = ["Inst.", "Busy",
                         "Dest Tag", "Address offset", "src reg"]
        instructionsHeading = ["Inst", "Issue",
                               "EX start", "EX end", "write to CDB", "Commit"]
        reservationHeading = ["Type", "Instruction", "Busy", "Dest tag",
                              "src tag1", "src tag2", "val 1", "val 2"]
        robHeading = ["Type", "Dest", "Value"]
        arfHeading = [f" R{i} " for i in range(1, 11)]
        ratHeading = [f" R{i} " for i in range(1, 11)]

        instructionTable = self.__generateTable(
            "Instructions",
            instructions,
            instructionsHeading,
            n_rows=6,
            hide_vertical_scroll=False
        )
        loadStoreBufferTable = self.__generateTable(
            "Load Store Buffer", buffer, bufferHeading)
        reservationStationTable = self.__generateTable(
            "Reservation Station", reserv, reservationHeading)
        RoBTable = self.__generateTable("ROB", RoB, robHeading)
        ARFTable = self.__generateTable("ARF", ARF, arfHeading)
        RATTable = self.__generateTable("RAT", RAT, ratHeading)

        displayLayout = [
            mainHeading,
            [sg.HorizontalSeparator(color="black")],
            instructionTable,
            reservationStationTable + RoBTable,
            loadStoreBufferTable,
            ARFTable + RATTable
        ]

        return displayLayout

    def generateWindow(self, machineState):
        sg.theme('SystemDefault')

        return sg.Window(
            'Tomasulo OOO processor sim',
            self.generateLayout(machineState),
            font='Times 14',
            size=sg.Window.get_screen_size(),
            element_padding=(10, 10),
            margins=(20, 20),
            text_justification="center",
            resizable=True,
            element_justification="center"
        )


if __name__ == "__main__":
    from dummy import insts, sampleResv, sampleRob, buffer, arf, rat

    GUI = Graphics()
    machineState = {
        "Instruction Table": {
            "contents": insts,
            "colors": ["lightgreen", "red", "", "lightyellow"]
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
    window = GUI.generateWindow(machineState)
    event, values = window.read()
