from impulse.root import root_mtg
from openalea.plantgl.all import Viewer

g = root_mtg.mtg_root()

s = root_mtg.Simulate(g)

for i in range(100):
    s.step()
    scene = root_mtg.plot(g)
    Viewer.display(scene)


