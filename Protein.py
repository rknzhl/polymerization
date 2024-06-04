import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio.v3 as iio
from datetime import datetime
import os


class ProteinModel:
    def __init__(self, len_beads, temperature=300):
        self.len_beads = len_beads
        self.num_beads = len_beads ** 3
        self.temperature = temperature
        self.kB = 1.38e-23
        self.positions = np.zeros((self.num_beads, 3))
        self.spring_constant = 1.0
        self.bond_length = 1.0

        index = 0
        for x in range(len_beads):
            for y in range(len_beads):
                for z in range(len_beads):
                    self.positions[index] = [x, y, z]
                    index += 1

    def energy(self):
        energy = 0.0
        for i in range(1, self.num_beads):
            displacement = self.positions[i] - self.positions[i - 1]
            bond_distance = np.linalg.norm(displacement)
            energy += 0.5 * self.spring_constant * (bond_distance - self.bond_length) ** 2
        return energy

    def monte_carlo_step(self):
        for i in range(self.num_beads):
            old_position = np.copy(self.positions[i])
            random_displacement = np.random.normal(0, 0.1, 3)
            self.positions[i] += random_displacement
            old_energy = self.energy()
            new_energy = self.energy()
            delta_e = new_energy - old_energy
            if delta_e > 0:
                probability = np.exp(-delta_e / (self.kB * self.temperature))
                if np.random.rand() > probability:
                    self.positions[i] = old_position

    def run_simulation(self, num_steps=100):
        frames = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlim([0, self.len_beads + 1])
        ax.set_ylim([0, self.len_beads + 1])
        ax.set_zlim([0, self.len_beads + 1])

        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        ax.xaxis.pane.set_edgecolor('w')
        ax.yaxis.pane.set_edgecolor('w')
        ax.zaxis.pane.set_edgecolor('w')
        print(f'Начало симуляции с количеством шагов: {num_steps}')
        for step in range(num_steps):
            self.monte_carlo_step()
            ax.clear()
            ax.scatter(self.positions[:, 0], self.positions[:, 1], self.positions[:, 2], c='blue', s=100)
            plt.title(f'Step {step + 1}')

            ax.set_xlim([0, self.len_beads])
            ax.set_ylim([0, self.len_beads])
            ax.set_zlim([0, self.len_beads])

            plt.draw()
            fig.canvas.draw()

            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(image)

        plt.close()

        # Создание папки, если она не существует
        if not os.path.exists('videos'):
            os.makedirs('videos')

        # Сохранение в видео
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = f'videos/simulation_{current_time}.mp4'
        iio.imsave(video_path, frames, fps=10)
        print(f'Видео сохранено в {video_path}')

    def get_positions(self):
        return self.positions
