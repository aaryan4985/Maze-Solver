document.addEventListener("DOMContentLoaded", function () {
  // Socket.io connection
  const socket = io();

  // DOM elements
  const mazeElement = document.getElementById("maze");
  const generateButton = document.getElementById("generate-maze");
  const solveButton = document.getElementById("solve-maze");
  const mazeSizeSelect = document.getElementById("maze-size");
  const algorithmSelect = document.getElementById("algorithm");
  const speedSelect = document.getElementById("speed");
  const statusElement = document.getElementById("status");

  // Store maze data
  let mazeData = null;
  let isSolving = false;

  // Socket.io event listeners
  socket.on("connect", function () {
    console.log("Connected to server");
    statusElement.textContent =
      'Connected to server. Click "Generate Maze" to start!';
  });

  socket.on("disconnect", function () {
    console.log("Disconnected from server");
    statusElement.textContent =
      "Disconnected from server. Please refresh the page.";
  });

  socket.on("maze_generated", function (data) {
    console.log("Maze generated", data);
    mazeData = data.maze;
    renderMaze();
    solveButton.disabled = false;
    statusElement.textContent =
      'Maze generated! Click "Solve Maze" to visualize the solution.';
  });

  socket.on("maze_solving_step", function (data) {
    const { position, type } = data;

    if (type === "start") {
      statusElement.textContent = "Starting maze solution...";
    } else if (
      type === "visiting" ||
      type === "frontier" ||
      type === "solution"
    ) {
      updateCell(position[0], position[1], type);

      // Update status
      if (type === "visiting") {
        statusElement.textContent = `Visiting cell (${position[0]}, ${position[1]})`;
      } else if (type === "frontier") {
        statusElement.textContent = `Adding (${position[0]}, ${position[1]}) to frontier`;
      } else if (type === "solution") {
        statusElement.textContent = `Solution path includes (${position[0]}, ${position[1]})`;
      }
    }
  });

  socket.on("maze_solved", function (data) {
    console.log("Maze solved", data);
    isSolving = false;
    generateButton.disabled = false;
    solveButton.disabled = false;
    statusElement.textContent =
      data.solution.length > 0
        ? `Solution found! Path length: ${data.solution.length} steps.`
        : "No solution found!";
  });

  socket.on("no_solution", function () {
    console.log("No solution found");
    isSolving = false;
    generateButton.disabled = false;
    solveButton.disabled = false;
    statusElement.textContent = "No solution found!";
  });

  socket.on("error", function (data) {
    console.error("Error:", data.message);
    statusElement.textContent = `Error: ${data.message}`;
    isSolving = false;
    generateButton.disabled = false;
    solveButton.disabled = mazeData === null;
  });

  // Button event listeners
  generateButton.addEventListener("click", function () {
    if (isSolving) return;

    const size = parseInt(mazeSizeSelect.value);
    statusElement.textContent = "Generating maze...";

    // Reset maze
    mazeData = null;
    mazeElement.innerHTML = "";
    solveButton.disabled = true;

    // Request new maze
    socket.emit("generate_maze", { rows: size, cols: size });
  });

  solveButton.addEventListener("click", function () {
    if (!mazeData || isSolving) return;

    isSolving = true;
    generateButton.disabled = true;
    solveButton.disabled = true;
    statusElement.textContent = "Solving maze...";

    // Reset solution visualization (keep walls and paths)
    resetMazeForSolving();

    // Request maze solution
    socket.emit("solve_maze", {
      maze: mazeData,
      algorithm: algorithmSelect.value,
      speed: speedSelect.value,
    });
  });

  // Render maze on the grid
  function renderMaze() {
    if (!mazeData) return;

    const rows = mazeData.length;
    const cols = mazeData[0].length;

    // Clear previous maze
    mazeElement.innerHTML = "";

    // Set grid size
    mazeElement.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
    mazeElement.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

    // Create cells
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const cell = document.createElement("div");
        cell.classList.add("cell");

        // Set cell type
        if (i === 0 && j === 0) {
          cell.classList.add("start");
          cell.textContent = "S";
        } else if (i === rows - 1 && j === cols - 1) {
          cell.classList.add("end");
          cell.textContent = "E";
        } else if (mazeData[i][j] === 1) {
          cell.classList.add("wall");
        } else {
          cell.classList.add("path");
        }

        cell.dataset.row = i;
        cell.dataset.col = j;
        mazeElement.appendChild(cell);
      }
    }
  }

  // Update cell appearance during solving
  function updateCell(row, col, type) {
    const cell = mazeElement.querySelector(
      `[data-row="${row}"][data-col="${col}"]`
    );
    if (!cell) return;

    // Remove old types first
    cell.classList.remove("visiting", "frontier", "solution");

    // Don't change start or end cells' base style
    if (
      (row === 0 && col === 0) ||
      (row === mazeData.length - 1 && col === mazeData[0].length - 1)
    ) {
      return;
    }

    cell.classList.add(type);
  }

  // Reset maze for new solving visualization
  function resetMazeForSolving() {
    const cells = mazeElement.querySelectorAll(".cell");
    cells.forEach((cell) => {
      cell.classList.remove("visiting", "frontier", "solution");
    });
  }

  // Generate initial maze on page load
  generateButton.click();
});
