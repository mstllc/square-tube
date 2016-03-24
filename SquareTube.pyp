import os
import math
import c4d

from c4d import plugins, utils, bitmaps

PLUGIN_ID = 1037029

class SquareTube(plugins.ObjectData):

    def __init__(self):
        self.SetOptimizeCache(True)

    def Init(self, op):
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_LENGTH])
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_WIDTH])
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_DEPTH])
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_THICKNESS])
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_TOP_ANGLE])
        self.InitAttr(op, float, [c4d.PY_SQUARETUBE_BOTTOM_ANGLE])

        op[c4d.PY_SQUARETUBE_LENGTH] = 60.96
        op[c4d.PY_SQUARETUBE_WIDTH] = 5.08
        op[c4d.PY_SQUARETUBE_DEPTH] = 5.08
        op[c4d.PY_SQUARETUBE_THICKNESS] = 0.1651
        op[c4d.PY_SQUARETUBE_TOP_ANGLE] = 0.0
        op[c4d.PY_SQUARETUBE_BOTTOM_ANGLE] = 0.0
        op[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP

        return True

    def GetVirtualObjects(self, op, hh):
        tube = c4d.PolygonObject(16, 16)
        if tube is None: return None

        length = op[c4d.PY_SQUARETUBE_LENGTH]
        if length is None: length = 60.96
        width = op[c4d.PY_SQUARETUBE_WIDTH]
        if width is None: width = 5.08
        depth = op[c4d.PY_SQUARETUBE_DEPTH]
        if depth is None: depth = 5.08
        thickness = op[c4d.PY_SQUARETUBE_THICKNESS]
        if thickness is None: thickness = 0.1651
        topa = op[c4d.PY_SQUARETUBE_TOP_ANGLE]
        if topa is None: topa = 0.0
        bota = op[c4d.PY_SQUARETUBE_BOTTOM_ANGLE]
        if bota is None: bota = 0.0

        ohw = width / 2
        ohd = depth / 2
        ihw = ohw - thickness
        ihd = ohd - thickness
        hl = length / 2

        lastat = 90 - math.degrees(topa)
        offsetOuterT = (depth * math.sin(topa)) / math.sin(math.radians(lastat))
        offsetInnerT = ((depth - thickness) * math.sin(topa)) / math.sin(math.radians(lastat))
        offsetCloseT = (thickness * math.sin(topa)) / math.sin(math.radians(lastat))

        lastab = 90 - math.degrees(bota)
        offsetOuterB = (depth * math.sin(bota)) / math.sin(math.radians(lastab))
        offsetInnerB = ((depth - thickness) * math.sin(bota)) / math.sin(math.radians(lastab))
        offsetCloseB = (thickness * math.sin(bota)) / math.sin(math.radians(lastab))

        for i in xrange(4):
            mod = (i + 1) % 4
            if i == 0:
                outer = c4d.Vector(ohw, -hl, ohd)
                inner = c4d.Vector(ihw, -hl, ihd)
                too = 0
                toi = offsetCloseT
                boo = 0
                boi = offsetCloseB
            elif i == 1:
                outer = c4d.Vector(ohw, -hl, -ohd)
                inner = c4d.Vector(ihw, -hl, -ihd)
                too = offsetOuterT
                toi = offsetInnerT
                boo = offsetOuterB
                boi = offsetInnerB
            elif i == 2:
                outer = c4d.Vector(-ohw, -hl, -ohd)
                inner = c4d.Vector(-ihw, -hl, -ihd)
                too = offsetOuterT
                toi = offsetInnerT
                boo = offsetOuterB
                boi = offsetInnerB
            elif i == 3:
                outer = c4d.Vector(-ohw, -hl, ohd)
                inner = c4d.Vector(-ihw, -hl, ihd)
                too = 0
                toi = offsetCloseT
                boo = 0
                boi = offsetCloseB

            tube.SetPoint(i, outer + c4d.Vector(0, boo, 0)) # Outer Bottom 0 - 3
            tube.SetPoint(i + 4, inner + c4d.Vector(0, boi, 0)) # Inner Bottom 4 - 7
            tube.SetPoint(i + 8, outer + c4d.Vector(0, length - too, 0)) # Outer Top 8 - 11
            tube.SetPoint(i + 12, inner + c4d.Vector(0, length - toi, 0)) # Inner Top 12 - 15
            tube.SetPolygon(i, c4d.CPolygon(i, mod, mod + 4, i + 4)) # Bottom Cap 0 - 3
            tube.SetPolygon(i + 4, c4d.CPolygon(i, mod, mod + 8, i + 8)) # Outer Wall 4 - 7
            tube.SetPolygon(i + 8, c4d.CPolygon(i + 8, mod + 8, mod + 12, i + 12)) # Top Cap 8 - 11
            tube.SetPolygon(i + 12, c4d.CPolygon(i + 12, mod + 12, mod + 4, i + 4)) # Inner Wall 12 - 15

        tube.Message(c4d.MSG_UPDATE)
        #tube.SetPhong(True, 1, utils.Rad(80.0))
        tube.SetName(op.GetName())
        return tube

if __name__ == "__main__":
    # Delete symbol cache if present
    path = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) + "/symbolcache"
    if os.path.exists(path):
        os.remove(path)

    dir, file = os.path.split(__file__)
    icon = bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(dir, "res", "icon-square-tube.tif"))

    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="SquareTube", g=SquareTube, description="squaretube", icon=icon, info=c4d.OBJECT_GENERATOR)
