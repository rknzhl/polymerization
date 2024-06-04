import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio
from datetime import datetime
import os


class ProteinModelSimulationMixin:
    def run_simulation(self, num_steps=100):
        frames = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlim([-self.len_beads/2, self.len_beads])
        ax.set_ylim([-self.len_beads/2, self.len_beads])
        ax.set_zlim([-self.len_beads/2, self.len_beads])

        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        ax.xaxis.pane.set_edgecolor('w')
        ax.yaxis.pane.set_edgecolor('w')
        ax.zaxis.pane.set_edgecolor('w')
        print(f'Начало симуляции с количеством шагов: {num_steps}')
        for step in range(num_steps):
            ax.clear()

            # Отображение молекул
            ax.scatter(self.positions[:, 0], self.positions[:, 1], self.positions[:, 2], c='blue', s=100)

            # Отображение соединений между молекулами
            for i in range(1, self.num_beads):
                x_values = [self.positions[i - 1, 0], self.positions[i, 0]]
                y_values = [self.positions[i - 1, 1], self.positions[i, 1]]
                z_values = [self.positions[i - 1, 2], self.positions[i, 2]]
                ax.plot(x_values, y_values, z_values, c='red')

            plt.title(f'Step {step + 1}')

            ax.set_xlim([-self.len_beads / 2, self.len_beads])
            ax.set_ylim([-self.len_beads / 2, self.len_beads])
            ax.set_zlim([-self.len_beads / 2, self.len_beads])

            plt.draw()
            fig.canvas.draw()

            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(image)

            self.monte_carlo_step()

        plt.close()

        # Создание папки, если она не существует
        if not os.path.exists('videos'):
            os.makedirs('videos')

        # Сохранение в видео
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = f'videos/simulation_{current_time}.mp4'
        with imageio.get_writer(video_path, fps=10) as writer:
            for frame in frames:
                writer.append_data(frame)
        print(f'Видео сохранено в {video_path}')
