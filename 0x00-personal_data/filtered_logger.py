#!/usr/bin/env python3
""" accept a list of strings fields constructor argument. """
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ accept a list of strings fields constructor argument.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ accept a list of strings fields constructor argument. """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns regex obfuscated log messages """
    for value in fields:
        message = re.sub(f'{value}=(.*?){separator}',
                         f'{value}={redaction}{separator}', message)
    return message
