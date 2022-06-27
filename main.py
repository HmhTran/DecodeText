from abc import ABC, abstractmethod
import os

from command_dict import CommandDict
from page import DecodePage
from command_user_loop import CommandUserLoop

def printDoubleSpaced(msg):
    print(f"\n{msg}\n")

class AApp(ABC):
    @abstractmethod
    def run(self):
        pass

class ACmdUesrLoopApp(AApp):
    def __init__(self, cmdUserLoop, page):
        self._displayPage = page.display
        self.__cmdUserLoop = cmdUserLoop
        self.__cmdUserLoop.setCmds(page.getCmds())
    
    @abstractmethod
    def _appOpen(self):
        pass
    
    @abstractmethod
    def _appClose(self):
        pass
    
    def run(self):
        self._appOpen()
        self.__cmdUserLoop.run()
        self._appClose()

class DecodeTextApp(ACmdUesrLoopApp):
    def __init__(self, cmdUserLoop, page):
        super().__init__(cmdUserLoop, page)
    
    def _appOpen(self):
        self._displayPage()
        print()            
    
    def _appClose(self):
        os.system("cls")
        print()
        print("Now exiting DecodeText.")
        print("Goodbye!")

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
