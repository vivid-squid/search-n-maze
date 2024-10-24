import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import csv, os
import argparse

def load_maze_from_csv(filename):
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        maze = [list(map(int, row)) for row in reader]
    return np.array(maze)

def draw_maze(maze, policy, start, end):
    rows, cols = maze.shape
    _, ax = plt.subplots()  
    img = np.zeros((rows, cols), dtype=np.uint8)
    img[maze == 0] = 255  
    ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax.axis('off')

    current = start
    ax.scatter(current[1], current[0], c='blue', s=100)  
    move_count = 0
    while current != end and move_count < rows * cols:
        y, x = current
        if current in policy:
            action = policy[current]
            
            if (action == 'up' and y > 0 and maze[y - 1, x] == 0) or \
               (action == 'down' and y < rows - 1 and maze[y + 1, x] == 0) or \
               (action == 'left' and x > 0 and maze[y, x - 1] == 0) or \
               (action == 'right' and x < cols - 1 and maze[y, x + 1] == 0):
                current = (y + (action == 'down') - (action == 'up'),
                           x + (action == 'right') - (action == 'left'))
                ax.scatter(current[1], current[0], c='blue', s=10)  # Path positions marked with smaller dots
                move_count += 1
            else:
                print(f"Invalid action {action} at position {current}")
                break
        else:
            print(f"No policy action at position {current}")
            break

    plt.show()

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
    R[(maze_array.shape[0] - 2, maze_array.shape[1] - 1)] = 2
    return R

def policy_evaluation(states,V,policy,P,R,gamma):
    search_length = 0
    while True:
        delta = 0
        for s in states:
            search_length += 1  
            v = V[s]
            a = policy[s]
            next_states = list(P[s][a].keys())
            probs = list(P[s][a].values())
            rewards = [R[next_s] for next_s in next_states]
            V[s] = np.sum([probs[i] * (rewards[i] + gamma * V[next_states[i]]) for i in range(len(next_states))])
            delta = max(delta, abs(v-V[s]))
        if delta < 0.001:
            break
    return search_length

def policy_iteration(states, policy, actions, P, R, V, gamma):
    total_search_length = 0
    iteration_count = 0
    while True:
        iteration_count += 1
        search_length = policy_evaluation(states, V, policy, P, R, gamma)
        total_search_length += search_length 
        policy_stable = policy_improve(states, policy, actions, P, R, V)
        if policy_stable:
            break
    return total_search_length

def policy_improve(states, policy, actions, P, R, V):
    policy_stable = True
    for s in states:
        old_action = policy[s]
        max_v = float('-inf')
        for a in actions:
            next_states = list(P[s][a].keys())
            probs = list(P[s][a].values())
            rewards = [R[next_s] for next_s in next_states]
            v = np.sum([probs[i] * (rewards[i] + gamma * V[next_states[i]]) for i in range(len(next_states))])
            if v > max_v:
                max_v = v
                policy[s] = a
        if old_action != policy[s]:
            policy_stable = False
    return policy_stable

def calculate_path_length(policy, start, end):
    current = start
    path_length = 0
    while current != end:
        if current not in policy:
            break  
        current = next_state_based_on_policy(current, policy)
        path_length += 1
    return path_length

def export_solution_to_csv(policy, filename):
   
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for state, action in policy.items():
            writer.writerow([state[0], state[1], action])
    print(f"Solution exported to {filename}")

def next_state_based_on_policy(current, policy):
    if current not in policy:
        return current 
    action = policy[current]
    action_effects = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    next_state = (current[0] + action_effects[action][0], current[1] + action_effects[action][1])
    return next_state

parser = argparse.ArgumentParser(description='Solve a maze from a CSV file.')
parser.add_argument('--maze_file', type=str, required=True, help='Path to the CSV file containing the maze.')
args = parser.parse_args()
maze_array = load_maze_from_csv(args.maze_file)

start = (0, 1)
end = (maze_array.shape[0] - 2, maze_array.shape[1] - 1)
gamma = 0.9

state_space = state_mapping(maze_array)
action_space = ['up', 'down', 'left', 'right']
value = {s: 0 for s in state_space}
probability = transition_probabilities(state_space, action_space)
policy = {s: action_space[0] for s in state_space}
reward = rewards(state_space)

start_time = time.time()
total_search_length = policy_iteration(state_space, policy, action_space, probability, reward, value, gamma)
end_time = time.time()
path_length = calculate_path_length(policy, start, end)
execution_time = end_time - start_time

print(policy)
print(f"Path Length: {path_length}")
print(f"Search Length: {total_search_length}")
print(f"Execution Time: {execution_time} seconds")

solution_filename = f"solutions/mdp_policy/maze_{maze_array.shape[1]}x{maze_array.shape[0]}.csv"
export_solution_to_csv(policy, solution_filename)

print("Start position:", start)

results = [str(maze_array.shape), path_length, total_search_length, execution_time]
with open('mdp_pi_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(results)
        
draw_maze(maze_array, policy, start, end)