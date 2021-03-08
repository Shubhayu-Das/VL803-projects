from collections import defaultdict
from random import randint


class Register:
    def __init__(self, name, value, busy):
        self._name = name
        self._value = value
        self._busy = busy

    def __str__(self):
        return f"[{'BUSY' if self._busy else 'FREE'}] {self._name}: {self._busy}"

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

    def setValue(self, new_val):
        self._value = new_val

    def setState(self, busy):
        self._busy = busy

    def isBusy(self):
        return self._busy


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

    def __str__(self):
        return f"<Register Bank {self._name} of size: {len(self._bank)}>"