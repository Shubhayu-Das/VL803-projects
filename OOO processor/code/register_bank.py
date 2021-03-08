from collections import defaultdict
from random import randint


class Register:
    def __init__(self, name, value, busy=False, link=None):
        self._name = name
        self._value = value
        self._busy = busy
        self._link = link

    def __str__(self):
        return f"[{'BUSY' if self._busy else 'FREE'}] {self._name}: {self._busy}"

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def getLink(self):
        return self._link
    
    def isBusy(self):
        return self._busy

    def setValue(self, new_val):
        self._value = new_val

    def setState(self, busy):
        self._busy = busy

    def setLink(self, link):
        self._link = link
        if link:
            self._busy = True
        else:
            self._busy = False

    def __str__(self):
        return f"<[{self._busy}] Register {self._name}: {self._value}>"


class RegisterBank:
    def __init__(self, name="", size=1, unit=Register, init="random"):
        self._name = name
        self._bank = defaultdict(None, {})

        if init == "random":
            init = [randint(1, 101)]*size
    
        for i in range(0, size):
            self._bank.update({f"R{i}": unit(f"R{i}", init[i], False)})

    def getRegister(self, name):
        return self._bank[name]

    def getEntries(self):
        return self._bank

    def updateRegister(self, robEntry):
        name = robEntry.getDestination().getName()

        self._bank[name].setValue(robEntry.getValue())

        if self._bank[name].getLink() == robEntry.getName():
            self._bank[name].setLink(None)

    def __str__(self):
        return f"<Register Bank {self._name} of size: {len(self._bank)}>"