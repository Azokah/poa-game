from input.command import Command


class LeftCommand(Command):
    def __init__(self, hero):
        self.hero = hero

    def execute(self):
        self.hero.phisics.walkLeft()

    def stop(self):
        self.hero.phisics.stopLeft()
