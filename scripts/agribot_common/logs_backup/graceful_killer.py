#!/usr/bin/python3
from __future__ import print_function
import signal


class Killer:  # pylint: disable=old-style-class,too-few-public-methods
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
        signal.signal(signal.SIGQUIT, self.exit)

    def exit(self, signal_number):
        print(  # pylint: disable=no-member
            "Received ", signal.strsignal(signal_number),
            ". Quitting after the synchronization finishes.")
        self.kill_now = True
