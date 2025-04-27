import random
import logging

logger = logging.getLogger(__name__)

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