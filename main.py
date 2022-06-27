from abc import ABC, abstractmethod

from command_dict import CommandDict
from page import DecodePage
from command_user_loop import CommandUserLoop
from app import DecodeTextApp

def printDoubleSpaced(msg):
    print(f"\n{msg}\n")

class AAppFactory():
    @abstractmethod
    def build(self):
        pass

class DecodeTextAppFactory(AAppFactory):
    def build(self):
        return DecodeTextApp(CommandUserLoop(CommandDict()), DecodePage())

def main():
    app = DecodeTextAppFactory().build()
    app.run()

if __name__ == "__main__":
    main()
