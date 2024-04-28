# Pathfinding-Visualizer
Python program built as a visualization tool with TKinter for observing the execution of pathfinding algorithms such as BFS (Breadth-First Search), DFS (Depth-First Search), and UCS (Uniform Cost Search), allowing users to choose an algorithm and see it in action. Includes random grid generation and visualization of visited nodes and the final path.

## Usage
When you run the program, the console will prompt you to choose one of the available algorithms by entering its name.

## Implementation Outline
The visualization displays the search strategy of each algorithm on a grid, with the program randomly generating the layout. The red square represents the goal, while the green squares depict the nodes being explored by the program. Additionally, blue squares symbolize water blocks, which have double the traversal cost compared to regular blocks, providing a test scenario for UCS. Dark-black squares represent impassable walls.

Upon reaching the goal node, the program highlights the final path found by the selected search algorithm in yellow. It opens a new window to pause the program, requiring you to close both windows to restart the program.

## Note
In some instances, the randomly generated grid may lack a viable path connecting the starting and ending nodes. In such cases, the console will display the message: "This randomly generated grid doesn't have a solution," and the program will terminate automatically.

## Output
Breadth-First-Search Demo Video

![Breadth-First-Search Demo Video](https://github.com/Krishnanshu-Gupta/Pathfinding-Visualizer/assets/30324213/8b85a3a5-5ebd-4fb1-b4f8-2c47fe7e9ff9)

---

Breadth-First-Search Output

![Breadth-First-Search Output](/BFS.png)

---

Depth-First-Search Output

![Depth-First-Search Output](/DFS.png)

---

Uniform-Cost-Search Output

![Uniform-Cost-Search Output](/UCS.png)

