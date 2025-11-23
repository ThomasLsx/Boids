# Boids Simulation

A Python implementation of Craig Reynolds' boids algorithm, simulating the flocking behavior of birds. This project uses Pygame for visualization and a Quadtree for efficient spatial partitioning.

![Boids Simulation](https://upload.wikimedia.org/wikipedia/commons/2/29/Boids.gif)

## Features

- **Boid Agents**: Each boid follows three simple rules:
    - **Cohesion**: Steer to move toward the average position of local flockmates.
    - **Separation**: Steer to avoid crowding local flockmates.
    - **Alignment**: Steer towards the average heading of local flockmates.
- **Quadtree Optimization**: A Quadtree data structure is used to efficiently find boids in the local neighborhood of each agent, significantly improving performance.
- **Interactive UI**: A simple user interface built with Pygame allows for real-time interaction with the simulation.

## How to Use

The simulation provides several controls to manipulate the boids and their behavior:

- **Add Boid**: Adds a new boid to the simulation.
- **Remove Boid**: Removes the last added boid.
- **Pause/Play**: Toggles the simulation between paused and running states.
- **Show Quadtree**: Toggles the visualization of the Quadtree structure.
- **Behavior Sliders**: Sliders are available to adjust the weights of the cohesion, separation, and alignment behaviors in real-time.

## Installation

It is recommended to use a virtual environment.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ThomasLsx/Boids.git
    cd Boids
    ```

2.  **Create and activate a virtual environment:**

    -   **Windows (PowerShell):**
        ```powershell
        python -m venv .venv
        .venv\Scripts\Activate.ps1
        ```
    -   **macOS/Linux (bash):**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the simulation, execute the `main.py` script:

```bash
python main.py
```

## Credits

This project was created by:
- Antoine BARTCZAK
- Lilian BRIAUT
- Thomas LESIEUX