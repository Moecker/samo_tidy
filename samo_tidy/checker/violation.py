class Violation:
    def __init__(self, id, message, file, line, column):
        self.id = id
        self.message = message
        self.file = file
        self.line = line
        self.column = column

    def __repr__(self):
        return {"id": self.id, "message": self.message, "file": self.file, "line": self.line, "column": self.column}

    def __str__(self):
        return (
            "Violation(id="
            + self.id
            + ", message="
            + str(self.message)
            + ", file="
            + str(self.file)
            + ", line="
            + str(self.line)
            + ", column="
            + str(self.column)
            + ")"
        )
