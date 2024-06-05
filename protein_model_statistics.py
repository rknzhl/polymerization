import numpy as np
from matplotlib import pyplot as plt


class ProteinModelStatisticsMixin:
    def calculate_statistics(self):
        # Используем последние 75% данных
        n = len(self.energy_arr)
        energy_arr = np.array(self.energy_arr[int(0.25 * n):])
        sq_energy_arr = energy_arr ** 2

        average_energy_sq = np.mean(sq_energy_arr)
        average_energy = np.mean(energy_arr)
        c_tepl = (average_energy_sq - average_energy**2) / (self.kB * (self.temperature**2))

        return average_energy, c_tepl

    def plot_energy(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.energy_arr, label='Энергия')
        plt.xlabel('Шаг симуляции')
        plt.ylabel('Энергия системы')
        plt.title('Энергия от шага симуляции')
        plt.legend()
        plt.grid(True)
        plt.show()