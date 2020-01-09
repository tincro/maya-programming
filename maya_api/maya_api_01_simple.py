# import old Python API1.0
from maya import OpenMaya as om1
# import 2.0 API1
from maya.api import OpenMaya as om

print("Hello, World! i am writing this using the standard Pythin print statement")

# using Maya API to write directly to where Maya wants us to write TO
om.MGlobal.displayInfo("Hello, World! I am writing this using the OpenMaya API")

# using old Maya API to write the same thing
om1.MGlobal.displayInfo("Hello, World! This is using the old API")
