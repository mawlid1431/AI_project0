import os
import sys
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Directory setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SCRIPT_DIR, 'static')

# Create static directory if it doesn't exist
os.makedirs(STATIC_DIR, exist_ok=True)

# Create a web-friendly version of the game
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>8-Puzzle Solver Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #E0F7FA;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #01579B;
            margin-bottom: 20px;
        }
        .container {
            max-width: 800px;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .instructions {
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .download-section {
            margin-top: 20px;
            text-align: center;
        }
        .btn {
            display: inline-block;
            background-color: #009688;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px;
            border: none;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #00796B;
        }
        .code-section {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            overflow-x: auto;
        }
        pre {
            margin: 0;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .features {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-top: 20px;
        }
        .feature {
            flex-basis: 48%;
            margin-bottom: 15px;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .feature h3 {
            margin-top: 0;
            color: #01579B;
        }
        @media (max-width: 768px) {
            .feature {
                flex-basis: 100%;
            }
        }
    </style>
</head>
<body>
    <h1>8-Puzzle Solver Game</h1>
    
    <div class="container">
        <h2>Game Overview</h2>
        <p class="instructions">
            This is an implementation of the classic 8-puzzle game with AI-powered solving capabilities. 
            The game features a 3x3 grid with numbered tiles (1-8) and one empty space. 
            The goal is to rearrange the tiles to achieve the target configuration by sliding tiles into the empty space.
        </p>
        
        <div class="features">
            <div class="feature">
                <h3>Game Features</h3>
                <ul>
                    <li>Interactive gameplay with mouse controls</li>
                    <li>New Game button to shuffle and start a new puzzle</li>
                    <li>Move counter and timer to track your progress</li>
                    <li>Visual feedback for hints and solved state</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>AI Features</h3>
                <ul>
                    <li><strong>Hint Button:</strong> Uses Greedy Best-First Search to suggest the next move</li>
                    <li><strong>Solve Button:</strong> Uses A* algorithm with Manhattan Distance heuristic to automatically solve the puzzle</li>
                    <li>All puzzles are guaranteed to be solvable</li>
                </ul>
            </div>
        </div>
        
        <div class="download-section">
            <h3>Download and Play</h3>
            <p>Download the game and run it on your computer:</p>
            <a href="/download/puzzle.py" class="btn">Download Game</a>
            <p>Requirements: Python 3.10+ and Pygame library</p>
            <p>Run with: <code>python puzzle.py</code></p>
        </div>
    </div>
    
    <div class="container">
        <h2>How to Play</h2>
        <ul class="instructions">
            <li>Click on tiles adjacent to the empty space to move them</li>
            <li>Use the "New Game" button to shuffle and start a new puzzle</li>
            <li>Use the "Hint" button when you need help with the next move (highlighted in yellow)</li>
            <li>Use the "Solve" button to watch the AI solve the puzzle automatically</li>
            <li>The goal is to arrange tiles in order (1-8) with empty space at bottom right</li>
        </ul>
    </div>
    
    <div class="container">
        <h2>AI Implementation</h2>
        <p>The game includes two AI algorithms:</p>
        
        <h3>A* Algorithm (Solve Button)</h3>
        <p>
            The A* algorithm finds the optimal solution path using Manhattan Distance as a heuristic.
            It evaluates states based on both the cost to reach the state and the estimated cost to the goal.
        </p>
        
        <h3>Greedy Best-First Search (Hint Button)</h3>
        <p>
            The Greedy Best-First Search algorithm suggests the next best move by evaluating
            which move brings the puzzle closest to the goal state using the Manhattan Distance heuristic.
        </p>
        
        <div class="code-section">
            <h3>Key Code Snippet: A* Solver</h3>
            <pre>
# A* algorithm to find the optimal solution path
# Initial state with Manhattan distance heuristic
# Uses a priority queue to explore states efficiently
# Returns the optimal path of moves to solve the puzzle
            </pre>
        </div>
    </div>
</body>
</html>
"""

with open(os.path.join(STATIC_DIR, 'index.html'), 'w') as f:
    f.write(html_content)

# Routes
@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(SCRIPT_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
