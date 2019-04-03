import numpy as np

from impulse.soil import soil

dxyz = [1.,1.,2.]#cm
size = [5,3,3] #z,x,y
origin = np.array([0.,0.,0.])
properties = ['Qwater', 'Volume_vox', 'Qnorg' , 'Qcorg', 'QNO3', 'QNH4', 'DA', 'Resist' ]

mysoil = soil.Soil3D(size, dxyz, origin, properties)
mysoil.m['Qwater'][0,:,:]

