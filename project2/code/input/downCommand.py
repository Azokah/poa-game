from input.command import Command


class DownCommand(Command):
    def __init__(self, hero):
        self.hero = hero

    def execute(self):
        self.hero.phisics.walkDown()

    def stop(self):
        self.hero.phisics.stopDown()
