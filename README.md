# 8-Puzzle Solver Game

![8-Puzzle Game Screenshot](screenshot.png)

**Project Note:**  
This project was my first game and my first AI project for the AI class at my university.  
It was a great learning experience in both game development and implementing AI algorithms!

---

A classic 8-puzzle game with AI-powered solving and hint features, built with Python and Pygame.

## Features

- Interactive 8-puzzle game (3x3 grid)
- "New Game" button to shuffle and start a new puzzle
- "Hint" button (Greedy Best-First Search AI)
- "Solve" button (A* algorithm with Manhattan Distance heuristic)
- Move counter and timer
- Visual feedback for hints and solved state
- All puzzles are guaranteed to be solvable

---

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/mawlid1431/AI_project0.git
   cd AI_project0
   ```

2. **Install Python 3.10+**  
   Download from [python.org](https://www.python.org/downloads/).

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or, if you only want to run the game:
   ```bash
   pip install pygame
   ```

---

## How to Run

To start the game, run:
```bash
python puzzle.py
```

The game window will open. You can now play the 8-puzzle game!

---

## How to Play

- **Move tiles:** Click on any tile adjacent to the empty space to move it.
- **New Game:** Click "New Game" to shuffle and start a new puzzle.
- **Hint:** Click "Hint" to highlight the best next move (AI suggestion).
- **Solve:** Click "Solve" to watch the AI solve the puzzle automatically.
- **Goal:** Arrange the tiles in order (1-8) with the empty space at the bottom right.

---

## AI Algorithms

- **Hint:** Uses Greedy Best-First Search to suggest the next best move.
- **Solve:** Uses the A* algorithm with Manhattan Distance heuristic to find the optimal solution path.

---

## License

This project is for educational purposes.

---

## Credits

Developed by Mawlid1431.