import tkinter as tk
import random
import math
from collections import deque
from queue import PriorityQueue

# Board code partially adapted from this repository: https://github.com/misbah4064/A_Star_Python
# It provided a foundation for helping setting up the TKinter window and graphics.
# The original author didn't use BFS, DFS, or UCS, and used A_star instead.
# Code was significantly changed for the purposes of this program.
class Board:
    # initializations
    rows = 30
    cols = 30
    Width = 600
    Walls = []
    Water = []

    # create start and end points
    start = (random.randint(1, 29), random.randint(1, 29))
    end = (random.randint(1, 29), random.randint(1, 29))
    distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    # ensures that start end points are at least 10 blocks away to increase difficulty
    while distance < 10:
        end = (random.randint(1, 29), random.randint(1, 29))
        distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    # create Walls and Water
    for i in range(cols):
        for j in range(rows):
            # 20% chance of spawning wall
            if random.randint(0,9) < 2 and (i,j) != start and (i,j) != end:
                Walls.append((i,j))
            # 6% chance of spawning water
            elif random.randint(0, 50) < 3 and (i,j) != start and (i,j) != end:
                Water.append((i, j))

# render the paths for all objects on the board
def render_path(canvas, board, path, visited, final = False):
    canvas.delete("all")
    width = board.Width // board.cols
    # display walls in black
    for (i, j) in board.Walls:
        canvas.create_rectangle(i*width, j*width,(i+1)*width, (j+1)*width, fill="black", width = 1)
    # display water in blue (these have double the cost of regular blocks)
    for (i, j) in board.Water:
        canvas.create_rectangle(i*width, j*width,(i+1)*width, (j+1)*width, fill="blue", width = 1)
    # display all visited nodes in green
    for (i, j) in visited:
        canvas.create_rectangle(i*width, j*width,(i+1)*width, (j+1)*width, fill="green", width = 1)
    # display the final path in yellow once the search algorithms conclude
    if final:
        for (i, j) in path:
            canvas.create_rectangle(i*width, j*width,(i+1)*width, (j+1)*width, fill="yellow", width = 1)  # Change color for path

    # display the start and end positions in green and red, respectively
    start = board.start
    end = board.end
    canvas.create_rectangle(start[0]*width, start[1]*width,(start[0]+1)*width, (start[1]+1)*width, fill="green", width = 1)
    canvas.create_rectangle(end[0]*width, end[1]*width,(end[0]+1)*width, (end[1]+1)*width, fill="red", width = 1)

rows = Board.rows
cols = Board.cols
Width = Board.Width
start = Board.start
end = Board.end

# grid class
class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.water = []

    # bounds detection
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    # make sure path doesn't go through walls
    def passable(self, id):
        return id not in self.walls

    # check neighbors
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    # determine the cost, make water double the cost of regular blocks
    # this helps test the UCS algorithm
    def cost(self, from_node, to_node):
        if to_node not in self.water:
            return 1
        else:
            return 2

diagram1 = SquareGrid(cols, rows)
diagram1.walls = Board.Walls
diagram1.water = Board.Water

# Breadth First Search
def bfs_search(graph, start, end):
    queue = deque([start])
    came_from = {}
    came_from[start] = None
    visited = set([start])

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for next_node in graph.neighbors(current):
            if next_node not in visited:
                queue.append(next_node)
                visited.add(next_node)
                came_from[next_node] = current

                # create the canvas visualizations and render on each step
                if "canvas" not in bfs_search.__dict__:
                    bfs_search.canvas = tk.Canvas(tk.Tk(), width=Board.Width, height=Board.Width)
                    bfs_search.canvas.pack()

                render_path(bfs_search.canvas, Board, reconstruct_path(came_from, start, current), visited)  # Pass reconstructed path
                bfs_search.canvas.update()
    return came_from, visited

# Depth First Search
def dfs_search(graph, start, end):
    stack = [start]
    came_from = {}
    came_from[start] = None
    visited = set([start])
    while stack:
        current = stack.pop()
        if current == end:
            break
        for next_node in graph.neighbors(current):
            if next_node not in visited:
                stack.append(next_node)
                visited.add(next_node)
                came_from[next_node] = current

                # create the canvas visualizations and render on each step
                if "canvas" not in dfs_search.__dict__:
                    dfs_search.canvas = tk.Canvas(tk.Tk(), width=Board.Width, height=Board.Width)
                    dfs_search.canvas.pack()
                render_path(dfs_search.canvas, Board, reconstruct_path(came_from, start, current), visited)  # Pass reconstructed path
                dfs_search.canvas.update()
    return came_from, visited

# Uniform Cost Search, which takes into account the different costs based on water or not
# Water has double the cost of a regular block
def uniform_cost_search(graph, start, end):
    pqueue = PriorityQueue()
    pqueue.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not pqueue.empty():
        current = pqueue.get()
        if current == end:
            break
        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                pqueue.put(next_node, priority)
                came_from[next_node] = current

                # create the canvas visualizations and render on each step
                if "canvas" not in uniform_cost_search.__dict__:
                    uniform_cost_search.canvas = tk.Canvas(tk.Tk(), width=Board.Width, height=Board.Width)
                    uniform_cost_search.canvas.pack()

                render_path(uniform_cost_search.canvas, Board, reconstruct_path(came_from, start, current), set(cost_so_far.keys()))  # Pass reconstructed path
                uniform_cost_search.canvas.update()
    return came_from, cost_so_far.keys()

# reconstruct the final, optimal path from the search algorithms
def reconstruct_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            print("This randomly generated grid doesn't have a solution")
            return None
    path.append(start)
    path.reverse()
    return path

# get the user choice for search algorithm
def get_search_algorithm():
    while True:
        choice = input("Choose a search algorithm (BFS, DFS, UCS): ").upper()
        if choice in ["BFS", "DFS", "UCS"]:
            return choice
        else:
            print("Invalid choice. Please choose BFS, DFS, or UCS.")

came_from = None
visited = None
algorithm_choice = get_search_algorithm()
if algorithm_choice == "BFS":
    search_algorithm = bfs_search
elif algorithm_choice == "DFS":
    search_algorithm = dfs_search
elif algorithm_choice == "UCS":
    search_algorithm = uniform_cost_search

print("Start Point:", start)
print("End Point:", end)

# Run the chosen search algorithm and find the final path
came_from, visited = search_algorithm(diagram1, start, end)
total_path = reconstruct_path(came_from, start, end)

if total_path is not None:
    print("Total Path:", total_path)

    # render the final paths in yellow
    if algorithm_choice == "BFS":
        render_path(bfs_search.canvas, Board, total_path, visited, True)
    elif algorithm_choice == "DFS":
        render_path(dfs_search.canvas, Board, total_path, visited, True)
    elif algorithm_choice == "UCS":
        render_path(uniform_cost_search.canvas, Board, total_path, visited, True)

    tk.Tk().mainloop() # open a new tkinter window when end reached to keep program running
