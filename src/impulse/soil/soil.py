import numpy as np
import openalea.plantgl.all as pgl

default_properties = ['Qwater', 'Volume_vox', 'Qnorg' , 'Qcorg', 'QNO3', 'QNH4', 'DA', 'Resist' ]

class Soil3D(object):
    def __init__(self, origin = (0,0,0), size = (100,100,100), dxyz = (1,1,1),  properties = {}):
        """ m: dictionnary of 3D numpy grids of the different quantitative properties
        (filled with ones)
            size: number of voxels along z:x:y axes
            dxyz: voxel dimensions along x,y,z
            origin: position of the first voxel (0,0,0) """

        self.origin = origin
        self.size = size
        self.dxyz = dxyz
        self.gridindexing = pgl.Grid3Indexing( dxyz, origin, self.upper())
        self.m = {}
        for p, v in properties:
            self.add_property(p,v)

    def upper(self):
        return [self.origin[i] + self.size[i]*self.dxyz[i] for i in range(3)]

    def properties(self):
        return self.m

    def add_property(self, name, default_value = 1, type=np.float):
        try :
            assert len(default_value) == self.gridindexing.size()
            self.m[name] = default_value
        except:
            self.m[name]= np.ones(self.size, dtype=type) * default_value

    def property(self, name):
        return self.m[name]

    def property_names(self):
        return self.m.keys()

    def pgl_representation(self, cm='jet', property_name='QWater', sizeratio = 0.1):
        "return Plantgl scene"
        if property_name not in self.property_names(): return
        colormap = pgl.PglMaterialMap(self.property(property_name).min(),self.property(property_name).max(),cm)
        sc = pgl.Scene()
        for i, vi in enumerate(self.property(property_name)):
            for j, vj in enumerate(vi):
                    for k, v in enumerate(vj):
                        sc += pgl.Shape(pgl.Translated(self.gridindexing.getVoxelCenter([i,j,k]),pgl.Box(self.gridindexing.getVoxelSize()*sizeratio)),colormap(v),i)
        return sc

    def getValueAt(self, property_name, pos):
        cid = self.gridindexing.indexFromPoint(pos)
        return self.property(property_name)[cid]

    def setValueAt(self, property_name, pos, value):
        self.property(property_name)[self.gridindexing.indexFromPoint(pos)] = value

    def __contains__(self,pos):
        return pgl.BoundingBox(self.getLowerCorner(),self.getUpperCorner()-(1e-5,1e-5,1e-5)).contains(pos)
