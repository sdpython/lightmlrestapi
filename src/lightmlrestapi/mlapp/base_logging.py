"""
@file
@brief Machine Learning Post request
"""
from datetime import datetime
import os
from time import perf_counter
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import jwt


class BaseLogging:
    """
    Simplifies logging. Logging is encrypted
    with module :epkg:`pyjwt`.
    """

    def __init__(self, secret, folder='.', level=logging.INFO, encoding='utf-8', when='d'):
        """
        @param      secret      secret for encryption (None to disable the logging)
        @param      folder      folder where to write the logs
        @param      level       logging level
        @param      when        when rotating the logs,
                                see `TimedRotatingFileHandler
                                <https://docs.python.org/3/library/logging.handlers.html?
                                highlight=streamhandler#logging.handlers.TimedRotatingFileHandler>`_
        @param      encoding    encoding
        """
        if secret is None:
            self.secret = None
        else:
            current_time = datetime.now()
            current_date = current_time.strftime("%Y-%m-%d")
            filename = "{0}-{1}.log".format(
                self.__class__.__name__, current_date)
            file_location = os.path.join(folder, filename)
            form = Formatter('%(asctime)s,%(levelname)s,%(message)s,%(data)s')
            self.handler = TimedRotatingFileHandler(
                file_location, encoding=encoding, delay=True, when=when)
            self.handler.setFormatter(form)
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.setLevel(level)
            self.logger.addHandler(self.handler)
            self.secret = secret

    def save_time(self):
        """
        Saves the times to get a duration later.
        """
        self.t1 = perf_counter()

    def duration(self):
        """
        Get the duration since @see me save_time was called.
        """
        return perf_counter() - self.t1

    def info(self, msg, data):
        """
        Logs any king of data into the logs.

        @param  msg         message
        @param  data        data to log
        """
        if self.secret is not None:
            enc_data = jwt.encode(data, self.secret, algorithm='HS256')
            self.logger.info(msg, extra=dict(data=enc_data))

    def error(self, msg, data):
        """
        Logs any king of data into the logs.

        @param  msg         message
        @param  data        data to log
        """
        if self.secret is not None:
            enc_data = jwt.encode(data, self.secret, algorithm='HS256')
            self.logger.error(msg, extra=dict(data=enc_data))


def enumerate_parsed_logs(folder, secret, encoding='utf-8'):
    """
    Goes through a list of logged files,
    reads and decrypt the content.

    @param      folder      folder which contains the logs
    @param      secret      secret
    @param      encoding    encoding
    @return                 iterator on decrypted data
    """
    for root, _, files in os.walk(folder):
        for name in files:
            full = os.path.join(root, name)
            with open(full, 'r', encoding=encoding) as f:
                for i, line in enumerate(f):
                    spl = line.rstrip('\n\r').split(',')
                    if len(spl) != 5:
                        raise ValueError(
                            "Format issue in\n    File \"{0}\", line {1}".format(full, i + 1))
                    if spl[4].startswith("b'") and spl[4].endswith("'"):
                        data = spl[4][2:-1]
                    else:
                        raise ValueError(
                            "Corrupted logs due to: '{0}'".format(spl[4]))
                    dec = jwt.decode(data, secret, algorithms=['HS256'])
                    dt = datetime.strptime(spl[0], '%Y-%m-%d %H:%M:%S')
                    rec = dict(dt=dt, code=spl[1], level=spl[2],
                               msg=spl[3], data=dec)
                    yield rec
