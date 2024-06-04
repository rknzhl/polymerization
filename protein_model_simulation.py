import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

from datetime import datetime
from tqdm import tqdm

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
        bar_format = "{l_bar}%s{bar}%s{r_bar}" % ('\033[92m', '\033[0m')
        for step in tqdm(range(num_steps), desc="Cимуляция процесса", bar_format = bar_format):
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
        imageio.mimsave(video_path, frames, fps=10, codec='mpeg4', quality=10)
        print(f'Видео сохранено в {video_path}')
