import sys

from input.command import Command


class EscapeCommand(Command):

    def execute(self):
        sys.exit()

    def stop(self):
        pass


