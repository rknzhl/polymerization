import numpy as np

class ProteinModelBase:
    def __init__(self, len_beads, temperature=300, mode = 'grid'):
        if mode == 'grid':
            self.len_beads = len_beads
            self.num_beads = len_beads ** 3
        if mode == 'random':
            self.len_beads = len_beads
            self.num_beads = len_beads

        self.positions = np.zeros((self.num_beads, 3))
        self.temperature = temperature
        self.kB = 1.38e-23
        self.spring_constant = 1.0
        self.bond_length = 1.0
        self.sigma = 1.5
        self.e = 1.2
        self.energy_arr = []
        self.mode = mode
        if self.mode == 'grid':
            self._initialize_grid()
        elif self.mode == 'random':
            self._initialize_random()
        else:
            raise ValueError("Неправильный формат. Надо 'grid' или 'random'.")


    def _initialize_grid(self):
        index = 0
        for z in range(self.len_beads):
            if z % 2 == 1:
                for y in range(self.len_beads):
                    if y % 2 == 1:
                        for x in range(self.len_beads):
                            self.positions[index] = [x, y, z]
                            index += 1
                    else:
                        for x in range(self.len_beads - 1, -1, -1):
                            self.positions[index] = [x, y, z]
                            index += 1
            else:
                for y in range(self.len_beads - 1, -1, -1):
                    if y % 2 == 0:
                        for x in range(self.len_beads):
                            self.positions[index] = [x, y, z]
                            index += 1
                    else:
                        for x in range(self.len_beads - 1, -1, -1):
                            self.positions[index] = [x, y, z]
                            index += 1

    def _initialize_random(self):
        self.positions[0] = np.array([0, 0, 0])  # Начальная позиция
        for i in range(1, self.num_beads):
            while True:
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                random_direction = np.array([
                    np.sin(phi) * np.cos(theta),
                    np.sin(phi) * np.sin(theta),
                    np.cos(phi)
                ])
                new_position = self.positions[i - 1] + random_direction
                if not any(np.all(new_position == self.positions[:i], axis=1)):
                    self.positions[i] = new_position
                    break

    def get_positions(self):
        return self.positions