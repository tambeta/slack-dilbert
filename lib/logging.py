
""" Custom logging utilities. """

import logging

class PrefixedLogRecord(logging.LogRecord):

    """ A LogRecord subclass providing the `prefix` field containing the
    logger name, unless it's the root logger.
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.prefix = "" if name == "root" else "[{}] ".format(name)

def make_log_record(name, level, fn, lno, msg, args, exc_info, func=None, sinfo=None, **kwargs):

    """ LogRecord factory. Note that path is currently passed as None.
    Implement path name extraction when desired.
    """

    return PrefixedLogRecord(name, level, None, lno, msg, args, exc_info, func, sinfo)
