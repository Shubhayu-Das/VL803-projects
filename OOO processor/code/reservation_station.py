from exceptions import AlreadyExistsException


class ReservationStationEntry:
    def __init__(self, id=None, instr="", busy=False, dest="",
                 src_tag1="", src_tag2="", src_val1="", src_val2=""):
        self._id = id
        self._instruction = instr
        self._busy = busy
        self._dest = dest
        self._src_tag1 = src_tag1
        self._src_tag2 = src_tag2
        self._src_val1 = src_val1
        self._src_val2 = src_val2

    def toggleState(self):
        self._busy = not self._busy

    def getID(self):
        return self._id

    def isBusy(self):
        return self._busy

    def destination(self):
        return self._dest

    def __str__(self):
        return f"""ReservationStationEntry:
                    Instruction: {self._instruction}
                    Busy State: {self._busy}
                    Destination: {self._dest}
                    Source Tag 1: {self._src_tag1}
                    Source Tag 2: {self._src_tag2}
                    Source Value 1: {self._src_val1}
                    Source Value 2: {self._src_val2}
                """


class ReservationStation:
    def __init__(self, datatype, size):
        self._type = datatype
        self._busy_flag = False
        self._size = size
        self._buffer = [ReservationStationEntry() for _ in range(size)]
        self._next_index = 0

    def __updateFreeIndex(self):
        self._next_index = (self._next_index + 1) % (self._size)
        self._busy_flag = False
        counter = 0

        while(self._buffer[self._next_index].isBusy()
                and counter < self._size):
            self._next_index = (self._next_index + 1) % (self._size)
            counter += 1

        if counter == self._size:
            self._busy_flag = True
            self._next_index = -1

    def __isValidID(self, id, newEntry=False):
        for entry in self._buffer:
            if id == entry.getID():
                return False if newEntry else True

        return True if newEntry else False

    def __getIndexFromID(self, id):
        counter = 0

        while counter < self._size:
            if self._buffer[counter].getID() == id:
                return counter
            counter += 1

        return False

    def addEntry(self, entry):
        if self._busy_flag:
            return self._busy_flag

        if self.__isValidID(entry.getID(), newEntry=True):
            self._buffer[self._next_index] = entry
            print(f"Added entry {entry.getID()}")
            self.__updateFreeIndex()
        else:
            raise AlreadyExistsException(entry)

    def removeEntry(self, entry):
        id = entry.getID()
        if self.__isValidID(id):
            self._buffer[self.__getIndexFromID(id)] = ReservationStationEntry()

            if self._busy_flag:
                self.__updateFreeIndex()

    def getBusyState(self):
        return self._busy_flag

    def __str__(self):
        return f"""Reservation Station for {self._type}.
                    Station Size: {self._size}
                    Busy State: {self.getBusyState()}
                    Next Index: {self._next_index}"""


if __name__ == "__main__":
    obj = ReservationStationEntry(
        1, "ADD", True, "ROB1", "R1", "R2", "10", "20")
    obj1 = ReservationStationEntry(
        2, "SUB", True, "ROB1", "R3", "R2", "10", "20")
    obj2 = ReservationStationEntry(
        3, "SUB", True, "ROB1", "R3", "R2", "10", "20")
    obj3 = ReservationStationEntry(
        4, "SUB", True, "ROB1", "R3", "R2", "10", "20")

    from constants import ADD_SUB

    addResvStation = ReservationStation(ADD_SUB, 3)

    for entry in [obj, obj1, obj, obj2, obj3]:
        try:
            print(addResvStation.addEntry(entry))
            if entry == obj2:
                addResvStation.removeEntry(obj2)
        except AlreadyExistsException:
            print(f"Entry already exists: {entry.getID()}")
