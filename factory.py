from abc import ABC, abstractmethod

from command_dict import CommandDict
from page import DecodePage
from command_user_loop import CommandUserLoop
from app import DecodeTextApp

class AAppFactory(ABC):
    @abstractmethod
    def build(self):
        pass

class DecodeTextAppFactory(AAppFactory):
    def build(self):
        return DecodeTextApp(CommandUserLoop(CommandDict()), DecodePage())
