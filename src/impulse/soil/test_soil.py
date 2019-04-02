import numpy as np


class Soil3D(object):
    def __init__(self,size, dxyz, origin, properties):
        """ m: dictionnary of 3D numpy grids of the different quantitative properties (filled with ones)
            size: number of voels along z:x:y axes
            dxyz: voxel dimensions along x,y,z
            origin: position of the first voxel (0,0,0) """

        self.size = size
        self.origin = origin
        self.dxyz = dxyz
        self.m = {}
        for p in properties:
            self.m[p] = np.ones(size)


dxyz = [1.,1.,2.]#cm
size = [5,3,3] #z,x,y
origin = np.array([0.,0.,0.])
properties = ['Qwater', 'Volume_vox', 'Qnorg' , 'Qcorg', 'QNO3', 'QNH4', 'DA', 'Resist' ]

mysoil = Soil3D(size, dxyz, origin, properties)
mysoil.m['Qwater'][0,:,:]











soil = {}
for p in properties:
    soil[p] = np.zeros(nbv)

#inititalisation


soil['Qwater'][0,:,:]


import pandas as pd

