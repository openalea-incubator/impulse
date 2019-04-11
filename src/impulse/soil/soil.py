import numpy as np
import openalea.plantgl.all as pgl
from math import floor

default_properties = ['Qwater', 'Volume_vox', 'Qnorg' , 'Qcorg', 'QNO3', 'QNH4', 'DA', 'Resist' ]

class Soil3D(object):
    def __init__(self, origin = (0,0,0), size = (100,100,100), dxyz = (1,1,1),  properties = {}, toric = (True,True,False)):
        """ m: dictionnary of 3D numpy grids of the different quantitative properties
        (filled with ones)
            origin: position of the first voxel (0,0,0) 
            size: number of voxels along z:x:y axes
            dxyz: voxel dimensions along x,y,z
            toric: define for each dimension if the grid is toric
            """

        self.maxdimension = 3
        self.toric = toric
        self.origin = np.array(origin)
        self.size = np.array(size)
        self.dxyz = np.array(dxyz)
        #self.gridindexing = pgl.Grid3Indexing( dxyz, origin, self.upper())
        self.m = {}
        for p, v in properties:
            self.add_property(p,v)

    def iindex(self, i, coord):
        val = int(floor((coord - self.origin[i]) / self.dxyz[i])) 
        if self.toric[i] : val = val % self.size[i]
        return val

    def indexFromPoint(self, pos):
        res = [self.iindex(i, posi) for i, posi in enumerate(pos)]
        return tuple(res)

    #def indexFromPoint(self, pos):
    #    return self.gridindexing.indexFromPoint(pos)

    def upper(self):
        return [self.origin[i] + self.size[i]*self.dxyz[i] for i in range(self.maxdimension)]

    def getVoxelCenter(self, index):
        return self.origin + self.dxyz*index + self.dxyz*0.5

    def properties(self):
        return self.m

    def add_property(self, name, default_value = 1, type=np.float):
        try :
            assert default_value.shape == self.size
            self.m[name] = default_value
        except:
            self.m[name]= np.ones(self.size, dtype=type) * default_value

    def property(self, name):
        return self.m[name]

    def property_names(self):
        return self.m.keys()

    def pgl_representation(self, cm='jet', property_name='QWater', sizeratio = 0.1, transparency = 0, minvalue = None, maxvalue = None, scalefunc = None, cmview = False):
        """ return Plantgl scene """
        if property_name not in self.property_names(): return

        mproperty = self.property(property_name)
        if (not scalefunc is None) and ((not minvalue is None) or (not maxvalue is None)):
            vscalefunc = np.vectorize(scalefunc)
            mproperty = vscalefunc(mproperty)
        minvalue = mproperty.min() if minvalue is None else minvalue
        maxvalue = mproperty.max() if maxvalue is None else maxvalue
        colormap = pgl.PglMaterialMap(minvalue, maxvalue, cm)
        sc = pgl.Scene()
        vsize = np.array(self.dxyz)*sizeratio/2.
        it = np.nditer(self.property(property_name), flags=['multi_index'])
        while not it.finished:                  
            idx, value = it.multi_index, it[0]
            if not scalefunc is None : value = scalefunc(value)
            if minvalue <= value <= maxvalue:
                mat = colormap(value)
                mat.transparency = transparency
                sc += pgl.Shape(pgl.Translated(self.getVoxelCenter(idx),
                                               pgl.Box(vsize)),
                                mat)
            it.iternext()

        if cmview:
            sc += colormap.pglrepr()
        return sc

    def getValueAt(self, property_name, pos):
        cid = self.indexFromPoint(pos)
        return self.property(property_name)[cid]

    def setValueAt(self, property_name, pos, value):
        self.property(property_name)[self.indexFromPoint(pos)] = value

    def incValueAt(self, property_name, pos, value):
        self.property(property_name)[self.indexFromPoint(pos)] += value

    def setLayerValue(self, property_name, layerdimension, layervalue, value):
        """
        An operator to assign directly a layer of the soil
        Example :
            # To assign a Z layer with a given value of Water
            soil.setLayerValue('QWater', 2, range(0,3), 5)
        """
        assert 0 <= layerdimension < self.maxdimension
        indices = [slice(None) for i in xrange(self.maxdimension)]
        indices[layerdimension] = layervalue
        indices = tuple(indices)

        expectedshape = list(self.size)
        try:
            expectedshape[layerdimension] = len(layervalue)
        except:
            expectedshape[layerdimension] = 1

        self.property(property_name)[indices] = value

    def setSliceValue(self, property_name, xslice = slice(None), yslice = slice(None), zslice = slice(None), value = None):
        self.property(property_name)[xslice,yslice,zslice] = value

    def set_3ds_properties(self, Smodel_obj, ls_properties):
        """ set a list of properties for 3ds soil model from  Smodel_obj"""
        for p in ls_properties:
            vals = getattr(Smodel_obj, p)#comme Smodel_obj.property_name, mais acces par nom
            reshaped_vals = np.reshape(vals, self.size)#reshape x,y,z
            self.add_property(p, reshaped_vals)

    def __getattr__(self, name):
        try:
            self.__getattribute__(name)
        except:
            try:
                return self.m[name]
            except:
                raise AttributeError(name)

    def __contains__(self,pos):
        return pgl.BoundingBox(self.getLowerCorner(),self.getUpperCorner()-(1e-5,1e-5,1e-5)).contains(pos)
