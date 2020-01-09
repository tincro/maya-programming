# OpenMaya 2 doesn't support creating deformers, so we use the old way

from maya import OpenMaya as om
from maya import OpenMayaMPx as ompx
import maya.cmds as cmds

# Unfortunately the API has changed between 2015 and 2016 so we need to get the right attr,
# This isnt' a big ddea, and if your only using 2016+ you can ski9p half [if statement]
kApiVersion = cmds.about(apiVersion=True)
if kApiVersion < 201600:
    inputAttr = ompx.cvar.MPxDeformerNode_input
    inputGeomAttr = ompx.cvar.MPxDeformerNode_inputGeom
    outputGeomAttr = ompx.cvar.MPxDeformerNode_outputGeom
    envelopeAttr = ompx.cvar.MPxDeformerNode_envelope
else:
    inputAttr = ompx.cvar.MPxGeometryFilter_input
    inputGeomAttr = ompx.cvar.MPxGeometryFilter_inputGeom
    outputGeomAttr = ompx.cvar.MPxGeometryFilter_outputGeom
    envelopeAttr = ompx.cvar.MPxGeometryFilter_envelope

class PushDeformer(ompx.MPxDeformerNode):
    id = om.MTypeId(0x01012) # Setup the ID
    name = 'push' # set up the name

    # Now add the attributes we'll be using
    # Unlike OpenMaya 2, we need to use an empty MObject here isntead of just None
    push = om.MObject()

    @classmethod
    def creator(cls):
        # Unlike OM2, we need to return this as MPxPtr instead
        return ompx.asMPxPtr(cls)

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()

        PushDeformer.push = nAttr.create('push', 'p', om.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(True)
        nAttr.setStorable(True)
        nAttr.setChannelBox(True)

        PushDeformer.addAttribute(PushDeformer.push)
        PushDeformer.attributeAffects(PushDeformer.push, outputGeomAttr)

        # We also want to make our node paintable
        cmds.makePaintable(
            PushDeformer.name,
            'weights',
            attrType='muliFloat',
            shapeMode='deformer'
        )
    def deform(self, data, geoIterator, matrix, geometryIndex):
        # Get the push values
        pushHandle = data.inputValue(self.push)
        push = pushHandle.asFloat()

        # Get evelope values
        envelopeHandle = data.inputValue(envelopeAttr)
        envelope = envelopeHandle.asFloat()

        # Get input geo
        mesh = self.getInputMesh(data, geometryIndex)

        # Create an empty array(list) of Float Vecotrs to store our normals in
        normals = om.MFloatVectorArray()
        # Then make the meshFn to interact with the mesh
        meshFn = om.MFnMesh(mesh)
        # And we use this to get and store the normals from the mesh onto the normals array we created above
        # Remember to pay attention to the luralization of normals
        meshFn.getVertexNormals(
            True, # If Ture, the normals are angleWeighted which is what we want
            normals, # We tell it wahat to store the data in, in this case, our array above
            om.MSpace.kTransform # Finally we tell it wha tspace we want the normals in, our local object space

        )
        # Now we can iterate through the geometry vertices and doe oru deformation
        while not geoIterator.isDone():
            # Get the index of our current point
            index = geoIterator.index()
            #  Look up the normals for this point from our array
            normal = om.MVector(normals[index])
            # Get the position fo the point
            position = geoIterator.position()
            # Then calculate the offset
            # we do thsi by multiplying the magnitutde of the normal vector by the intensity of the push and envelope
            offset = (normal * push * envelope)

            # We then query the painted weigth for this are a
            weight = self.weightValue(data, geometryIndex, index)
            offset = (offset * weight)

            # Finally we can set the position
            geoIterator.setPosition(position+offset)
            # And always remember to go to next item
            geoIterator.next()

        def getInputMesh(self, data, geomIdx):
            # T oget the mesh we need to check the inptu of the node
            inputHandle = data.outputArrayValue(inputAttr)
            inputHandle.jumpToElement(geomIdx)
            # once we have the input handle, we get its values, then find the children mesh and get it as a mesh MObject
            mesh = inputHandle.outputValue().child(inputGeomAttr).asMesh()
            return mesh

def initializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)

    try:
        pluginFn.registerNode(
            PushDeformer.name, # The name of the node
            PushDeformer.id, # The unique ID of the node
            PushDeformer.creator, # the function to create this node
            PushDeformer.initialize, # The function to intialize the node
            ompx.MPxNode.kDeformerNode # one extra argument to tel lit the type of node
        )
    except:
        om.MGlobal.displayError('Failed to register node %s' % PushDeformer.name)
        raise

def uninitializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(PushDeformer.id)
    except:
        om.MGlobal.displayError('Failed to deregister node %s' % PushDeformer.name)
        raise
"""
To load

from Nodes import pushDeformer
import maya.cmds as mc

try:
    # Force is important
    mc.unloadPlugin('pushDeformer', force=True)
finally:
    mc.loadPlugin(pushDeformer.__file__)

mc.polySphere()
mc.deformer(type='push')
"""
