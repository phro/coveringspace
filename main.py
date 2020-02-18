from math import sin, cos, pi

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties
import sys

# Debugging
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class MyApp(ShowBase):

    def recenterMouse(self):
        self.win.movePointer(0,
              int(self.win.getProperties().getXSize() / 2),
              int(self.win.getProperties().getYSize() / 2))

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.plane = self.loader.loadModel("models/plane.bam")
        self.plane.reparentTo(self.render)
        self.cube = self.loader.loadModel("models/cube.bam")
        self.cube.reparentTo(self.render)

        self.accept('a', lambda: self.recenterMouse())

        self.accept('escape', sys.exit, [0])

        self.camera.setPos(0,-20,3)
        self.cube.setPos(0,0,1)
        self.camera.lookAt(self.cube)

        self.taskMgr.add(self.updateCameraTask, "Update Camera Task")

        self.mouseText = self.genLabelText("",1)
        self.lastMouseX, self.lastMouseY = None, None
        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_confined)
        wp.setCursorHidden(True)
        self.win.requestProperties(wp)

    def genLabelText(self, text, i):
        text = OnscreenText(text = text, pos = (-1.3, .5-.05*i), fg=(0,1,0,1),
                      align = TextNode.ALeft, scale = .05)
        return text

    def updateCameraTask(self, task):
        """Update the camera to the mouse's movement."""
        mw = base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            dx, dy = mw.getMouseX(), mw.getMouseY()
        else:
            dx, dy = 0, 0
        self.mouseText.setText("(dx,dy) = ({},{})".format(dx,dy))
        self.recenterMouse()

        self.camera.setH(self.camera.getH()+20*dx)
        p=self.camera.getP()-20*dy
        #  self.mouseText.setText("(x,y) = ({},{}), (dx,dy) = ({},{})".format(x,y,dx,dy))
        #  self.mouseText.setText("Camera Pitch: {}".format(p))
        if p<-20:
            self.camera.setP(-20)
        elif p>10:
            self.camera.setP(10)
        else:
            self.camera.setP(p)
        return Task.cont

app=MyApp()
app.run()
