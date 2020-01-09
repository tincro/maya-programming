import maya.cmds as cmds
from optwin import AC_OptionsWindow
class AC_PolyOptionsWindow(AC_OptionsWindow):
    def __init__(self):
        AC_OptionsWindow.__init__(self)
        self.title = 'Polygon Creation Options'
        self.actionName = 'Create'
    def displayOptions(self):
        self.objType = cmds.radioButtonGrp(
            label='Object Type: ',
            labelArray4=[
                'Cube',
                'Cone',
                'Cylinder',
                'Sphere'
            ],
            numberOfRadioButtons=4,
            select=1
        )
        self.xformGrp = cmds.frameLayout(
            label='Transformations',
            collapsable=True
        )
        cmds.formLayout(
            self.optionsForm, e=True,
            attachControl=(
                [self.xformGrp,'top',2,self.objType]
            ),
            attachForm=(
                [self.xformGrp,'left',0],
                [self.xformGrp,'right',0]
            )
        )
        self.xformCol = cmds.columnLayout()
        self.position = cmds.floatFieldGrp(
            label='Position: ',
            numberOfFields=3
        )
        self.rotation = cmds.floatFieldGrp(
            label='Rotation (XYZ): ',
            numberOfFields=3
        )
        self.scale = cmds.floatFieldGrp(
            label='Scale: ',
            numberOfFields=3,
            value=[1.0,1.0,1.0,1.0]
        )
        cmds.setParent(self.optionsForm)
        self.color = cmds.colorSliderGrp(
            label='Vertex Colors: '
        )
        cmds.formLayout(
            self.optionsForm, e=True,
            attachControl=(
                [self.color,'top',0,self.xformGrp]
            ),
            attachForm=(
                [self.color,'left',0]
            )
        )
    def applyBtnCmd(self, *args):
        self.objIndAsCmd={
            1:cmds.polyCube,
            2:cmds.polyCone,
            3:cmds.polyCylinder,
            4:cmds.polySphere
        }
        objIndex = cmds.radioButtonGrp(
            self.objType, q=True, select=True
        )
        newObject = self.objIndAsCmd[objIndex]()
        pos = cmds.floatFieldGrp(
            self.position, q=True, value=True
        )
        rot = cmds.floatFieldGrp(
            self.rotation, q=True, value=True
        )
        scale = cmds.floatFieldGrp(
            self.scale, q=True, value=True
        )
        cmds.xform(newObject[0], t=pos, ro=rot, s=scale)
        col = cmds.colorSliderGrp(
            self.color, q=True, rgbValue=True
        )
        cmds.polyColorPerVertex(
            newObject[0],
            colorRGB=col,
            colorDisplayOption=True
        )
AC_PolyOptionsWindow.showUI()