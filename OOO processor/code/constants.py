DEBUG = False
GUI_FONTSIZE   = 16
LIMIT          = 10
CYCLE_DURATION = 400

ADD_SUB = "ADD/SUB"
MUL_DIV = "MUL/DIV"
LW = "LW"

NumCycles = {
    "ADD": 1,
    "SUB": 1,
    "MUL": 10,
    "DIV": 40,
    "LW": 5
}


class RunState:
    NOT_STARTED = "NOT STARTED"
    RS          = "RS"
    EX_START    = "EX_STARTED"
    EX_END      = "EX_END"
    CDB         = "CDB"
    COMMIT      = "COMMIT"        
    