from input.command import Command


class UpCommand(Command):
    def __init__(self, hero):
        self.hero = hero

    def execute(self):
        self.hero.phisics.walkUp()

    def stop(self):
        self.hero.phisics.stopUp()
