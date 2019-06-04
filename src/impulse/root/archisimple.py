
from openalea.lpy import *
import os.path as op
import os

class ArchiSimpleModel:
    def __init__(self, **params):
        self.model = Lsystem(op.join(op.dirname(__file__), 'archisimple.lpy'), params)
        self.structure = self.model.axiom
        self.nbiter = 0

    def simulate(self, dt):
        nbiter = self.model.dt/dt
        self.structure = self.model.iterate(self.structure, self.nbiter, nbiter)
        self.nbiter += nbiter

    def structure(self):
        return LsMTG(self.structure)

    def plot(self):
        self.model.plot(self.structure)