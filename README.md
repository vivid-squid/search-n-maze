
# Search-n-maze README

This README provides instructions on how to generate mazes, apply various search algorithms, and use Markov Decision Processes (MDP) to solve them. It also includes guidance on visualizing the results.

## 1. Generate Maze

To generate a new maze, use the following command:

python Generate_maze_file.py

## 2. Search Algorithms

To solve the generated maze, you can use one of the following search algorithms. Replace `maze_1x1_1.csv` with the name of your maze file if different.

### a. Breadth-First Search (BFS)

python Bfs_file.py --maze_file ./generated_mazes/maze_1x1/maze_1x1_1.csv

### b. Depth-First Search (DFS)

python Dfs_file.py --maze_file ./generated_mazes/maze_1x1/maze_1x1_1.csv

### c. A-Star (A*)

python A-star_file.py --maze_file ./generated_mazes/maze_1x1/maze_1x1_1.csv


## 3. Markov Decision Processes (MDP)

To solve the maze using MDP strategies, use one of the following commands:

### a. MDP Policy Iteration

python MDP_policy.py --maze_file ./generated_mazes/maze_1x1/maze_1x1_1.csv

### b. MDP Value Iteration

python MDP_value.py --maze_file ./generated_mazes/maze_1x1/maze_1x1_1.csv


## 4. Visualize the Result

To visualize the result of the maze solving process, use the following command. Replace `[search,mdp,all]` with your choice of `search` for search algorithms, `mdp` for MDP strategies, or `all` to visualize both types.

python visualize_result.py --algorithm_type [search,mdp,all]

### Note:

- Ensure that Python and all required libraries are installed on your system.
- Replace `./generated_mazes/maze_1x1/maze_1x1_1.csv` with the actual path to your maze file if different.
- The visualization step requires specifying the algorithm type to properly generate and display the results.

