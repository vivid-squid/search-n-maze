import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plot algorithm metrics.choose between: search,mdp,all')
parser.add_argument('--algorithm_type', type=str, choices=['search', 'mdp', 'all'], help='Type of algorithms to plot: search, mdp, or all')
args = parser.parse_args()


bfs_data = pd.read_csv('bfs_results.csv', header=None)
dfs_data = pd.read_csv('dfs_results.csv', header=None)
astar_data = pd.read_csv('a*_results.csv', header=None)
mdp_vi_data = pd.read_csv('mdp_vi_results.csv', header=None)
mdp_pi_data = pd.read_csv('mdp_pi_results.csv', header=None)

bfs_data.columns = ['Maze Size', 'Path Length', 'Search Length', 'Execution Time']
dfs_data.columns = ['Maze Size', 'Path Length', 'Search Length', 'Execution Time']
astar_data.columns = ['Maze Size', 'Path Length', 'Search Length', 'Execution Time']
mdp_vi_data.columns = ['Maze Size', 'Path Length', 'Search Length', 'Execution Time']
mdp_pi_data.columns = ['Maze Size', 'Path Length', 'Search Length', 'Execution Time']

def plot_data(algorithm_type):
    if algorithm_type == 'search':
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Adjusted figsize for better spacing

        axs[0].plot([str(size) for size in bfs_data['Maze Size']], bfs_data['Execution Time'], 'o-', label='BFS Execution Time')
        axs[0].plot([str(size) for size in dfs_data['Maze Size']], dfs_data['Execution Time'], 's-', label='DFS Execution Time', color='orange')
        axs[0].plot([str(size) for size in astar_data['Maze Size']], astar_data['Execution Time'], '^-', label='A* Execution Time', color='green')
        
        axs[0].set_title('Execution Time vs. Maze Size')
        axs[0].set_xlabel('Maze Size')
        axs[0].set_ylabel('Execution Time')
        axs[0].legend()
        axs[0].tick_params(labelsize=8)

        axs[1].plot([str(size) for size in bfs_data['Maze Size']], bfs_data['Search Length'], 'o-', label='BFS Search Length')
        axs[1].plot([str(size) for size in dfs_data['Maze Size']], dfs_data['Search Length'], 's-', label='DFS Search Length', color='orange')
        axs[1].plot([str(size) for size in astar_data['Maze Size']], astar_data['Search Length'], '^-', label='A* Search Length', color='green')

        axs[1].set_title('Search Length vs. Maze Size')
        axs[1].set_xlabel('Maze Size')
        axs[1].set_ylabel('Search Length')
        axs[1].legend()
        axs[1].tick_params(labelsize=8)

        plt.tight_layout()
        plt.show()
        
    elif algorithm_type == 'mdp':
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Adjusted figsize for better spacing

        axs[0].plot([str(size) for size in mdp_vi_data['Maze Size']], mdp_vi_data['Execution Time'], 'o-', label='MDP_VI Execution Time')
        axs[0].plot([str(size) for size in mdp_pi_data['Maze Size']], mdp_pi_data['Execution Time'], 's-', label='MDP_PI Execution Time', color='orange')

        axs[0].set_title('Execution Time vs. Maze Size')
        axs[0].set_xlabel('Maze Size')
        axs[0].set_ylabel('Execution Time')
        axs[0].legend()
        axs[0].tick_params(labelsize=8)

        axs[1].plot([str(size) for size in mdp_vi_data['Maze Size']], mdp_vi_data['Search Length'], 'o-', label='MDP_VI Execution Time')
        axs[1].plot([str(size) for size in mdp_pi_data['Maze Size']], mdp_pi_data['Search Length'], 's-', label='MDP_PI Execution Time', color='orange')


        axs[1].set_title('Search Length vs. Maze Size')
        axs[1].set_xlabel('Maze Size')
        axs[1].set_ylabel('Search Length')
        axs[1].legend()
        axs[1].tick_params(labelsize=8)

        plt.tight_layout()
        plt.show()
    elif algorithm_type == 'all':
        fig, axs = plt.subplots(1, 2, figsize=(25, 5))  # 1 row, 5 columns for all algorithms
        

        axs[0].plot([str(size) for size in bfs_data['Maze Size']], bfs_data['Execution Time'], 'o-', label='BFS Execution Time',color='blue')
        axs[0].plot([str(size) for size in dfs_data['Maze Size']], dfs_data['Execution Time'], 's-', label='DFS Execution Time', color='orange')
        axs[0].plot([str(size) for size in astar_data['Maze Size']], astar_data['Execution Time'], '^-', label='A* Execution Time', color='green')

        axs[0].plot([str(size) for size in mdp_vi_data['Maze Size']], mdp_vi_data['Execution Time'], 'o-', label='MDP_VI Execution Time',color='violet')
        axs[0].plot([str(size) for size in mdp_pi_data['Maze Size']], mdp_pi_data['Execution Time'], 's-', label='MDP_PI Execution Time', color='yellow')

        axs[0].set_title('Execution Time vs. Maze Size')
        axs[0].set_xlabel('Maze Size')
        axs[0].set_ylabel('Execution Time')
        axs[0].legend()
        axs[0].tick_params(labelsize=8)

        axs[1].plot([str(size) for size in bfs_data['Maze Size']], bfs_data['Search Length'], 'o-', label='BFS Search Length')
        axs[1].plot([str(size) for size in dfs_data['Maze Size']], dfs_data['Search Length'], 's-', label='DFS Search Length', color='orange')
        axs[1].plot([str(size) for size in astar_data['Maze Size']], astar_data['Search Length'], '^-', label='A* Search Length', color='green')

        axs[1].plot([str(size) for size in mdp_vi_data['Maze Size']], mdp_vi_data['Search Length'], 'o-', label='MDP_VI Execution Time', color='violet')
        axs[1].plot([str(size) for size in mdp_pi_data['Maze Size']], mdp_pi_data['Search Length'], 's-', label='MDP_PI Execution Time', color='yellow')


        axs[1].set_title('Search Length vs. Maze Size')
        axs[1].set_xlabel('Maze Size')
        axs[1].set_ylabel('Search Length')
        axs[1].legend()
        axs[1].tick_params(labelsize=8)

        plt.tight_layout()
        plt.show()
           
    else:
        print("Invalid algorithm type")
        return

# plot_data('search') # For BFS, DFS, and A*
# # plot_data('mdp')    # For MDP VI and MDP PI
# # plot_data('all')    # For all algorithms together

plot_data(args.algorithm_type)