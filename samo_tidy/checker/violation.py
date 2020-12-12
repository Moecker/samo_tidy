class Violation:
    def __init__(self, id, file, line, column):
        self.id = id
        self.file = file
        self.line = line
        self.column = column

    def __repr__(self):
        return {"id": self.id, "file": self.file, "line": self.line, "column": self.column}

    def __str__(self):
        return (
            "Violation(id="
            + self.id
            + ", file="
            + str(self.file)
            + ", line="
            + str(self.line)
            + ", column="
            + str(self.column)
            + ")"
        )
