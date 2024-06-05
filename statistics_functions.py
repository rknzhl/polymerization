import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from protein_model import ProteinModel
from multiprocessing import Pool, cpu_count


def run_simulation_for_temperature(args):
    temp, len_beads, num_steps, mode = args
    model = ProteinModel(len_beads, temperature=temp, mode=mode)
    model.run_simulation(num_steps=num_steps, save_video=False)
    average_energy, heat_capacity = model.calculate_statistics()
    return temp, heat_capacity, average_energy


def run_cap_vs_temp(temp_range, len_beads, num_steps=100, mode='grid'):
    temperatures = []
    heat_capacities = []
    average_energies = []

    args = [(temp, len_beads, num_steps, mode) for temp in temp_range]

    with Pool(processes=cpu_count() - 2) as pool:
        for temp, heat_capacity, average_energy  in tqdm(pool.imap_unordered(run_simulation_for_temperature, args),
                                        total=len(temp_range), desc="Ход процесса"):
            temperatures.append(temp)
            heat_capacities.append(heat_capacity)
            average_energies.append(average_energy)

    return temperatures, heat_capacities, average_energies


def plot_heat_capacity_vs_temperature(temperatures, heat_capacities):
    # Сортировка данных по температуре
    sorted_indices = np.argsort(temperatures)
    sorted_temperatures = np.array(temperatures)[sorted_indices]
    sorted_heat_capacities = np.array(heat_capacities)[sorted_indices]

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_temperatures, sorted_heat_capacities, marker='o', linestyle='-', color='b', label='Heat Capacity')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Heat Capacity (a.u.)')
    plt.title('Heat Capacity vs Temperature')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_energy_vs_temperature(temperatures, average_energies):
    sorted_indices = np.argsort(temperatures)
    sorted_temperatures = np.array(temperatures)[sorted_indices]
    sorted_average_energies = np.array(average_energies)[sorted_indices]

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_temperatures, sorted_average_energies, marker='o', linestyle='-', color='b', label='Average Energy')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Average Energy (a.u.)')
    plt.title('Average Energy vs Temperature')
    plt.legend()
    plt.grid(True)
    plt.show()
