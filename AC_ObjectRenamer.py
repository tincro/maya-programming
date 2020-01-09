from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None
}

DEFAULT_SUFFIX = "grp"

def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection: Whether or not we use the current selection

    Returns:
        A list of all the objects we operated on
    """
    # grab selection
    objects = cmds.ls(selection=selection, dag=True, long=True)
    # This function cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You don't have anything selected!")

    # sort everything in the selection list
    objects.sort(key=len, reverse=True)
    # grab the shortName of each object in the selection array
    for obj in objects:
        shortName = obj.split("|")[-1]
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        # if only one dependent grab object type of child, else the obj
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)
        # suffix DAG objects depending on object type
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        if not suffix:
            continue

        # if obj is already named with suffix, skip it.
        if obj.endswith('_'+suffix):
            continue
        # rename DAG object with correct suffix
        newName = "%s_%s" % (shortName, suffix)
        cmds.rename(obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)
    return objects
