import sys
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaAnim as oma
import maya.api.openMayaRender as omr

def maya_useNewAPI():
    pass

# this dictionary will store all of our shapes and their point
# points are represented as a list of list of 3 floats each representing a vert
shapes = {
    'square': [
        [0.5,0.5,0.0],
        [0.5,-0.5,0.0],
        [-0.5,-0.5,0.0],
        [-0.5,0.5,0.0]
    ],
    'triangle': [
        [-0.5,-0.5,0],
        [0.5,-0.5,0.0],
        [0,0.5,0]
    ]
}

# We'll sort and store the list of names in an easy to access list
shapeNames = sorted(shapes.keys())

class CustomLocator(omui.MPxLocatorNode):
    id = om.MTypeId(0x01015)
    name = 'customLocator'

    # These are new and required for Viewport 2 to know how to draw the object
    drawDbClassification = "drawdb/geometry/customLocator"
    drawRegistrantId = "customLocatorPlugin"

    # Add Attribute placeholders
    shape = None
    color = None

    @classmethod
    def creator(cls):
        return cls()

    @staticmethod
    def initialize():
        eAttr = om.MFnEnumAttribute()
        CustomLocator.shape = eAttr.create('shape', 's')
        eAttr.storable = True

        # We can simply add shapes from the dictionary above
        for i, shape in enumerate(shapeNames):
            eAttr.addField(shape, i)

        CustomLocator.addAttribute(CustomLocator.shape)

        # now add the color attr
        nAttr = om.MFnNumericAttribute()
        CustomLocator.color = nAttr.createColor('color', 'col')
        nAttr.default = (0.5, 0.1, 0.1)
        nAttr.storable = True

        CustomLocator.addAttribute(CustomLocator.color)

# this clas sis required to let us control how vp2.0 will render our node
class CustomLocatorDrawOverride(omr.MPxDrawOverride):
    # this name isn't needed but for log purposes
    name = 'customLocatorOverride'

    def __init__(self, obj):
        super(CustomLocatorDrawOverride, self).__init__(
            # maya object to drawdb
            obj,
            # The callback to invoke when drawing
            None,
            # isAlwaysDirty. If set to true, it can be much heavier because it constantly updates
            False
        )

        @classmethod
        def creator(cls, obj):
            # the over ride gets a ref erece to the obj being drawing
            # we then give back a new override with this obj as a parameter
            return cls(obj)

        def supportedDrawAPIs(self):
            # Tell maya which vp we can render in .
            return omr.MRenderer.kOpenGL | omr.MRenderer.kDirectX11 | omr.MRenderer.kOpenGLCoreProfile

        def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
            """
            Maya calls this function whenever the object needs to be updated for a draw.
            This is where you should fetch any data needed, because doing it in the actual draw can crash Maya

            :param objPath: The path to the object being drawn
            :param cameraPath: The path to the camera that is being used to draw
            :param frameContext: Frame level context information
            :param oldData: Data cached by the previous draw of the instance

            :return: new data
            """
            data = oldData # default our data to the oldData
            if not isInstance(data, LocatorData):
                # But if it isn't the type we've defined, make a new one
                data = LocatorData()

            # We need to find out which shape we're expected to draw
            # We can get this from the objPath
            locator = objPath.node()
            # from this we get the plug and see what the value is set to
            shapePlug = om.MPlug(locator, CustomLocator.shape)

            # If it can't be fetched, just exit because we can't draw anything
            if shapePlug.isNull:
                om.MGlobal.displayError('Cannot find shape plug for node')
                return data

            # We have to get the display status of this node
            state = omr.MGeometryUtilities.displayStatus(objPath)
            # If its dormant, it means that it's not selected so we'll use the set color
            # The ampersnad operator checks if the two bit values are equal
            # Its an efficient way to compare two states even fi they are integers
            if state & omr.MGeometryUtilities.kDormant:
                # We get the color plug and try and get its value
                colorPlug = om.MPlug(locator, CustomLocator.color)
                if colorPlug.isNull:
                    # If it can't be fetched then default it
                    color = om.MColor((0.5, 0.3, 0.3))
                else:
                    # If it is available, then lets get the color
                    color = []
                    # The color is a compound attribute so we need to get all the children
                    # We do this by looping through it
                    for channel in range(colorPlug.numChildren()):
                        channelPlug = colorPlug.child(channel)
                        color.append(channelPlug.asFloat())
                    color = om.MColor(color)
                # Set the color that we'll be drawing now so it always gets updated
                # data.color = omr.MGeometryUtilities.wireframeColor(objPath)
                data.color = color
            else:
                # Otherwise if it is any form of selected, just shade it by the wireframe color
                data.color = omr.MGeometryUtilities.wireframeColor(objPath)
            # Then letes see what index is set for the shape
            shape = shapePlug.asInt()
            # If ti matches the current shape, then just return the data
            if shape == data.shape:
                return data

            # If it's a differnt shape then before, lets calculate its properties
            shapeName = shapeNames[shape]
            currentShapePoints = shapes[shapeName]
            currentShapePointCount = len(currentShapePoints)

            # We clear the existing Data
            data.lineList.clear()
            data.triangleList.clear()

            # Then lets construct some new data to draw
            for i in range(currentShapePointCount - 1):
                # We start out by defining the lines of this shape
                # These consist of two points, each with xyz
                data.lineList.append(om.MPoint(
                    currentShapePoints[i][0],
                    currentShapePoints[i][1],
                    currentShapePoints[i][2]
                ))
                data.lineList.append(om.MPoint(
                    currentShapePoints[i + 1][0],
                    currentShapePoints[i + 1][1],
                    currentShapePoints[i + 1][2]
                ))

                # Then lets construct the triangles that will fil lout this shape
                data.triangleList.append(om.MPoint(
                    currentShapePoints[0][0],
                    currentShapePoints[0][1],
                    currentShapePoints[0][2]
                ))

                data.triangleList.append(om.MPoint(
                    currentShapePoints[i][0],
                    currentShapePoints[i][1],
                    currentShapePoints[i][2]
                ))

                data.triangleList.append(om.MPoint(
                    currentShapePoints[i + 1][0],
                    currentShapePoints[i + 1][1],
                    currentShapePoints[i + 1][2]
                ))
            return data
        def addUIDrawables(self, objPath, drawManager, frameContext, data):
            # If we don't have valid data, then don't draw
            if not isinstance(data, LocatorData):
                return

            # Start drawing
            drawManager.beginDrawable()

            # Set the current color
            drawManager.setColor(data.color)

            # We get the state of the current object
            # and we use this to set its depth priority
            # in this case, if its selected, its always in the high priority, Otherwise not
            state = omr.MGeometryUtilities.displayStatus(objPath)
            if state & omr.MGeometryUtilities.kActiveComponent:
                depthPriority = omr.MRenderItem.sActiveWireDepthPriority
            else:
                depthPriority = omr.MRenderItem.sDormantFilledDepthPriority
            drawManager.setDepthPriority(depthPriority)

            # set the drawing mode based on the current shading type
            if (frameContext.getDisplayStyle() & omr.MFrameContext.kGouraudShadeed):
                drawManager.mesh(
                    omr.MGeometry.kTriangles,
                    data.triangleList
                )
            # Give ti the lines to draw
            drawManager.mesh(omr.MUIDrawManager.kLines, data.lineList)

            # Then end drawing
            drawManager.endDrawable()

class LocatorData(om.MUserData):
    def __init__(self):
        # The false tells it not to delete after its used
        super(LocatorData, self).__init__(false)

        self.shape = None # The shape index that is being drawn
        self.color = MColor() # Holds the color to draw
        self.lineList = om.MPointArray() # The list of lines to draw
        self.triangleList = om.MPointArray() # the list of triangles to draw


def initializePlugin(plugin):
    # We'll update the list when the plugin is initialized in case it changes
    global shapeNames
    shapenames = sorted(shapes.keys())

    # Also lets make sure this directory is in the path so we can load our attr editor # TEMP:
    dirName ='E:/Projects/AdvancePython/Scene'
    # Maya will lo for the vnironment varaible, MAYA_SCRIPT_PATH t olook for our scripts
    MAYA_SCRIPT_PATH = os.getenv('MAYA_SCRIPT_PATH')
    if dirName not in MAYA_SCRIPT_PATH:
        # os.pathsep gives us the character that separates paths on yoru specific operating system
        MAYA_SCRIPT_PATH += (os.pathsep + dirName)
        os.environ['MAYA_SCRIPT_PATH'] = MAYA_SCRIPT_PATH

    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(
            CustomLocator.name, # The name of the node
            CustomLocator.id, # The unique ID of the node
            CustomLocator.creator, # the function to create this node
            CustomLocator.initialize, # The function to intialize the node
            CustomLocator.kLocatorNode, # the type of node it is
            CustomLocator.drawDbClassification # The Viewport 2 classification
        )
    except:
        om.MGlobal.displayError('Failed to register node %s' % CustomLocator.name)
        raise

    # Next we register the override for VP2 to use
    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(
            CustomLocator.drawDbClassification, # the VP2 classification
            CustomLocator.drawRegistrantId, # the ID name to register it as
            CustomLocatorDrawOverride.creator # The creator for the override
        )
    except:
        om.MGlobal.displayError('Failed to register override: %s' % CustomLocatorDrawOverride.name)
        raise

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(CustomLocator.id)
    except:
        om.MGlobal.displayError('Failed to deregister node %s' % CustomLocator.name)
        raise

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(
            CustomLocator.drawDbClassification,
            CustomLocator.drawRegistrantId
        )
    except:
        om.MGlobal.displayError('Failed to deregsiter override %s' % CustomLocatorDrawOverride.name)
        raise
"""
To load


import maya.cmds as mc
from Scene import customLocator
mc.file(new=True, force=True)

try:
    # Force is important
    mc.unloadPlugin('customLocator', force=True)
finally:
    mc.loadPlugin(customLocator.__file__)

mc.createNode('customLocator')
"""
