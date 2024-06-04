import numpy as np


class ProteinModelMonteCarloMixin:
    def monte_carlo_step(self):
        for i in range(self.num_beads):
            old_position = np.copy(self.positions[i])
            random_displacement = np.random.normal(0, 0.1, 3)
            random_sign = np.random.choice([-1, 1], size=1)
            self.positions[i] += random_sign * random_displacement
            old_energy = self.energy()
            new_energy = self.energy()
            delta_e = new_energy - old_energy
            if delta_e > 0:
                probability = np.exp(-delta_e / (self.kB * self.temperature))
                if np.random.rand() > probability:
                    self.positions[i] = old_position
