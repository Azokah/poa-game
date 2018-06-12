from abc import ABCMeta
from abc import abstractmethod


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def stop(self):
        pass
