from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging
import time

from maze_generator import generate_maze
from maze_solvers import bfs_solve, dfs_solve, astar_solve

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)