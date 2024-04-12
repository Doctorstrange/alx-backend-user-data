#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import logging
from typing import List
import re
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter_datum that returns the log message obfuscated: """
    for value in fields:
        message = re.sub(f'{value}=.*?{separator}',
                         f'{value}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ accept a list of strings fields constructor argument. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ akes no arguments and returns nothing """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    dbstuff = mysql.connector.connection.MySQLConnection(user=username,
                                                         password=password,
                                                         host=host,
                                                         database=db_name)
    return dbstuff


def main():
    """
    One secure option is to store them as
    environment variable on the application server.
    """
    db = get_db()
    data = db.data()
    data.execute("SELECT * FROM users;")
    field_names = [i[0] for i in data.description]

    logger = get_logger()

    for row in data:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    data.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ hat takes no arguments and returns a logging.Logger object
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ hat takes no arguments and returns a logging.Logger object """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
