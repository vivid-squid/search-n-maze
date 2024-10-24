import sys
import random
import csv, os
import numpy as np
sys.setrecursionlimit(50000)
# The maze.
maze = dict()


def display_maze(width,height):
   for y in range(0, height):
      for x in range(0, width):
         if maze[x][y] == 0:
            sys.stdout.write("  ")
         else:
            sys.stdout.write("[]")
      sys.stdout.write("\n")

# Initialize the maze.
def init_maze(width,height):
   for x in range(0, width):
      maze[x] = dict() 
      for y in range(0, height):
         maze[x][y] = 1

# Carve the maze starting at x, y.
def carve_maze(x, y,width,height):
   dir = random.randint(0, 3)
   count = 0
   while count < 4:
      dx = 0
      dy = 0
      if dir == 0:
         dx = 1
      elif dir == 1:
         dy = 1
      elif dir == 2:
         dx = -1
      else:
         dy = -1
      x1 = x + dx
      y1 = y + dy
      x2 = x1 + dx
      y2 = y1 + dy
      if x2 > 0 and x2 < width and y2 > 0 and y2 < height:
         if maze[x1][y1] == 1 and maze[x2][y2] == 1:
            maze[x1][y1] = 0
            maze[x2][y2] = 0
            carve_maze(x2, y2,width,height)
      count = count + 1
      dir = (dir + 1) % 4

# Generate the maze.
def generate_maze(width,height):
   random.seed()
   maze[1][1] = 0 
   carve_maze(1, 1,width,height)
   maze[1][0] = 0 
   maze[width - 1][height - 2] = 0 
   
def save_maze_to_csv(maze, width, height, base_directory='generated_mazes'):
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Define the directory name based on the dimensions of the maze
    directory_name = f"maze_{width}x{height}"
    directory_path = os.path.join(base_directory, directory_name)
    
    # Create the directory for this size of maze if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Find the next available file number
    existing_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    file_number = 1
    if existing_files:
        existing_files.sort()
        last_file = existing_files[-1]
        # Extract the number from the file name
        file_number = int(last_file.split('_')[-1].replace('.csv', '')) + 1

    # Define the full path for the new maze file
    filename = f"maze_{width}x{height}_{file_number}.csv"
    full_path = os.path.join(directory_path, filename)

    # Write the maze to a CSV file
    with open(full_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for y in range(height):
            row = [maze[x][y] for x in range(width)]
            csvwriter.writerow(row)

    print(f"Maze saved to '{full_path}'")

# Generate and display a random maze.
def main(width,height):
   init_maze(width,height)
   generate_maze(width,height)

   display_maze(width,height)
   # filename = f"maze_{width}x{height}.csv"
   save_maze_to_csv(maze, width, height)

# The size of the maze (must be odd).
width = int(input("Enter the number of width: ")) 
height = int(input("Enter the number of height: ")) 
main(width,height)