import matplotlib.pyplot as plt

from protein_model import ProteinModel


def run_simulation_for_temperatures(temp_range, len_beads, num_steps=1000, mode='random'):
    temperatures = []
    heat_capacities = []

    for temp in temp_range:
        model = ProteinModel(len_beads, temperature=temp, mode=mode)
        model.run_simulation(num_steps=num_steps)
        average_energy, heat_capacity = model.calculate_statistics()
        temperatures.append(temp)
        heat_capacities.append(heat_capacity)

    return temperatures, heat_capacities


def plot_heat_capacity_vs_temperature(temperatures, heat_capacities):
    plt.figure(figsize=(10, 6))
    plt.plot(temperatures, heat_capacities, marker='o', linestyle='-', color='b', label='Heat Capacity')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Heat Capacity (a.u.)')
    plt.title('Heat Capacity vs Temperature')
    plt.legend()
    plt.grid(True)
    plt.show()