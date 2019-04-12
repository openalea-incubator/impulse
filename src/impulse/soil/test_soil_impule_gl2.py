#test soil impulse G Louarn v2
# couplage avec l'interface sol d'impulse - racines forcee dans une structure fixe par defaut (root)

import numpy as np

# import du sol 3ds + test
from soil3ds import soil_moduleN as solN
from soil3ds.test.test_init_soil import init_sol_test

# import de l'interface sol impulse
import impulse.soil.soil as soil_interface



########################
## exemple 1
## couplage + boucle avec uniquement transpiration plante
## (pas d'entree d'eau + pas d'evaporation du sol avec epsi=1.)
########################

nb_jours = 100
Rain = [0.]*nb_jours
Irrig = [0.]*nb_jours
epsi = [0.9999]*nb_jours #efficience d'interceptio plante ; 1: voit que effet transpi
Et0 = [0.5]*nb_jours #ETP (mm)



## creation d'un objet sol 3ds par defaut (S)
S = init_sol_test(pattern8 = [[-50.,-50.], [50.,50.]], dz=5., size=[10,10,30])
stateEV = [0.,0.,0.] #pour le calcul de l'evaporation du sol (memoire du cumul evapore depuis derniere PI)


#instancie un odjet sol 3D d'interface vide (mysoil) a partir de l'objet sol 3ds (S)
size_ = S.size[1:]+S.size[0:1] #passe z,x,y en xyz
dxyz_ = [S.dxyz[0][0], S.dxyz[1][0], S.dxyz[2][0]]
origin = S.origin


mysoil = soil_interface.Soil3D(origin, size_, dxyz_)


## Boucle jounaliere
for j in range(nb_jours):

    #remplissage des valeurs de propriete de l'interface a partir du contenu de l'ojet 3ds et et d'une liste de propriete dediees
    properties_3ds = ['asw_t', 'tsw_t', 'Corg', 'Norg', 'm_NO3', 'm_NH4', 'm_soil_vol', 'm_Tsol', 'm_DA', 'ftsw_t']
    # signification des properties:
    # asw_t : quantite d'eau libre pour plante dans le voxel au temps t (mm)
    # tsw_t : quantite d'eau totale dans le voxel au temps t (mm)
    # ftsw_t : fraction d'eau ranspirable = asw_t/tsw_t
    # m_soil_vol : volume des voxels (m3)
    # m_DA : densite apparente du sol par voxel (g.cm-3)
    # m_Tsol: Temperature sol (degreC - entree actuellement forcee par meteo)
    # Corg: (kg C dans le voxel)
    # Norg: (kg N dans le voxel)
    # m_NH4: (kg N NH4 dans le voxel)
    # m_NO3: (kg N NO3 dans le voxel)


    #mysoil.m
    mysoil.set_3ds_properties(S, properties_3ds)
    #mysoil.m

    # mise a jour d'une propriete root_density dans mysoil
    mysoil.add_property('root_density', default_value = 0.)
    mysoil.m['root_density'][:,:,0] = 50.
    mysoil.m['root_density'][:,:,1] = 10.


    #lecure de root_density dans l'interface sol et construction du ls_root pour 3ds
    #resh = np.reshape(mysoil.m['root_density'], S.size)#reshape z,x,y pour 3ds
    #reshape remet pas les racines dans l'ordre que je veux!!!??
    root = np.zeros(S.size)
    for i in range(S.size[0]): root[i,:,:] = mysoil.m['root_density'][:,:,i]
    ls_roots = [root]#liste des systemes racinaires des differentes plantes


    #step de water balance
    ls_transp, evapo_tot, ls_drainage, stateEV,  ls_m_transpi, m_evap, ls_ftsw = S.stepWBmc(Et0[j], ls_roots, [epsi[j]], Rain[j], Irrig[j], stateEV)

    print j, ls_ftsw[0] #print de la fraction d'eau disponible percue par le systeme racinaire







#test des reshape

#ord='C'

#x = np.ones([2,3,4], order=ord)
#x[1,:,:] =0.

#y = np.reshape(x, [3,4,2], order=ord)
#y[:,:,0]

#z = np.reshape(y, [2,3,4], order=ord)







