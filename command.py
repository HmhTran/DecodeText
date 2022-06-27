from abc import ABC, abstractmethod

from utilities import printDoubleSpaced

class ACommand(ABC):
    __indentLen = 4
    
    @property
    @abstractmethod
    def name(self):
        pass
    
    def __eq__(self, other):
        return getType(self) == getType(other)
    
    def _errMsg(self, errMsgDetail=""):
        errMsgBase = f"Invalid {self.name.lower()} command"
        if errMsgDetail and errMsgDetail[-1] != ".":
            errMsgDetail += "."
        
        return f"{errMsgBase}: {errMsgDetail}" if errMsgDetail else f"{errMsgBase}."
    
    def _printHelpLine(self, tabN=0, s=""):
        if tabN < 0:
            raise ValueError("tabN must be a non-negative integer.")
        
        print(f"{''.ljust(self.__indentLen * tabN)}{s}")
    
    def _helpName(self, args=[]):
        return f"{self.name}:"
    
    def _helpSyntax(self, args=[]):
        syntax = f"Syntax: {self.name}"
        for a in args:
            syntax += " "
            if a[0] == "*":
                syntax+="Optional"
                a = a[1:]
            if not a.isidentifier():
                raise ValueError(f"arg {a} is not a valid variable name.")
            syntax += f"{{{a}}}"
        
        return syntax
    
    def _helpDescription(self, s):
        return f"Description: {s}"
    
    def printHelp(self):
        print("NA")
        print()
    
    @abstractmethod
    def execute(self, userInput):
        pass

class NoneCommand(ACommand):
    @property
    def name(self):
        return ""
    
    def __bool__(self):
        return False
    
    def execute(self, argsStr):
        print("Please enter a command.\n")
        return True

class InvalidCommand(ACommand):
    @property
    def name(self):
        return "invalid"
    
    def __bool__(self):
        return False
    
    def execute(self, argsStr):
        printDoubleSpaced("No such command available.")
        return True

class QuitCommand(ACommand):
    @property
    def name(self):
        return "quit"
    
    def printHelp(self):
        self._printHelpLine(0, self._helpName())
        self._printHelpLine(1, self._helpSyntax())
        self._printHelpLine(1, self._helpDescription("Exit program."))
        self._printHelpLine()
    
    def execute(self, argsStr):
        if argsStr != "":
            printDoubleSpaced(self._errMsg())
            return True
        
        return False

class HelpCommand(ACommand):
    def __init__(self, displayCmds):
        self.__displayCmds = displayCmds
    
    @property
    def name(self):
        return "help"
    
    def printHelp(self):
        self._printHelpLine(0, self._helpName())
        self._printHelpLine(1, self._helpSyntax())
        self._printHelpLine(1, self._helpDescription("List all available commands and how to use them."))
        self._printHelpLine()
    
    def execute(self, argsStr):
        if argsStr != "":
            printDoubleSpaced(self._errMsg())
            return True
            
        self.__displayCmds()
        return True

noneCmd = NoneCommand()
invalidCmd = InvalidCommand()
