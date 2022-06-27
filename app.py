from abc import ABC, abstractmethod
import os

class AApp(ABC):
    @abstractmethod
    def run(self):
        pass

class AUserInterfaceApp(AApp):
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

class DecodeTextApp(AUserInterfaceApp):
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
