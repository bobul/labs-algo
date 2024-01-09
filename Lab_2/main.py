import numpy as np
import heapq
import pandas as pd
import time
import psutil
import matplotlib.pyplot as plt
import seaborn as sns


def generate_random_maze(size):
    return np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])


def is_valid_move(maze, x, y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0


def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def astar_search(maze, start, goal):
    def is_dead_end(node):
        valid_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        count_valid_moves = sum(
            1 for action in valid_moves if is_valid_move(maze, node[0] + action[0], node[1] + action[1]))
        return count_valid_moves == 1

    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    dead_ends_count = 0
    generated_states_count = 0

    while open_set:
        current_g, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), dead_ends_count, generated_states_count

        closed_set.add(current)

        for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = current[0] + action[0], current[1] + action[1]
            neighbor = (new_x, new_y)

            if not is_valid_move(maze, new_x, new_y) or neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                priority = tentative_g_score + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
                generated_states_count += 1

        if is_dead_end(current):
            dead_ends_count += 1

    return None, dead_ends_count, generated_states_count


def depth_limited_search(maze, start, goal, depth_limit):
    def is_dead_end(node):
        valid_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        count_valid_moves = sum(
            1 for action in valid_moves if is_valid_move(maze, node[0] + action[0], node[1] + action[1]))
        return count_valid_moves == 1

    def recursive_dls(node, depth):
        nonlocal dead_ends_count, generated_states_count

        if depth == 0:
            return None
        if node == goal:
            return [node]

        closed_set.add(node)

        for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = node[0] + action[0], node[1] + action[1]
            neighbor = (new_x, new_y)

            if not is_valid_move(maze, new_x, new_y) or neighbor in closed_set:
                continue

            path = recursive_dls(neighbor, depth - 1)

            if path is not None:
                return [(node[0], node[1])] + path
            generated_states_count += 1

        if is_dead_end(node):
            dead_ends_count += 1

        return None

    closed_set = set()
    dead_ends_count = 0
    generated_states_count = 0

    solution = recursive_dls(start, depth_limit)

    return solution, dead_ends_count, generated_states_count


columns = ["Experiment", "Algorithm", "Steps", "Dead Ends", "Generated States", "Memory Usage (MB)"]
experiment_results = pd.DataFrame(columns=columns)

num_experiments = 20
maze_size = 20
depth_limit = 30

for i in range(1, num_experiments + 1):
    maze = generate_random_maze(maze_size)
    start = (np.random.randint(0, maze_size), np.random.randint(0, maze_size))
    goal = start
    while goal == start:
        goal = (np.random.randint(0, maze_size), np.random.randint(0, maze_size))

    start_time = time.time()
    astar_solution, dead_ends, generated_states = astar_search(maze, start, goal)
    end_time = time.time()
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # in MB

    steps = len(astar_solution) - 1 if astar_solution else None

    experiment_results = experiment_results._append({
        "Experiment": i,
        "Algorithm": "A*",
        "Steps": steps,
        "Dead Ends": dead_ends,
        "Generated States": generated_states,
        "Memory Usage (MB)": memory_usage
    }, ignore_index=True)

for i in range(1, num_experiments + 1):
    maze = generate_random_maze(maze_size)
    start = (np.random.randint(0, maze_size), np.random.randint(0, maze_size))
    goal = start
    while goal == start:
        goal = (np.random.randint(0, maze_size), np.random.randint(0, maze_size))

    start_time = time.time()
    depth_limited_solution, dead_ends, generated_states = depth_limited_search(maze, start, goal, depth_limit)
    end_time = time.time()
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # in MB

    steps = len(depth_limited_solution) - 1 if depth_limited_solution else None

    experiment_results = experiment_results._append({
        "Experiment": i,
        "Algorithm": "Depth-Limited Search",
        "Steps": steps,
        "Dead Ends": dead_ends,
        "Generated States": generated_states,
        "Memory Usage (MB)": memory_usage
    }, ignore_index=True)

experiment_results.to_csv("experiment_results.csv", index=False)

print(experiment_results)

average_metrics = experiment_results.groupby("Algorithm").mean()
print("\nAverage Metrics:")
print(average_metrics)

plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

plt.subplot(2, 2, 1)
sns.barplot(x=average_metrics.index, y='Steps', data=average_metrics)
plt.title('Average Steps by Algorithm')
plt.ylabel('Average Steps')

plt.subplot(2, 2, 2)
sns.barplot(x=average_metrics.index, y='Dead Ends', data=average_metrics)
plt.title('Average Dead Ends by Algorithm')
plt.ylabel('Average Dead Ends')

plt.subplot(2, 2, 3)
sns.barplot(x=average_metrics.index, y='Generated States', data=average_metrics)
plt.title('Average Generated States by Algorithm')
plt.ylabel('Average Generated States')

plt.subplot(2, 2, 4)
sns.barplot(x=average_metrics.index, y='Memory Usage (MB)', data=average_metrics)
plt.title('Average Memory Usage by Algorithm')
plt.ylabel('Average Memory Usage (MB)')

plt.tight_layout()
plt.savefig("average_metrics_plot.png")

plt.show()
