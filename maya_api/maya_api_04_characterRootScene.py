import os
from maya import OpenMaya as om
from maya import OpenMayaMPx as ompx

# Custom transfrom must inherit from the MPxTransform node
class CharacterRoot(ompx.MPxTransform):
    kNodeName = 'characterRoot'
    kNodeID = om.MTypeId(0x01013)

    # Trasform can also implement a custom transfomration matrix
    # This isn't necessarry for our example, so we add base class
    kMatrix = ompx.MPxTransformationMatrix
    # matrix must also have an ID
    kMatrixID =om.MTypeId(0x01014)

    version = om.MObject()
    author = om.MObject()

    @classmethod
    def creator(cls):
        return ompx.asMPxPtr(cls)

    @staticmethod
    def initialize():
        # First add version number attribute so we can easily query the rig version number
        nAttr = om.MFnNumericAttribute()
        CharacterRoot.version = nAttr.create('version', 'ver', om.MFnNumericData.kInt, 0)
        nAttr.setStorable(True)

        # Then lets store the author of the rig meta data as well \\
        # Strings are generic typed attr
        tAttr = om.MFnTypedAttribute()
        # To create the default value we must create it from MFnStringDAta
        sData = om.MFnStringData()
        defaultValue = sData.create('Austin Cronin')
        # Finally we make our attr
        CharacterRoot.author = tAttr.create('author', 'a', om.MFnData.kString, defaultValue)

        # Then lts add them to our node
        CharacterRoot.addAttribute(CharacterRoot.version)
        CharacterRoot.addAttribute(CharacterRoot.author)

def initializePlugin(plugin):
    # add current directory to the script path so it can find the template we wrote
    dirName ='E:/Projects/AdvancePython/Scene'
    # Maya will lo for the vnironment varaible, MAYA_SCRIPT_PATH t olook for our scripts
    MAYA_SCRIPT_PATH = os.getenv('MAYA_SCRIPT_PATH')
    if dirName not in MAYA_SCRIPT_PATH:
        MAYA_SCRIPT_PATH += (os.pathsep + dirName)
        os.environ['MAYA_SCRIPT_PATH'] = MAYA_SCRIPT_PATH

    pluginFn = ompx.MFnPlugin(plugin)
    try:
        pluginFn.registerTransform(
            CharacterRoot.kNodeName, # The name of the node
            CharacterRoot.kNodeID, # The unique ID of the node
            CharacterRoot.creator, # the function to create this node
            CharacterRoot.initialize, # The function to intialize the node
            CharacterRoot.kMatrix, # Matrix MObject
            CharacterRoot.kMatrixID # matrix ID

        )
    except:
        om.MGlobal.displayError('Failed to register node %s' % CharacterRoot.kNodeName)
        raise

def uninitializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(CharacterRoot.kNodeID)
    except:
        om.MGlobal.displayError('Failed to deregister node %s' % CharacterRoot.kNodeName)
        raise
"""
To load


import maya.cmds as mc
from Scene import characterRoot
try:
    mc.delete(mc.ls(type='characterRoot'))
    # Force is important
    mc.unloadPlugin('characterRoot', force=True)
finally:
    mc.loadPlugin(characterRoot.__file__)

mc.createNode('characterRoot', name='acronin')
"""
