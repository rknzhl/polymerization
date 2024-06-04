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
        self.sigma = 4
        self.e = 1

        index = 0

        for z in range(len_beads):
            if z % 2 == 1:
                for y in range(len_beads):
                    if y % 2 == 1:
                        for x in range(len_beads):
                            self.positions[index] = [x, y, z]
                            index += 1
                    else:
                        for x in range(len_beads - 1, -1, -1):
                            self.positions[index] = [x, y, z]
                            index += 1
            else:
                for y in range(len_beads - 1, -1, -1):
                    if y % 2 == 0:
                        for x in range(len_beads):
                            self.positions[index] = [x, y, z]
                            index += 1
                    else:
                        for x in range(len_beads - 1, -1, -1):
                            self.positions[index] = [x, y, z]
                            index += 1

    def get_positions(self):
        return self.positions