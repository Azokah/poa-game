from input.command import Command


class RightCommand(Command):
    def __init__(self, hero):
        self.hero = hero

    def execute(self):
        self.hero.phisics.walkRight()

    def stop(self):
        self.hero.phisics.stopRight()
