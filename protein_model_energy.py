import numpy as np
class ProteinModelEnergyMixin:
    def energy(self):
        energy = 0.0
        for i in range(1, self.num_beads):
            displacement = (self.positions[i] - self.positions[i - 1])*self.bond_length
            bond_distance = np.linalg.norm(displacement)
            energy += 0.5 * self.spring_constant * (bond_distance - self.bond_length) ** 2
        for i in range(0, self.num_beads):
            for j in range(i + 1, self.num_beads):  # Исключаем дублирование и самовзаимодействие
                displacement = (self.positions[i] - self.positions[j]) * self.bond_length
                bond_distance = np.linalg.norm(displacement)
                if bond_distance != 0:
                    energy += (self.sigma2 / (bond_distance) ** 12 - self.sigma1 / (bond_distance)**6)
        return energy

