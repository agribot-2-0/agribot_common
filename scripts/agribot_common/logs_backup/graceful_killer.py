#!/usr/bin/python3
from __future__ import print_function
import signal


class Killer:  # pylint: disable=old-style-class,too-few-public-methods
    kill_now = False
    exception_message_list = []

    def __init__(self, time):
        self._exception_log_period = time
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
        signal.signal(signal.SIGQUIT, self.exit)
        signal.signal(signal.SIGALRM, self.print_what)

    def exit(self, signal_number, _):
        print(
            "Received ",
            signal.strsignal(signal_number),  # pylint: disable=no-member
            ". Quitting after the synchronization finishes.")
        self.kill_now = True
        signal.alarm(0)

    def print_what(self, *_):
        if self.exception_message_list:
            print(self.exception_message_list)
            self.exception_message_list = []
        signal.alarm(self._exception_log_period)
