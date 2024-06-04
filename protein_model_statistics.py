import numpy as np


class ProteinModelStatisticsMixin:
    def calculate_statistics(self):
        sq_energy_arr = []
        for i in range(len(self.energy_arr)):
            sq_energy_arr.append(self.energy_arr[i]**2)
        average_energy_sq = np.mean(sq_energy_arr)
        average_energy = np.mean(self.energy_arr)
        c_tepl = (average_energy_sq - average_energy**2)/(self.kB * (self.temperature**2))
        return average_energy, c_tepl