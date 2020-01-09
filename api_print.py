from maya import OpenMaya as om1
from maya.api import OpenMaya as om

print("Hello, World! I am writing this using the standard Python print statement!")

om.MGlobal.displayInfo("Hello, World! I am writing this using the OpenMaya API")

om1.MGlobal.displayInfo("Hello, World! I am writing this using the old API")