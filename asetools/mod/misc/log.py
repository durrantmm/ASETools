"""
This is a module that handles all of the logging for ASETools
It provides two types of logging classes: Log and SimpleLog
Log will log to both an output file and to the user's terminal
SimpleLog will only log to the user's terminal

"""

import logging
import os

# Here are some strings that are used to log recurring events
msg_checking_version = "Ensuring that {NAME} is version {VERSION}..."
msg_starting_run = "Running {NAME}..."
msg_executing_command = "Executing the command:{DELIM}{COMMAND}"
msg_saving_run_info = "Saving run info to {PATH}"
msg_check_version_signature = "stderr={STDERR}, ignore_error={IGNORE_E}, pass_version_to_parser={PVTP}"
msg_execute_command_signature = "stderr={STDERR}, subprocess={SHELL}"


class Log:
    """
    A class that acts as a wrapper for the logging module.
    It simplifies the creation of a log.
    It logs to the console and to a specified file.
    """
    def __init__(self, outdir):
        """
        This is the constructor for a Log instance.
        :param outdir: The specified output directory where logging will occur.
        """
        format_str = "%(levelname)s %(asctime)s:\t%(message)s"
        logformat = logging.Formatter(format_str)

        logging.basicConfig(level=logging.INFO, format=format_str)
        self.rootLogger = logging.getLogger()

        fileHandler = logging.FileHandler("{0}/asetools.{1}.log".format(outdir, os.path.basename(outdir)))
        fileHandler.setFormatter(logformat)
        self.rootLogger.addHandler(fileHandler)

    def info(self, s):
        """Log at info level."""
        self.rootLogger.info(s)

    def error(self, s):
        """Log at error level."""
        self.rootLogger.error(s)

    def debug(self, s):
        """Log at debug level."""
        self.rootLogger.debug(s)

    def warning(self, s):
        """Log at warning level."""
        self.rootLogger.warning(s)

    @classmethod
    def info_chk(cls, log, msg):
        """Safely log info."""
        if log:
            log.info(msg)

    @classmethod
    def error_chk(cls, log, msg):
        """Safely log an error."""
        if log:
            log.info(msg)

    @classmethod
    def debug_chk(cls, log, msg):
        """Safely log debug."""
        if log:
            log.debug(msg)

    @classmethod
    def warning_chk(cls, log, msg):
        """Safely log warning."""
        if log:
            log.warning(msg)


class SimpleLog:
    """
    A class that acts as a wrapper for the logging module.
    It simplifies the creation of a log.
    It only logs to the console.
    """
    def __init__(self):
        """
        This is the constructor for the SimpleLog instance.
        """
        format_str = "%(levelname)s %(asctime)s:\t%(message)s"

        logging.basicConfig(level=logging.INFO, format=format_str)
        self.rootLogger = logging.getLogger()

    def info(self, s):
        """Log at info level."""
        self.rootLogger.info(s)

    def error(self, s):
        """Log at error level."""
        self.rootLogger.error(s)

    def debug(self, s):
        """Log at debug level."""
        self.rootLogger.debug(s)

    def warning(self, s):
        """Log at warning level."""
        self.rootLogger.warning(s)

    @classmethod
    def info_chk(cls, log, msg):
        """Safely log info."""
        if log:
            log.info(msg)

    @classmethod
    def error_chk(cls, log, msg):
        """Safely log an error."""
        if log:
            log.info(msg)

    @classmethod
    def debug_chk(cls, log, msg):
        """Safely log debug."""
        if log:
            log.debug(msg)

    @classmethod
    def warning_chk(cls, log, msg):
        """Safely log warning."""
        if log:
            log.warning(msg)
