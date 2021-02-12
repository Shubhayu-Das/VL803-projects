class Register:
    def __init__(self, val=0, name="", valid=True, link=None):
        self._name = int(name, 2)
        self._value = val
        self._valid = valid
        self._link = link

    def getReg(self):
        if self._valid:
            return self
        else:
            return self._link.getReg()
    
    def link(self, link):
        self._valid = False
        self._link = link

    def unlink(self):
        self._value = self.getValue()
        self._valid = True
        self._link = None

    def getValue(self):
        if self._valid:
            return self._value
        else:
            return self._link.getValue()

    def setValue(self, val):
        if self._valid:
            self._value = val
        else:
            self._link.setValue(val)


    def __str__(self):
        return f"R{self._name}"
