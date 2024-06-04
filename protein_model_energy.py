import numpy as np
class ProteinModelEnergyMixin:
    def energy(self):
        energy = 0.0
        for i in range(1, self.num_beads):
            displacement = self.positions[i] - self.positions[i - 1]
            bond_distance = np.linalg.norm(displacement)
            energy += 0.5 * self.spring_constant * (bond_distance - self.bond_length) ** 2
        return energy