import openalea.mtg as mtg
import openalea.plantgl.all as pgl
from openalea.mtg import turtle as turt
from openalea.mtg.plantframe import color

#liste fonctions
# def plot(g, prop_cmap='radius', cmap='jet', lognorm=False):
#     """
#     Exemple:
#
#         >>> from openalea.plantgl.all import *
#         >>> s = plot()
#         >>> shapes = dict( (x.getId(), x.geometry) for x in s)
#         >>> Viewer.display(s)
#     """
#     visitor = get_root_visitor()
#
#     turtle = turt.PglTurtle()
#     turtle.down(180)
#     scene = turt.TurtleFrame(g, visitor=visitor, turtle=turtle, gc=False)
#
#     # Compute color from radius
#     color.colormap(g,prop_cmap, cmap=cmap, lognorm=lognorm)
#
#     shapes = dict((sh.getId(),sh) for sh in scene)
#
#     colors = g.property('color')
#     for vid in colors:
#         if vid in shapes:
#             shapes[vid].appearance = pgl.Material(colors[vid])
#     scene = pgl.Scene(shapes.values())
#     return scene


#liste des parametres
init1 = 100
init2 = 30

#creation de la struture MTG initiale
#
g = mtg.MTG()

#noeud principal de la plante avec pool de concentration
root =  g.add_component(g.root, label ='systracinaire')
nid = g.node(root)
nid.C1 = init1

#rajout de l'apex connecte au root
apex = g.add_child(root, label='A',edge_type='<')
nid_apex = g.node(apex)
nid_apex.C2 = init2
nid_apex.radius = 0.1
nid_apex.length = 2
nid_apex.cumulatedlength = 2
nid_apex.thr = 0.1

STEPS = 25
dt = 1
kv = 20
kz = 15
sgl = 20
ibd = 50
hierc = 0.75
rir =0.9*0.001


for tps in range(STEPS):
    for vtx in g.VtxList():
        if g.label(vtx)=='A':
            nid_apex = g.node(vtx)
            #vitesse d'allongement segment
            if nid_apex.radius<nid_apex.thr:
                nid_apex.radius += rir*nid_apex.C2
            else:
                v = (nid_apex.radius*2)*nid_apex.C2*kv*1/kz #kv constante de vitesse
                dl = v*dt
                nid_apex.length += dl
                nid_apex.cumulatedlength += dl

                print tps,nid_apex.length

                if nid_apex.length > sgl:
                    seg1 = g.add_child(vtx, label='S', edge_type='<')
                    nid_s1 = g.node(seg1)
                    nid_s1.C2 = nid_apex.C2
                    nid_s1.radius = nid_apex.radius
                    nid_s1.length = sgl

                    nid_apex.length = nid_apex.length - sgl

                    if nid_apex.cumulatedlength > ibd:
                        apexB = g.add_child(vtx, label='A', edge_type='+')
                        nid_apexB = g.node(apexB)
                        #nid_apex = g.node(apex)
                        nid_apexB.C2 = nid_apex.C2
                        nid_apexB.radius = 0.
                        nid_apexB.length = 0.
                        nid_apexB.cumulatedlength = 2
                        nid_apexB.thr = nid_apex.radius*hierc
                        nid_apex.cumulatedlength -= 0#ibd



