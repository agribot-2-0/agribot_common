#!/usr/bin/python3
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
        print(  # pylint: disable=superfluous-parens
            "Received ",
            signal.strsignal(signal_number),  # pylint: disable=no-member
            ". Quitting after the synchronization finishes.")
        self.kill_now = True
        signal.alarm(0)

    def add_exception(self, exception):
        if exception not in self.exception_message_list:
            self.exception_message_list.append(exception)

    def clear_exception_message_list(self):
        self.exception_message_list = []

    def print_what(self, *_):
        if self.exception_message_list:
            print(self.exception_message_list)  # pylint: disable=superfluous-parens
            self.exception_message_list = []
        signal.alarm(self._exception_log_period)
