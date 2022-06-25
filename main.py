from abc import ABC, abstractmethod
import os

QUIT_COMMAND_NAMES = {"quit", "exit", "close"}

def printDoubleSpaced(msg):
    print(f"\n{msg}\n")

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

class CommandDict():
    def setCmds(self, cmdList):
        cmdDict = {}
        for cmd in [cmd for cmd in cmdList if cmd.name != "help" and not cmd.name in QUIT_COMMAND_NAMES]:
            if cmd.name in cmdDict:
                raise ValueError(f"Command list contains duplicate command: {cmd.name}.")
            cmdDict[cmd.name] = {"isOn": True, "cmd": cmd}
        self.__cmdDict = cmdDict
    
    def __init__(self, cmdList=[]):
        self.setCmds(cmdList)
    
    def get(self, cmdName):
        cmdName = cmdName.lower()
        cmd = self.__cmdDict.get(cmdName)        
        return cmd["cmd"] if cmd and cmd["isOn"] else invalidCmd
    
    def checkIsCmdIn(self, cmdName):
        return cmdName.lower() in self.__cmdDict
    
    def __tryGetCmd(self, cmdName):
        cmdName = cmdName.lower()
        cmd = self.__cmdDict.get(cmdName)
        if not cmd:
            raise ValueError("No such command available.")
        return cmd
    
    def setIsCmdOn(self, cmdName, isOn):
        cmd = self.__tryGetCmd(cmdName)
        self.__cmdDict[cmdName]["isOn"] = isOn
    
    def checkIsCmdOn(self, cmdName):
        cmd = self.__tryGetCmd(cmdName)
        return cmd["isOn"]
    
    def printHelp(self):
        for cmd in [command["cmd"] for command in self.__cmdDict.values() if command["isOn"]]:
            cmd.printHelp()

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

class CommandUserLoop():
    def __displayCmds(self):
        printDoubleSpaced("List of Available Commands")
        self.__cmdDict.printHelp()
        for cmd in self.__cliCmdDict.values():
            cmd.printHelp()
    
    def setCmds(self, cmds):
        cmdDict = CommandDict(cmds) if isinstance(cmds, list) else cmds
        self.__cmdDict = cmdDict
    
    def __init__(self, cmdList=[]):
        self.setCmds(cmdList)
        
        self.__cliCmdDict = {
            "help": HelpCommand(self.__displayCmds),
            "quit": QuitCommand()
        }
    
    def __splitUserInput(self, userInput):
        spaceIdx = userInput.find(" ")
        cmdName = userInput[0:spaceIdx] if spaceIdx > -1 else userInput
        argsStr = userInput[spaceIdx+1:] if cmdName != userInput else ""
        return cmdName, argsStr
    
    def __getCmd(self, cmdName):
        if not cmdName:
            return noneCmd
        
        cmdName = cmdName.lower()
        cmdName = "quit" if cmdName in QUIT_COMMAND_NAMES else cmdName
        
        if not cmdName.isidentifier():
            return invalidCmd
        elif cmdName != "help" and cmdName != "quit":
            return self.__cmdDict.get(cmdName)
        else:
            return self.__cliCmdDict.get(cmdName, invalidCmd)
    
    def run(self):
        isRunning = True
        while(isRunning):
            print("Enter Command:")
            userInput = input()
            cmdName, argsStr = self.__splitUserInput(userInput)
            command = self.__getCmd(cmdName)
            isRunning = command.execute(argsStr)

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
