from input.escapeCommand import EscapeCommand
from input.upCommand import UpCommand
from input.downCommand import DownCommand
from input.rightCommand import RightCommand
from input.leftCommand import LeftCommand

class InputManager:
    def __init__(self, hero):
        self.commands = dict()
        self.commands['ESC'] = EscapeCommand()
        self.commands['UP'] = UpCommand(hero)
        self.commands['DOWN'] = DownCommand(hero)
        self.commands['RIGHT'] = RightCommand(hero)
        self.commands['LEFT'] = LeftCommand(hero)

    def command(self, key):
        return self.commands[key]
