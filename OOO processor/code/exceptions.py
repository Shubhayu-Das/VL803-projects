class AlreadyExistsException(Exception):
    def __init__(self, entry, message="Entry already exists: "):
        self._message = message
        super().__init__(self._message + str(entry.getID()))
