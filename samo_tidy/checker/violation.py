import samo_tidy.utils.utils as utils


class Violation:
    """Represents a violation"""

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
            f"(Violation("
            f"id={self.id}, "
            f"message={self.message}, "
            f"file_name={str(utils.make_link(self.file_path))}, "
            f"line={str(self.line)}, "
            f"column={str(self.column)}"
            f")"
        )

    def limit_message(self):
        return "{self.message: 1.50}"

    def file_path_link(self):
        return f"file://{self.file_path}"

    def style(self):
        return f"{self.id}:{self.file_name}:{self.line}:{self.column}"
