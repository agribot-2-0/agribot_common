#!/usr/bin/python3
from __future__ import print_function
import signal


class Killer:  # pylint: disable=old-style-class,too-few-public-methods
    kill_now = False
    exception_message = None

    def __init__(self):
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
        if self.exception_message != None:
            print(self.exception_message)
            self.exception_message = None
        signal.alarm(10 * 60)
