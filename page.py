from abc import ABC, abstractmethod

from command_dict import CommandDict

class APage(ABC):
    def __init__(self, cmdList=[]):
        self._cmdDict = CommandDict(cmdList)
    
    @abstractmethod
    def display(self):
        pass
    
    def getCmds(self):
        return self._cmdDict

class DecodePage(APage):
    def display(self):
        print("\nWelcome to DecodeText!")
