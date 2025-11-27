# Snake 3D - PvZ Style

This is a pseudo-3D style Snake game developed with Python and Pygame. It features unique visuals and rich gameplay mechanics, supporting both single-player and two-player versus modes.

## Quickstart

### Prerequisites
- Python 3.8+
- Poetry (Recommended) or pip

### Installation & Run (Using Poetry)

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Run the Game**
   ```bash
   poetry run start
   # Or
   poetry run python main.py
   ```

### Installation & Run (Using pip)

> Note: If `requirements.txt` is not present, you can generate it via `poetry export` or manually install `pygame`.

1. **Install Dependencies**
   ```bash
   pip install pygame
   ```

2. **Run the Game**
   ```bash
   python main.py
   ```

## Technical Architecture

This project utilizes a modular package structure and uses **Poetry** for dependency management and building. It primarily relies on the **Pygame** library for graphics rendering and event handling.

*   **Project Structure**:
    *   `snake_game/`: Core source package
        *   `main.py`: Package entry point
        *   `game.py`: Core controller
        *   `snake.py`: Snake entity logic
        *   `sprites.py`: Other game entities (Food, Bomb, Explosion)
        *   `ui.py`: UI components and font system
        *   `settings.py`: Global configuration
    *   `pyproject.toml`: Project configuration and dependency management

*   **Core Language**: Python 3
*   **Graphics Engine**: Pygame (SDL wrapper)
*   **Rendering Method**: 2D primitive drawing (circles, rectangles), simulating a 3D visual experience through layering, highlights, and shadows.
*   **Font System**: Built-in custom `PixelFont` class that renders pixel-style fonts directly via code. It does not rely on external font files, ensuring consistency across environments (while retaining a fallback mechanism for loading system fonts).
*   **Input Handling**: Keyboard events control snake movement, while mouse events are used for UI interaction.

## Logical Architecture

The game logic adopts Object-Oriented Programming (OOP) principles. The main modules are divided as follows:

### 1. Core Controller (`Game` Class)
The central hub of the system, responsible for:
*   **State Management**: Maintaining the game state machine (`MENU`, `PLAYING`, `PAUSED`, `GAMEOVER`).
*   **Main Loop**: Coordinating the three major lifecycles: `handle_events` (Input), `update` (Logic), and `draw` (Rendering).
*   **Mode Management**: Handling initialization and rule differences for Single Player (`SINGLE`) and Two Player Versus (`VERSUS`) modes.

### 2. Entities
*   **Snake**:
    *   Manages the list of body coordinates, movement direction, and growth logic.
    *   Implements collision detection (self, walls, enemies).
    *   Includes special state logic: `freeze` (frozen when hit) and `shrink` (bomb damage).
*   **Food**:
    *   Responsible for randomly generating coordinates that do not overlap with obstacles.
    *   Manages food rendering.
*   **Bomb**:
    *   Randomly spawns as an obstacle.
    *   Contains countdown or trigger logic with unique visual rendering.
*   **Explosion**:
    *   A simple particle system effect used for visual feedback when bombs are triggered.

### 3. Auxiliary Systems
*   **PixelFont**: Custom character bitmap data implementing basic ASCII character rendering with scaling support.
*   **Button**: Encapsulates rectangular area detection, mouse hover effects, and click callbacks for building the UI menu.

## Game Mechanics

*   **Movement**: The snake head leads the body movement, supporting smooth grid-based movement.
*   **Boundary Handling**: Includes wall bounce mechanics (at specific angles) or game over conditions.
*   **Versus Rules**: In two-player mode, if a snake's head collides with the opponent's body, it gets frozen and bounces back, adding a layer of strategy.
*   **Items**:
    *   **Food**: Increases score and causes the snake to grow.
    *   **Bomb**: Contact reduces the snake's length and triggers an explosion effect.
