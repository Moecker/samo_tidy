import samo_tidy.utils.utils as utils


class Violation:
    def __init__(self, id, message, file_path, line, column):
        self.id = id
        self.message = message
        self.file_path = file_path
        self.file_name = utils.only_filename(self.file_path)
        self.line = line
        self.column = column

    def __repr__(self):
        return {
            "id": self.id,
            "message": self.message,
            "file_name": self.file_name,
            "line": self.line,
            "column": self.column,
        }

    def __str__(self):
        return (
            "Violation(id="
            + self.id
            + ", message="
            + str(self.message)
            + ", file_path="
            + str(self.file_name)
            + ", line="
            + str(self.line)
            + ", column="
            + str(self.column)
            + ")"
        )
