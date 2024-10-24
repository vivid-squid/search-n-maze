import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue
import time
import os
import sys

def load_maze_from_csv(filename):
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        maze = [list(map(int, row)) for row in reader]
    return np.array(maze)

def draw_maze(maze, path):
    rows, cols = maze.shape
    img = np.zeros((rows, cols), dtype=np.uint8)
    img[maze == 0] = 255  # Set paths to white
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    if path is not None:  # Ensure path is not None
        for y, x in path:  # Iterate over path if it exists
            plt.scatter(x, y, c='b', marker='o')
            plt.pause(0.0001)
    plt.show()

def BFS(maze, start, end):
    visited = set()
    queue = Queue()
    queue.put((start, []))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    search_length = 0
    while not queue.empty():
        current, path = queue.get()
        if current == end:
            path_length = len(path) + 1
            return path + [current], search_length, path_length #, execution_time
        if current in visited:
            continue
        visited.add(current)
        search_length += 1
        for dx, dy in directions:
            next_step = (current[0] + dx, current[1] + dy)
            if 0 <= next_step[0] < maze.shape[0] and 0 <= next_step[1] < maze.shape[1] and maze[next_step[0], next_step[1]] == 0:
                queue.put((next_step, path + [current]))
    return None, search_length, 0  # Return None if no path is found

def save_maze_to_csv(maze, path, base_directory='solutions/Bfs'):
    height, width = maze.shape

    directory_path = os.path.join(base_directory, f"maze_{width}x{height}")
    os.makedirs(directory_path, exist_ok=True)

    existing_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    next_file_number = len(existing_files) + 1

    filename = f"maze_{width}x{height}_{next_file_number}.csv"
    full_path = os.path.join(directory_path, filename)

    maze_with_path = np.array(maze)
    if path is not None:
        for position in path:
            maze_with_path[position] = 2  # Mark the path with a different value

    with open(full_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in maze_with_path:
            csvwriter.writerow(row)

    print(f"Maze with path saved to '{full_path}'")

parser = argparse.ArgumentParser(description='Solve a maze from a CSV file.')
parser.add_argument('--maze_file', type=str, required=True, help='Path to the CSV file containing the maze.')
args = parser.parse_args()


maze_array = load_maze_from_csv(args.maze_file)

start = (0, 1)
end = (maze_array.shape[0] - 2, maze_array.shape[1] - 1)
start_time = time.time()
path, search_length, path_length = BFS(maze_array, start, end)
end_time = time.time()

exe_time = end_time - start_time

if path:
    print("Maze has a path!")
    print("Path is:", path)
    print("Search Length:", search_length)
    print("Path Length:", path_length)
    print("Execution Time:", exe_time, "seconds")
else:
    print("Maze does not have a path. Displaying maze without a path.")

save_maze_to_csv(maze_array, path)

results = [str(maze_array.shape), path_length, search_length, exe_time]
with open('bfs_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(results)

draw_maze(maze_array, path)