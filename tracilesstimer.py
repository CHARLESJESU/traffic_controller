import os
import traci
import time

# Set the directory where the SUMO config file is located
os.chdir("E:/traffic signal/sumotest2/charles")

# Initialize SUMO simulation
sumoCmd = ["sumo-gui", "-c", "ssasda.sumocfg"]
traci.start(sumoCmd)

def set_traffic_signal_phase(junction_id, phase_index, states):
    state = states[phase_index]
    traci.trafficlight.setRedYellowGreenState(junction_id, state)

def get_vehicle_counts(edges):
    vehicle_counts = {}
    for edge in edges:
        vehicle_counts[edge] = traci.edge.getLastStepVehicleNumber(edge)
    return vehicle_counts

edges_of_interest = ["E0", "-E1", "-E2", "-E3"]
junction_id = "J1"

# Traffic light states for each phase
states = [
    "GGGGrrrrrrrrrrrr",  # Phase 1
    "yyyyrrrrrrrrrrrr",  # Phase 2
    "rrrrGGGGrrrrrrrr",  # Phase 3
    "rrrryyyyrrrrrrrr",  # Phase 4
    "rrrrrrrrGGGGrrrr",  # Phase 5
    "rrrrrrrryyyyrrrr",  # Phase 6
    "rrrrrrrrrrrrGGGG",  # Phase 7
    "rrrrrrrrrrrryyyy"   # Phase 8
]

final_vehicle_counts = []
cycle_count = 0
phase_start_time = traci.simulation.getTime()
in_phase_7 = False

# Phase durations for each cycle
phase_durations = [10, 5, 10, 5, 10, 5, 10, 5]

while traci.simulation.getMinExpectedNumber() > 0:
    current_time = traci.simulation.getTime()
    elapsed_time = current_time - phase_start_time

    cumulative_duration = 0
    for i, duration in enumerate(phase_durations):
        cumulative_duration += duration
        if elapsed_time < cumulative_duration:
            phase_index = i
            break

    if phase_index == 6 and not in_phase_7:
        cycle_count += 1
        in_phase_7 = True
        print(f"Cycle {cycle_count} is completed.")

        if cycle_count >= 3:
            live_vehicle_counts = get_vehicle_counts(edges_of_interest)
            final_vehicle_counts = [live_vehicle_counts[edge] for edge in edges_of_interest]
            print("Vehicle counts at the time cycle count reaches 3:")
            print(final_vehicle_counts)

    elif phase_index != 6:
        in_phase_7 = False

    # Set the traffic signal phase for the junction
    set_traffic_signal_phase(junction_id, phase_index, states)

    traci.simulationStep()

    if elapsed_time >= sum(phase_durations):
        phase_start_time = current_time

traci.close()
