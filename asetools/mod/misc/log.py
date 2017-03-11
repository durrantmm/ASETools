import logging, os, sys

msg_checking_version = "Ensuring that {NAME} is version {VERSION}..."
msg_starting_run = "Starting to run {NAME}..."
msg_executing_command = "Executing the command:{DELIM}{COMMAND}"
msg_saving_run_info = "Saving run info to {PATH}"


class Log:

    def __init__(self, outdir):
        format_str = "%(levelname)s %(asctime)s:\t%(message)s"
        logformat = logging.Formatter(format_str)

        logging.basicConfig(level=logging.INFO, format=format_str)
        self.rootLogger = logging.getLogger()

        fileHandler = logging.FileHandler("{0}/{1}.log".format(outdir, os.path.basename(outdir)))
        fileHandler.setFormatter(logformat)
        self.rootLogger.addHandler(fileHandler)

    def info(self, s):
        self.rootLogger.info(s)

    def error(self, s):
        self.rootLogger.error(s)

    def debug(self, s):
        self.rootLogger.debug(s)

    def warning(self, s):
        self.rootLogger.warning(s)

    @classmethod
    def info_chk(cls, log, msg):
        if log:
            log.info(msg)

    @classmethod
    def error_chk(cls, log, msg):
        if log:
            log.info(msg)

    @classmethod
    def debug_chk(cls, log, msg):
        if log:
            log.debug(msg)

    @classmethod
    def warning_chk(cls, log, msg):
        if log:
            log.warning(msg)


class SimpleLog:
    def __init__(self):
        format_str = "%(levelname)s %(asctime)s:\t%(message)s"
        logformat = logging.Formatter(format_str)

        logging.basicConfig(level=logging.DEBUG, format=format_str)
        self.rootLogger = logging.getLogger()

    def info(self, s):
        self.rootLogger.info(s)

    def error(self, s):
        self.rootLogger.error(s)

    def debug(self, s):
        self.rootLogger.debug(s)

    def warning(self, s):
        self.rootLogger.warning(s)

    @classmethod
    def info_chk(cls, log, msg):
        if log:
            log.info(msg)

    @classmethod
    def error_chk(cls, log, msg):
        if log:
            log.info(msg)

    @classmethod
    def debug_chk(cls, log, msg):
        if log:
            log.debug(msg)

    @classmethod
    def warning_chk(cls, log, msg):
        if log:
            log.warning(msg)
