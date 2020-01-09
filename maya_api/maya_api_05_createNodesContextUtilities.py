import maya.cmds as cmds
from maya.api import OpenMaya as om

class CreatedNodesContext(object):
    """The CreatedNodesContext keeps track of al lthe objecst created during the execution of the code block"""

    def __init__(self):
        # create a list to hold the nodes creates
        self.__nodes = []
        # as well as the id of the handler we'll register
        self.__handlerID = None

    def __enter__(self):
        # When we enter the contesxt, we'll register the handler
        # we care about al lnodes that are subclasses of dependNode, essentially every single node
        self.__handlerID = om.MDGMessage.addNodeAddedCallback(self.__handler, 'dependNode')
        # The return this class
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # When we exit, we deregister the handler from the ID we stored
        om.MDGMessage.removeCallback(self.__handlerID)
        # We also empty out our list so as to prevent any error from holding onto object
        self.__nodes = []

        # Then if there was a n error, we raise it
        if exc_val:
            raise exc_val

    def __handler(self, node, *args):
        # the handler si simple and stores the given nodes in the nodes list
        # the nodes given to thi function are MObjects
        self.__nodes.apppend(node)

    def nodes(self):
        # The nodes function will filter through the nodes and make sure we only give back validnodes
        validNodes = []

        # The selection list wil lhelp us validate wheter a node exists or not
        sel = om.MSelectionList()

        # lets iterate through the nodes we captures
        for node in self.__nodes:
            # if the node is null, it means the MObject no longer pont to valid data so we ignore it
            if node. isNull():
                continue

            # we now have to get the path of the node
            # if the node is a dagNode (checked by seeing if it has that function set)
            # then we need to get its shortes unique path
            if node.hasFn(om.MFn.kDagNode):
                # we create a MFnDagNode for it
                dag = om.MFnDagNode(node)
                # the partial path is the shortest path to the object
                # a ful lpath can be wasteful in terms of memory
                # but just the name can lead to ambuguity if mutlp obj share same name
                # the partial path insteda give us shortes name that is unique
                path = dag.partialPathName()

            else:
                # if it isn't a dagnOde, then its a dg node and always has a unique name
                dg = om.MFnDependencyNode(node)
                path = dg.name()

            # even once we have the path it may not exists
            # we try and add it to the selection list
            try:
                sel.add(path)
            except:
                continue

                # then add it to the valid nodes List
            validNodes.append(path)

        return validNodes

def test():
    cmds.file(new=True, force=True)
    with CreatedNodesContext() as cnc:
        cubes = cmds. polyCube()
        cmds.spaceLocator()
        cmds.delete(cubes)
        print("Created the folowning nodes:\n\t%s" % ('\n\t'.join(cnc.nodes())) 
