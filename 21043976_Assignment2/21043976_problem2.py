import argparse  # Importing the argparse module for command-line argument parsing
import heapq
import math 
from typing import List, Tuple, Callable  # Importing necessary type hints

class Node:
    '''
    Definition of the Node class, representing a node in the search algorithm.
    It has properties such as parent (the parent node), 
    position (the position of the node in the maze), 
    g (cost from the start node to the current node), 
    h (estimated cost from the current node to the goal node), 
    and f (sum of g and h).
    '''
    def __init__(self, parent: 'Node', position: Tuple[int, int]):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Estimated cost from current node to goal node
        self.f = 0  # Sum of g and h
    def __lt__(self, other):
        return self.f < other.f
        
#h1((x,y)) = = 0
def heuristic_1(node: Tuple[int, int], goal: Tuple[int, int]) -> int:
    return 0 

#h2((x,y)) = height-x + width-y
def heuristic_2(node: Tuple[int, int], goal: Tuple[int, int]) -> int:
    return abs(goal[0] - node[0]) + abs(goal[1] - node[1])

#h3((x,y)) = sqrt((height-x)^2+(width-y)^2)
def heuristic_3(node: Tuple[int, int], goal: Tuple[int, int]) -> float:
    return math.sqrt((goal[0] - node[0])**2 + (goal[1] - node[1])**2)

def a_star_algorithm(maze: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int], heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = heuristic_3) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    '''
    The a_star_algorithm function implements the A* algorithm to find the shortest path from the start position to the goal position in the maze. 
    It takes an optional heuristic argument that defaults to heuristic_3. 
    The function returns a tuple containing the path (a list of positions) and the nodes visited in the search (a list of positions)
    '''
    # Define the list of possible movements in the maze (up, down, left, right)
    movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Initialize both open and closed lists
    open_list = []
    closed_list = []

    # Add the start node
    start_node = Node(None, start)
    goal_node = Node(None, goal)
    heapq.heappush(open_list, (start_node.f, start_node))

    # Loop until the goal is found
    while open_list:
        # Get the current node
        _, current_node = heapq.heappop(open_list)

        # Add current node to closed list
        closed_list.append(current_node)

        # Found the goal
        if current_node.position == goal_node.position:
            path = []
            nodes = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], [node.position for node in closed_list]  # Return reversed path and nodes

        # Generate children
        children = []
        for movement in movements:
            # Get the new position
            new_position = (current_node.position[0] + movement[0], current_node.position[1] + movement[1])

            # Check if new position is within the maze boundaries
            if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                continue

            # Check if new position is walkable terrain
            if maze[new_position[0]][new_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, new_position)
            children.append(new_node)

        # Process children
        for child in children:
            # Check if child is already in the closed list
            if child in closed_list:
                continue

            # Calculate the g, h, and f values for the child
            child.g = current_node.g + 1
            child.h = heuristic(child.position, goal_node.position)
            child.f = child.g + child.h

            # Check if child is already in the open list
            in_open_list = False
            for _, open_node in open_list:
                if open_node.position == child.position:
                    in_open_list = True
                    break

            if in_open_list:
                # Check if the new path has a lower cost
                if child.g < open_node.g:
                    open_list.remove((open_node.f, open_node))
                    heapq.heappush(open_list, (child.f, child))
            else:
                heapq.heappush(open_list, (child.f, child))

    return [], []  # No path found


def read_maze(file_path):
    with open(file_path, 'r') as file:
        dimensions = file.readline()  # Read the dimensions line and discard it
        maze = [list(map(int, line.strip().split())) for line in file.readlines()]
    return maze

def write_output(maze, path, nodes):
    path_maze = [row.copy() for row in maze]
    nodes_maze = [row.copy() for row in maze]

    for p in path:
        path_maze[p[0]][p[1]] = 2
    
    for n in nodes:
        nodes_maze[n[0]][n[1]] = 3

    with open("path_file.txt", 'w') as file:
        #file.write(str(student_id) + '\n')
        file.write('21043976\n')
        for row in path_maze:
            file.write(''.join(map(str, row)) + '\n')

    with open("nodes_file.txt", 'w') as file:
        file.write('21043976\n')
        for row in nodes_maze:
            file.write(''.join(map(str, row)) + '\n')

def main():
    parser = argparse.ArgumentParser(description='A* algorithm for maze solving.')
    parser.add_argument('-m', '--maze', type=str, required=True, help='Path to the input maze file.')
    parser.add_argument('-n', '--node', type=str, required=True, help='Path to the output node file.')
    parser.add_argument('-p', '--path', type=str, required=True, help='Path to the output path file.')
    parser.add_argument('-H', '--heuristic', type=str, default='3', choices=['h1', 'h2', 'h3'], help='Heuristic function to use (h1, h2, or h3). Default is h3.')
    #parser.add_argument('-s', '--student_id', type=str, required=True, help='Student ID.')
    args = parser.parse_args()

    # Choose the heuristic function based on the argument
    if args.heuristic == 'h1':
        heuristic = heuristic_1
    elif args.heuristic == 'h2':
        heuristic = heuristic_2
    else:  # Default is 'c'
        heuristic = heuristic_3

    # Read the maze from the input file
    maze = read_maze(args.maze)

    # Solve the maze using the A* algorithm
    start_pos = (0, 0)
    goal_pos = (len(maze) - 1, len(maze[0]) - 1)
    path, visited_nodes = a_star_algorithm(maze, start_pos, goal_pos)

    #print(path)
    #print(visited_nodes)

    # Write the path and visited nodes to the output files
    write_output(maze, path, visited_nodes)

if __name__ == '__main__':
    main()
