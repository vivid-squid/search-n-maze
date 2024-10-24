# import Generate_maze as GM
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import argparse
import os
import csv 

sys.setrecursionlimit(50000)

def load_from_csv(maze_file):
    with open(maze_file, mode='r') as file:
        reader = csv.reader(file)
        maze = [list(map(int, row)) for row in reader]
    return np.array(maze)

def draw_maze(maze, policy, start, end):
    rows, cols = len(maze), len(maze[0])
    img = np.zeros((rows, cols), dtype=np.uint8)
    img[maze == 0] = 255
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    current = start
    while current != end and current in policy:
        plt.scatter(current[1], current[0], c='b', marker='o')
        move = policy[current]
        
        if move == 'up' and current[0] > 0:
            current = (current[0]-1, current[1])
        elif move == 'down' and current[0] < rows - 1:
            current = (current[0] + 1, current[1])
        elif move == 'left' and current[1] > 0:
            current = (current[0], current[1]-1)
        elif move == 'right' and current[1] < cols - 1:
            current = (current[0], current[1]+1)
        else:
            print("Invalid move or out of bounds:", current, move)
            break

        plt.pause(0.0001)
    plt.scatter(end[1], end[0], c='b', marker='o')
    plt.show()

def calculate_path_length(policy, start, end, maze_shape):
    current = start
    path_length = 0
    while current != end:
        next_move = policy.get(current)  
        if next_move is None:
            print("No policy for state:", current)
            break  

       
        if next_move == 'up':
            next_state = (current[0]-1, current[1])
        elif next_move == 'down':
            next_state = (current[0]+1, current[1])
        elif next_move == 'left':
            next_state = (current[0], current[1]-1)
        elif next_move == 'right':
            next_state = (current[0], current[1]+1)

        if 0 <= next_state[0] < maze_shape[0] and 0 <= next_state[1] < maze_shape[1]:
            current = next_state
            path_length += 1
        else:
            print("Attempted to move out of bounds:", next_state)
            break  

    return path_length


def state_mapping(maze):
    S = []
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 0:
                S.append((i, j))
    return S
def transition_probabilities(S,A):
    P = {}
    for s in S:
        P[s] = {}
        for a in A:
            P[s][a] = {}
            if a == "up":
                next_s = (s[0] - 1, s[1])
            elif a == "down":
                next_s = (s[0] + 1, s[1])
            elif a == "left":
                next_s = (s[0], s[1] - 1)
            else:
                next_s = (s[0], s[1] + 1)
            if next_s in S:
                P[s][a][next_s] = 1
            else:
                P[s][a][s] = 1
    return P

def rewards(S):
    R={}
    for s in S:
        R[s] = -1 if maze_array[s[0]][s[1]] == 0 else -0.1
    R[(maze_array.shape[0]-2, maze_array.shape[1]-1)] = 10
    return R

def value_iteration(gamma,S,V,A,P,R):
    search_length = 0 

    while True:
        delta=0
        for s in S:
            search_length += 1 
            v = V[s]
            max_value = float("-inf")
            max_action = ''
            for a in A:
                next_states = list(P[s][a].keys())
                if len(next_states) == 0:
                    continue
                expected_value = sum([P[s][a][next_s] * (R[next_s] + gamma * V[next_s]) for next_s in next_states])
                if expected_value > max_value:
                    max_action = a
                max_value = max(max_value, expected_value)
            V[s] = max_value
            delta = max(delta, abs(v - V[s]))
            policy[s] = max_action
        if delta < 1e-300:
            break
    return search_length

def export_solution_to_csv(policy, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for state, action in policy.items():
            writer.writerow([state[0], state[1], action])
    print(f"Solution exported to {filename}")


def get_policy(policy,S,end,A,P,R,V):
    for s in S:
        if s == end:
            continue
        max_value = float("-inf")
        max_action = ''
        for a in A:
            next_states = list(P[s][a].keys())
            if len(next_states) == 0:
                continue
            expected_value = sum([P[s][a][next_s] * (R[next_s] + gamma * V[next_s]) for next_s in next_states])
            if expected_value > max_value:
                max_value = expected_value
                max_action = a
        policy[s] = max_action


parser = argparse.ArgumentParser(description='Solve a maze from a CSV file.')
parser.add_argument('--maze_file', type=str, required=True, help='Path to the CSV file containing the maze.')
args = parser.parse_args()
maze_array = load_from_csv(args.maze_file)

start = (0, 1) 
end = (maze_array.shape[0]-2, maze_array.shape[1]-1) 
gamma = 0.9
state_space = state_mapping(maze_array)
action_space = ['up', 'down', 'left', 'right']
value = {s: 0 for s in state_space}
probability = transition_probabilities(state_space, action_space)
policy = {s: action_space[0] for s in state_space}
reward = rewards(state_space)

print(value)
print(policy)

start_time = time.time()
search_length = value_iteration(gamma, state_space, value, action_space, probability, reward)
end_time = time.time()

execution_time=end_time-start_time
path_length = calculate_path_length(policy, start, end, maze_array.shape)

solution_filename = f"solutions/mdp_value/maze_{maze_array.shape[1]}x{maze_array.shape[0]}.csv"
export_solution_to_csv(policy, solution_filename)

print(f"Path Length: {path_length}")
print(f"Search Length: {search_length}")
print(f"Execution Time: {execution_time} seconds")

results = [str(maze_array.shape), path_length, search_length, execution_time]
with open('mdp_vi_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(results)

draw_maze(maze_array, policy, start, end)