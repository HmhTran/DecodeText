from utilities import printDoubleSpaced
from command import QuitCommand, HelpCommand, noneCmd, invalidCmd

QUIT_COMMAND_NAMES = {"quit", "exit", "close"}

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
