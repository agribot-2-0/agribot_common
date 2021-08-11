#!/usr/bin/python3
import signal


class Killer:  # pylint: disable=old-style-class
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
        signal.signal(signal.SIGQUIT, self.exit)

    def exit(self, signal_number, frame):
        print("Received ", signal.strsignal(signal_number),
              ". Quitting after the synchronization finishes.")
        self.kill_now = True
