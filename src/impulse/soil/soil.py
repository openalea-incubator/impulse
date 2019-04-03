import numpy as np

default_properties = ['Qwater', 'Volume_vox', 'Qnorg' , 'Qcorg', 'QNO3', 'QNH4', 'DA', 'Resist' ]

class Soil3D(object):
    def __init__(self, size, dxyz, origin, properties):
        """ m: dictionnary of 3D numpy grids of the different quantitative properties
        (filled with ones)
            size: number of voels along z:x:y axes
            dxyz: voxel dimensions along x,y,z
            origin: position of the first voxel (0,0,0) """

        self.size = size
        self.origin = origin
        self.dxyz = dxyz
        self.m = {}
        for p in properties:
            self.m[p] = np.ones(size)

    def properties(self):
        return self.m

    def add_property(name, type=np.float):
        self.m[name]= np.ones(self.size, dtype=type)

    def property_names(self):
        return self.m.keys()

    def plot(self, cm='jet', property_name='QWater'):
        "return Plantgl scene"
        from openalea.plantgl.all import Scene
        if property_name not in self.property_names():
            pass
        return Scene()

