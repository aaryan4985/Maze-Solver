from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
from collections import deque
import time
import heapq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_maze(rows=15, cols=15):
    """
    Generate a maze with open paths and walls.
    0 represents an open path, 1 represents a wall.
    """
    logger.info(f"Generating maze of size {rows}x{cols}")
    
    # Initialize with all walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    # Make sure start and end points are open
    maze[0][0] = 0  # Start point
    maze[rows-1][cols-1] = 0  # End point
    
    # Create some random paths
    for i in range(rows):
        for j in range(cols):
            # Higher probability of open cells
            if random.random() > 0.3:  # 70% chance of being open
                maze[i][j] = 0
    
    # Ensure a path exists from start to end (simple approach)
    for i in range(rows):
        maze[i][0] = 0  # Create a path along the left edge
    for j in range(cols):
        maze[rows-1][j] = 0  # Create a path along the bottom edge
        
    return maze

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

@socketio.on('generate_maze')
def handle_generate_maze(data):
    rows = data.get('rows', 15)
    cols = data.get('cols', 15)
    
    logger.info(f"Generating maze: {rows}x{cols}")
    maze = generate_maze(rows, cols)
    emit('maze_generated', {'maze': maze})

@socketio.on('solve_maze')
def handle_solve_maze(data):
    maze = data.get('maze', [])
    algorithm = data.get('algorithm', 'bfs')
    speed = data.get('speed', 'medium')

    if not maze:
        logger.error("No maze provided")
        emit('error', {'message': 'No maze provided'})
        return

    logger.info(f"Solving maze with algorithm: {algorithm} at speed: {speed}")

    # Define sleep times based on speed
    speed_delay = {
        'slow': 0.5,
        'medium': 0.2,
        'fast': 0.05
    }
    delay = speed_delay.get(speed, 0.2)

    # Start solving
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows-1, cols-1)
    
    # Emit start position
    emit('maze_solving_step', {'position': start, 'type': 'start'})
    time.sleep(delay)

    solution = []
    if algorithm == 'bfs':
        solution = bfs_solve(maze, start, end, emit, delay)
    elif algorithm == 'dfs':
        solution = dfs_solve(maze, start, end, emit, delay)
    elif algorithm == 'astar':
        solution = astar_solve(maze, start, end, emit, delay)

    # Emit final solution path
    if solution:
        emit('maze_solved', {'solution': solution})
    else:
        emit('no_solution', {})

def bfs_solve(maze, start, end, emit_func, delay):
    """
    Breadth-First Search algorithm for maze solving.
    Emits steps for visualization.
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start}
    parent = {}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    while queue:
        current = queue.popleft()
        r, c = current
        
        # Emit current visiting cell
        emit_func('maze_solving_step', {'position': current, 'type': 'visiting'})
        time.sleep(delay)
        
        # Check if we've reached the end
        if current == end:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            # Emit solution path animation
            for step in path:
                emit_func('maze_solving_step', {'position': step, 'type': 'solution'})
                time.sleep(delay)
            
            return path
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                
                # Emit frontier cell
                emit_func('maze_solving_step', {'position': neighbor, 'type': 'frontier'})
                time.sleep(delay)
    
    return []  # No path found

def dfs_solve(maze, start, end, emit_func, delay):
    """
    Depth-First Search algorithm for maze solving.
    Emits steps for visualization.
    """
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = {start}
    parent = {}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    while stack:
        current = stack.pop()  # Pop from the end (LIFO)
        r, c = current
        
        # Emit current visiting cell
        emit_func('maze_solving_step', {'position': current, 'type': 'visiting'})
        time.sleep(delay)
        
        # Check if we've reached the end
        if current == end:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            # Emit solution path animation
            for step in path:
                emit_func('maze_solving_step', {'position': step, 'type': 'solution'})
                time.sleep(delay)
            
            return path
        
        # Explore neighbors in reverse order for visual effect
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and neighbor not in visited):
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                
                # Emit frontier cell
                emit_func('maze_solving_step', {'position': neighbor, 'type': 'frontier'})
                time.sleep(delay)
    
    return []  # No path found

def heuristic(a, b):
    """Manhattan distance heuristic for A* algorithm"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_solve(maze, start, end, emit_func, delay):
    """
    A* algorithm for maze solving.
    Emits steps for visualization.
    """
    rows, cols = len(maze), len(maze[0])
    
    # Priority queue for A* (f_score, counter, position)
    # counter is used to break ties consistently
    counter = 0
    open_set = [(heuristic(start, end), counter, start)]
    counter += 1
    
    # For tracking and visualization
    open_positions = {start}
    closed_set = set()
    
    # For path reconstruction
    came_from = {}
    
    # g_score: cost from start to position
    g_score = {start: 0}
    
    # f_score: estimated total cost from start to goal through position
    f_score = {start: heuristic(start, end)}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    while open_set:
        # Get position with lowest f_score
        current_f, _, current = heapq.heappop(open_set)
        open_positions.remove(current)
        
        # Skip if already evaluated
        if current in closed_set:
            continue
        
        # Emit current visiting cell
        emit_func('maze_solving_step', {'position': current, 'type': 'visiting'})
        time.sleep(delay)
        
        # Check if we've reached the end
        if current == end:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            
            # Emit solution path animation
            for step in path:
                emit_func('maze_solving_step', {'position': step, 'type': 'solution'})
                time.sleep(delay)
            
            return path
        
        # Mark as evaluated
        closed_set.add(current)
        
        # Explore neighbors
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            # Skip if out of bounds, wall, or already evaluated
            if (nr < 0 or nr >= rows or nc < 0 or nc >= cols or 
                maze[nr][nc] == 1 or neighbor in closed_set):
                continue
            
            # Calculate tentative g_score
            tentative_g = g_score[current] + 1
            
            # If this path is better
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                # Record this path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                
                # Add to open set if not already there
                if neighbor not in open_positions:
                    counter += 1
                    heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                    open_positions.add(neighbor)
                    
                    # Emit frontier cell
                    emit_func('maze_solving_step', {'position': neighbor, 'type': 'frontier'})
                    time.sleep(delay)
    
    return []  # No path found

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)