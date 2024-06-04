import numpy as np

class ProteinModelBase:
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

    def get_positions(self):
        return self.positions