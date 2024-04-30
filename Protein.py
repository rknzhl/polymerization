import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ProteinModel:
    def __init__(self, len_beads, temperature=300):
        self.len_beads = len_beads
        self.num_beads = len_beads ** 3
        self.temperature = temperature
        self.kB = 1.38e-23
        self.positions = np.zeros((self.num_beads, 3))
        self.spring_constant = 1.0  # примерно значение пружинной константы
        self.bond_length = 1.0  # примерное значение длины связи

        index = 0
        for x in range(len_beads):
            for y in range(len_beads):
                for z in range(len_beads):
                    self.positions[index] = [x, y, z]
                    index += 1

    def energy(self):
        """ Рассчитать энергию системы на основе текущих позиций """
        energy = 0.0
        for i in range(1, self.num_beads):
            displacement = self.positions[i] - self.positions[i - 1]
            bond_distance = np.linalg.norm(displacement)
            energy += 0.5 * self.spring_constant * (bond_distance - self.bond_length) ** 2
        return energy

    def monte_carlo_step(self):
        """ Выполнить один шаг Монте-Карло """
        for i in range(self.num_beads):
            old_position = np.copy(self.positions[i])
            random_displacement = np.random.normal(0, 0.1, 3)  # случайное смещение
            self.positions[i] += random_displacement
            old_energy = self.energy()
            new_energy = self.energy()
            delta_e = new_energy - old_energy
            if delta_e > 0:
                probability = np.exp(-delta_e / (self.kB * self.temperature))
                if np.random.rand() > probability:
                    self.positions[i] = old_position  # отклонить изменение

    def run_simulation(self, num_steps=100):
        """ Запустить симуляцию """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for step in range(num_steps):
            self.monte_carlo_step()
            ax.clear()
            ax.scatter(self.positions[:, 0], self.positions[:, 1], self.positions[:, 2])
            plt.pause(0.05)  # Пауза для отображения gi
        plt.show()

    def get_positions(self):
        """ Получить текущие позиции """
        return self.positions

# Использование класса
model = ProteinModel(len_beads=4)
model.run_simulation(num_steps=1)
