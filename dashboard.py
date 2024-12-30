from flask import Flask, jsonify, send_from_directory
import json

app = Flask(__name__)

@app.route('/simulation-data')
def simulation_data():
    with open('simulation_data.json', 'r') as f:
        data = json.load(f)
    return jsonify({'final_vehicle_counts': data['final_vehicle_counts']})

@app.route('/')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

if __name__ == "__main__":
    app.run(port=5500, debug=True)  # Ensure the port matches the one you're using
