import numpy as np


class ProteinModelMonteCarloMixin:
    def monte_carlo_step(self):
        for i in range(self.num_beads):
            old_position = np.copy(self.positions[i])
            old_energy = self.energy()
            sum_dist = 0
            for j in range(1, self.num_beads):
                displacement = self.positions[j] - self.positions[j - 1]
                sum_dist += np.linalg.norm(displacement)
            av_dist = sum_dist / self.num_beads
            random_displacement = np.random.normal(0, 0.1 * av_dist, 3)
            self.positions[i] += random_displacement
            new_energy = self.energy()
            delta_e = new_energy - old_energy
            if delta_e > 0:
                probability = np.exp(-delta_e / (self.kB * self.temperature))
                if np.random.rand() > probability:
                    self.energy_arr.append(old_energy)
                    self.positions[i] = old_position
                else:
                    self.energy_arr.append(new_energy)
            else:
                self.energy_arr.append(new_energy)