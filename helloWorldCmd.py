from maya.api import OpenMaya as om

def maya_useNewAPI():
    pass

class HelloWorldCmd(om.MPxCommand):
    # name of the command
    kPluginCmdName = "hello"

    # Flag names for the name flag
    kNameFlag = '-n'
    kLongNameFlag = '-name'

    # the functions action command
    def doIt(self, args):

        # to parse the arguments, pass them to MArgDatabase and use MPxCommands buildt in syntax method to resolve it
        argData = om.MArgDatabase(self.syntax(), args)

        # Check if flag has been provided
        if argData.isFlagSet(HelloWorldCmd.kNameFlag):
            # get its value
            name = argData.flagArgumentString(HelloWorldCmd.kNameFlag, 0)
        else:
            # if nothing is provided, default
            name = 'World'

        om.MGlobal.displayInfo("Hello, %s!" % name)

# Initialize plugin
# create the command
def cmdCreator():
    '''Create an instance of our command'''
    return HelloWorldCmd()

# lets our command take arguments
def syntaxCreator():
    '''Defines the argument and flag syntax for this command'''
    # make the syntax object that will handle all the parameters given to the command
    syntax = om.MSyntax()

    syntax.addFlag(
        HelloWorldCmd.kNameFlag,
        HelloWorldCmd.kLongNameFlag,
        om.MSyntax.kString
    )

    return syntax

# Initialize the plugin when it loads
def initializePlugin( mobject ):
    '''Initialize Plugin when Maya loads it'''
    # convert our plugin to a type MFnPLugin so we can interact with it
    mplugin = om.MFnPlugin(mobject)

    try:
        mplugin.registerCommand(HelloWorldCmd.kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        om.MGlobal.displayError('Failed to register command: %s\n' % HelloWorldCmd.kPluginCmdName)
        raise

def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)

    try:
        mplugin.deregisterCommand(HelloWorldCmd.kPluginCmdName)
    except:
        om.MGlobal.displayError('Faled to deregister command: %s\n' % HelloWorldCmd.kPluginCmdName)
        raise
