from flask import Flask, request, jsonify
import numpy as np
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    print("Received simulation parameters:", data)  # Print received parameters for debugging
    num_spins = data['num_spins']
    magnetic_field_strength = data['magnetic_field_strength']  # Magnetic Field Strength in Tesla (T)
    time_steps = data['time_steps']  # Time Steps in seconds (s)
    time_step_duration = data['time_step_duration']  # Time Step Duration in seconds (s)
    resonance_frequency = data['resonance_frequency']  # Resonance Frequency in Hertz (Hz)
    
    spins = initialize_spins(num_spins)
    energy_levels = []
    energies = []  # List to store energy at each timestep

    for step in range(time_steps):
        total_magnetic_moment = calculate_total_magnetic_moment(spins)
        torque = calculate_torque(total_magnetic_moment, magnetic_field_strength)
        spins = update_spin_orientations(spins, torque, time_step_duration)
        energy = calculate_total_energy(spins, magnetic_field_strength)
        energies.append(energy)  # Store energy for each timestep
        print(f"Step {step+1}: Calculated energy = {energy}, Resonance frequency = {resonance_frequency} Hz")
        if np.isclose(abs(energy), resonance_frequency):
            energy_levels.append(energy)
            break

    simulation_result = {
        'timestamp': str(datetime.now()),
        'spins': spins.tolist(),
        'energy_levels': energy_levels,
        'energies': energies  # Include energies in the result
    }
    save_simulation_result(simulation_result)
    print("Simulation results saved to file.")
    return jsonify(simulation_result)

def save_simulation_result(simulation_result):
    with open('simulation_results.json', 'a') as file:
        json.dump(simulation_result, file)
        file.write('\n')

def initialize_spins(num_spins):
    return np.random.choice([-1, 1], size=num_spins)

def calculate_total_magnetic_moment(spins):
    return np.sum(spins)

def calculate_torque(total_magnetic_moment, magnetic_field_strength):
    return total_magnetic_moment * magnetic_field_strength

def update_spin_orientations(spins, torque, time_step_duration):
    angle_change = torque * time_step_duration
    return spins * np.cos(angle_change)

def calculate_total_energy(spins, magnetic_field_strength):
    return -np.sum(spins) * magnetic_field_strength

if __name__ == '__main__':
    app.run(debug=True)
