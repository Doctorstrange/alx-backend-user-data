#!/usr/bin/env python3
""" filter_datum that returns the log message obfuscated """
import re


def filter_datum(fields, redaction, message, separator):
    pattern = re.compile(r'(\b' + '|'.join(fields) + r')=')
    return pattern.sub(r'\1=' + redaction + separator, message)
