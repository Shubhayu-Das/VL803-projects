from register_bank import Register, RegisterBank


class ARFRegister(Register):
    def __init__(self, name="", val=0, busy=True, link=None):
        super(ARFRegister, self).__init__(name, val, busy)
        self._link = link

    def setLink(self, new_link):
        self._link = new_link
        if new_link:
            self.setState(True)
        else:
            self.setState(False)
    
    def getLink(self):
        return self._link

    def getSource(self):
        if self._link:
            return self._link
        else:
            return f"ARF.{self._name}"

    def getDisplay(self):
        if self._link:
            return self._link.getName()
        else:
            return self._value

    def __str__(self):
        return f"[{'BUSY' if self._busy else 'FREE'}] ARF.{self.getName()}-> {self._link}"


class ARF(RegisterBank):
    def __init__(self, size=32):
        super(ARF, self).__init__("ARF", size, unit=ARFRegister, init=[12, 16, 45, 5, 3, 4, 1 ,2, 2, 3])

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
    arf = ARF()
    print(f"Decoded register: {arf.getRegister('00100')}")
    arf.updateRegister("R4", 10, True, "RAT.R2")

    print(arf.getRegister("R4"))

    # from rat import RAT
