# AI Maze Solver

This project is a maze generator and solver application using Flask and SocketIO. The server generates a random maze and solves it using three different algorithms: **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, and **A\* (A-star)**. The solution is visualized in real-time using WebSockets.

## Features
- **Maze Generation**: Generates a random maze with a configurable size (default is 15x15).
- **Maze Solving**: Solve the generated maze using one of three algorithms:
  - **BFS**: Breadth-First Search
  - **DFS**: Depth-First Search
  - **A\***: A-star (with Manhattan distance heuristic)
- **Real-Time Visualization**: Uses SocketIO to send real-time updates about the solving process.
- **Configurable Speed**: You can adjust the speed of the algorithm's execution for better visualization.

## Prerequisites

Before you can run the project, you need to have Python 3.7+ and `pip` installed on your system. You will also need to install the required dependencies.

### Install Python
Ensure you have Python 3.7 # AI Maze Solver

A web-based application that generates and solves mazes using various AI search algorithms. This project visualizes pathfinding algorithms including Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search.

## Features

- Generate random mazes of various sizes (10x10, 15x15, 20x20, 25x25, 30x30)
- Solve mazes using different algorithms:
  - Breadth-First Search (BFS) - Guarantees shortest path
  - Depth-First Search (DFS) - Uses less memory but may not find shortest path
  - A* Search Algorithm - Uses heuristics to efficiently find shortest path
  - Dijkstra's Algorithm - Optimal for weighted paths
- Real-time visualization of the solving process
- Adjustable animation speed
- Responsive design with dark/light mode
- Interactive UI with intuitive controls
- Statistics display showing cells visited, path length, and solving time

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, Flask-SocketIO
- **Visualization**: Custom CSS animations
- **Communication**: WebSockets for real-time updates

## Project Structure

```
ai-maze-solver/
├── app.py                  # Main Flask application
├── maze_generator.py       # Maze generation algorithms
├── maze_solvers.py         # Maze solving algorithms
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Styling for the application
│   └── js/
│       └── script.js       # Client-side JavaScript
├── templates/
│   └── index.html          # Main HTML template
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   https://github.com/opkpEh/Maze-Solver.git
   cd Maze-Solver
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Algorithm Details

### Breadth-First Search (BFS)
- Explores all neighbor nodes at the present depth before moving to nodes at the next depth
- Guarantees the shortest path in unweighted graphs
- Uses more memory than DFS

### Depth-First Search (DFS)
- Explores as far as possible along each branch before backtracking
- Uses less memory than BFS
- Does not guarantee the shortest path
- Well-suited for maze exploration

### A* Search Algorithm
- Combines the advantages of BFS and greedy best-first search
- Uses heuristics to guide the search
- Optimal and complete when using admissible heuristics
- Finds the shortest path while expanding fewer nodes


## Implementation Notes

### WebSocket Communication

The application uses WebSockets (via Flask-SocketIO) for real-time communication between the server and client:

- `generate_maze` event sends maze generation parameters to the server
- `maze_generated` event returns the generated maze to the client
- `solve_maze` event sends solving parameters to the server
- `maze_solving_step` event updates the client about each step in the solving process
- `maze_solved` event sends the final solution path to the client

### Maze Generation

The maze is generated using a randomized Depth-First Search algorithm with backtracking, which ensures that all generated mazes have exactly one solution.

### Customization

You can customize the application by:
- Modifying the CSS in `static/css/style.css` to change the appearance
- Adding new solving algorithms in `maze_solvers.py`
- Implementing different maze generation algorithms in `maze_generator.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by various pathfinding algorithm visualizers
- Flask-SocketIO for real-time WebSocket communication
- CSS animations for visualizing the algorithms in actionor later installed. You can check your version by running:

```bash
python --version
