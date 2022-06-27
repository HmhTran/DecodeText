from command import invalidCmd

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
