from math import sin, cos, pi

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties
from panda3d.core import Vec3
import sys

# Debugging
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class MyApp(ShowBase):

    def recenterMouse(self):
        self.win.movePointer(0,
              int(self.win.getProperties().getXSize() / 2),
              int(self.win.getProperties().getYSize() / 2))

    def updateKeyMap(self, controlName, controlState):
        """ Update the key map

        :controlName:  The specific key
        :controlState: Boolean
        """
        self.keyMap[controlName] = controlState

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.keyMap = {
                "up"    : False,
                "down"  : False,
                "right" : False,
                "left"  : False,
                }

        self.keymapping= zip(
                (",", "a", "e", "o"),
                #  ("w", "a", "s", "d"),
                ("up", "left", "right", "down")
                )
        for key, keyname in self.keymapping:
            self.accept(key,    
                    self.updateKeyMap, [keyname, True ])
            self.accept(key+"-up",
                    self.updateKeyMap, [keyname, False])
        self.movementDirs = [
                ("up",    Vec3.unitY()),
                ("left", -Vec3.unitX()),
                ("right", Vec3.unitX()),
                ("down", -Vec3.unitY())
                ]

        self.plane = self.loader.loadModel("models/plane.bam")
        self.plane.reparentTo(self.render)
        self.cube = self.loader.loadModel("models/cube.bam")
        self.cube.reparentTo(self.render)

        self.accept('escape', sys.exit, [0])

        self.camera.setPos(0,-20,3)
        self.cube.setPos(0,0,1)
        self.camera.lookAt(self.cube)

        self.taskMgr.add(self.mouseWatchTask, "Mouse Watch Task")
        self.taskMgr.add(self.keyboardWatchTask, "Keyboard Watch Task")

        self.debugText = self.genLabelText("",1)

        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_confined)
        wp.setCursorHidden(True)
        self.win.requestProperties(wp)

    def genLabelText(self, text, i):
        text = OnscreenText(text = text, pos = (-1.3, .5-.05*i), fg=(0,1,0,1),
                      align = TextNode.ALeft, scale = .05)
        return text

    def keyboardWatchTask(self, task):
        """Handle keyboard input"""
        dt = globalClock.getDt()

        for keyname, dir in self.movementDirs:
            if self.keyMap[keyname]:
                self.camera.setPos(self.camera,dir.__mul__(5*dt))
        return Task.cont

    def mouseWatchTask(self, task):
        """Update the camera to the mouse's movement."""
        mw = base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            dx, dy = mw.getMouseX(), mw.getMouseY()
        else:
            dx, dy = 0, 0
        self.recenterMouse()

        self.camera.setH(self.camera.getH()-20*dx)
        p=self.camera.getP()+40*dy
        if p<-90:
            self.camera.setP(-90)
        elif p>90:
            self.camera.setP(90)
        else:
            self.camera.setP(p)
        self.debugText.setText("Pitch: {}".format(self.camera.getP()))
        return Task.cont

app=MyApp()
app.run()
