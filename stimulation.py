from flask import Flask, request, jsonify
import numpy as np
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes of your Flask app

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    num_spins = data.get('num_spins', 100)
    magnetic_field_strength = data.get('magnetic_field_strength', 1.0)  # Magnetic Field Strength in Tesla (T)
    time_steps = data.get('time_steps', 10)  # Time Steps in seconds (s)
    time_step_duration = data.get('time_step_duration', 0.01)  # Time Step Duration in seconds (s)
    resonance_frequency = data.get('resonance_frequency', 1.0)  # Resonance Frequency in Hertz (Hz)

    spins = initialize_spins(num_spins)
    energy_levels = []
    energies = []

    for step in range(time_steps):
        total_magnetic_moment = calculate_total_magnetic_moment(spins)
        torque = calculate_torque(total_magnetic_moment, magnetic_field_strength)
        spins = update_spin_orientations(spins, torque, time_step_duration)
        energy = calculate_total_energy(spins, magnetic_field_strength)
        energies.append(energy)
        if np.isclose(abs(energy), resonance_frequency):
            energy_levels.append(energy)
            break

    simulation_result = {
        'timestamp': str(datetime.now()),
        'spins': spins.tolist(),
        'energy_levels': energy_levels,
        'energies': energies
    }
    save_simulation_result(simulation_result)
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
