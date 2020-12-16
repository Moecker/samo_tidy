import logging


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return "[%s] %s" % (self.prefix, msg), kwargs


def setup_logger(loglevel, log_file=None):
    the_logger = logging.getLogger()

    if loglevel:
        level = getattr(logging, loglevel.upper(), None)
        if not isinstance(level, int):
            raise ValueError("Invalid log level: %s" % loglevel)
    else:
        level = logging.INFO

    formater = logging.Formatter("[%(levelname)-10.10s] %(message)s")
    the_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formater)
    the_logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(
            log_file,
            "w",
        )
        file_handler.setFormatter(formater)
        the_logger.addHandler(file_handler)
