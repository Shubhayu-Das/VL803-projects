DEBUG = False
LIMIT          = 10
CYCLE_DURATION = 150

NumCycles = {
    "ADD": 1,
    "SUB": 1,
    "MUL": 6,
    "DIV": 10,
    "LW": 5
}

class RunState:
    NOT_STARTED = "NOT STARTED"
    RS          = "RS"
    EX_START    = "EX_STARTED"
    EX_END      = "EX_END"
    CDB         = "CDB"
    COMMIT      = "COMMIT"        
    

ADD_SUB = "ADD/SUB"
MUL_DIV = "MUL/DIV"
LW = "LW"