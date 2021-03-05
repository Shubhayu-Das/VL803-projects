from register_bank import Register, RegisterBank


class RATRegister(Register):
    def __init__(self, name="", val=0, busy=True, link=None):
        super(RATRegister, self).__init__(name, val, busy)
        self._link = link

    def setLink(self, new_link):
        self._link = new_link
    
    def getLink(self):
        return self._link

    def getSource(self):
        if self._link:
            return self._link
        else:
            return f"RAT.{self._name}"

    def getDisplay(self):
        if self._link:
            return self._link
        else:
            return self._value

    def __str__(self):
        return f"[{'BUSY' if self._busy else 'FREE'}] RAT.{self._name}: {self._value}"


class RAT(RegisterBank):
    def __init__(self, size=32):
        super(RAT, self).__init__("RAT", size, unit=RATRegister)
        self._size = size
        self._index = 0
        self._is_full = False

    def __updateFreeIndex(self):
        counter = 0
        while(counter < self._size):
            self._index = (self._index + 1) % self._size
            if not self._bank[f"R{self._index}"].isBusy():
                break
            counter += 1

        if counter == self._size:
            self._is_full = True
            self._index = -1
        else:
            self._is_full = False

    def getBusyState(self):
        return self._is_full
    
    def addEntry(self, arf_reg):
        if self._is_full:
            return False

        idx = f"R{self._index}"
        self._bank[idx].setValue(arf_reg.getValue())
        previous = self._bank[idx]

        self.__updateFreeIndex()

        return previous

    def getRegister(self, bin_tag):
        bin_tag = bin_tag.upper()

        if bin_tag[0] == 'R':
            return self._bank[bin_tag]
        else:
            return self._bank[f"R{int(bin_tag, 2)}"]


    def updateRegister(self, name, value, busyState, mapping):
        name = name.upper()

        if name[0] != 'R':
            name = f"R{int(bin_tag, 2)}"

        self._bank[name].setValue(value)
        self._bank[name].setState(busy=busyState)
        self._bank[name].setLink(mapping)


if __name__ == "__main__":
    rat = RAT()
    print(f"Decoded register: {rat.getRegister('00100')}")
    # rat.updateRegister("R4", 10, True, "RAT.R2")

    print(rat.getRegister("R4").getValue())
