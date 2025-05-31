"""
8-Puzzle Solver Game - Improved Version
A classic logic-based puzzle game with AI solving capabilities
"""

import pygame
import sys
import random
import heapq
import time
from copy import deepcopy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
BOARD_SIZE = 450
GRID_SIZE = 3
TILE_SIZE = BOARD_SIZE // GRID_SIZE
MARGIN = 25
FPS = 60

# Colors
BACKGROUND = (224, 247, 250)  # Light blue
TILE_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (1, 87, 155)     # Dark blue
BORDER_COLOR = (0, 0, 0)      # Black
BUTTON_COLOR = (0, 150, 136)  # Teal
BUTTON_TEXT_COLOR = (255, 255, 255)  # White
HINT_COLOR = (255, 245, 157)  # Light yellow
HIGHLIGHT_COLOR = (255, 193, 7)  # Amber for highlighting

# Goal state (1-8 in order, 0 represents empty space)
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Arial', 36)
button_font = pygame.font.SysFont('Arial', 24)
info_font = pygame.font.SysFont('Arial', 20)
help_font = pygame.font.SysFont('Arial', 16)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.is_clicked = False
        self.click_time = 0
        
    def draw(self, surface):
        # Visual feedback for button state
        if self.is_clicked and time.time() - self.click_time < 0.2:
            color = (0, 110, 96)  # Darker when clicked
        elif self.is_hovered:
            color = (0, 130, 116)  # Slightly darker when hovered
        else:
            color = BUTTON_COLOR
            
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 2, border_radius=5)
        
        text_surf = button_font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.click_time = time.time()
                if self.action:
                    return self.action()
        return False

class PuzzleGame:
    def __init__(self):
        self.board = deepcopy(GOAL)
        self.empty_pos = (2, 2)  # Position of the empty tile (row, col)
        self.moves = 0
        self.start_time = time.time()
        self.game_solved = False
        self.hint_pos = None
        self.solving = False
        self.solution_path = []
        self.solution_index = 0
        self.last_move_time = 0
        self.show_help = False
        self.shuffle()
        
        # Create buttons
        button_width = 120
        button_height = 40
        button_y = HEIGHT - 80
        spacing = (WIDTH - (button_width * 3)) // 4
        
        self.new_game_button = Button(
            spacing, button_y, button_width, button_height, 
            "New Game", self.shuffle
        )
        
        self.hint_button = Button(
            spacing * 2 + button_width, button_y, button_width, button_height, 
            "Hint", self.get_hint
        )
        
        self.solve_button = Button(
            spacing * 3 + button_width * 2, button_y, button_width, button_height, 
            "Solve", self.solve_puzzle
        )
        
        # Help button
        self.help_button = Button(
            WIDTH - 50, 10, 40, 40, 
            "?", self.toggle_help
        )
        
        self.buttons = [self.new_game_button, self.hint_button, self.solve_button, self.help_button]
    
    def toggle_help(self):
        """Toggle the help display"""
        self.show_help = not self.show_help
        return True
    
    def shuffle(self):
        """Shuffle the board to create a new puzzle"""
        # Reset game state
        self.board = deepcopy(GOAL)
        self.empty_pos = (2, 2)
        self.moves = 0
        self.start_time = time.time()
        self.game_solved = False
        self.hint_pos = None
        self.solving = False
        self.solution_path = []
        
        # Perform random moves to shuffle
        moves = 100  # Number of random moves
        for _ in range(moves):
            valid_moves = self.get_valid_moves()
            if valid_moves:
                move = random.choice(valid_moves)
                self.move_tile(move[0], move[1], count_move=False)
        
        # Ensure the puzzle is solvable
        if not self.is_solvable():
            # If not solvable, swap any two tiles to make it solvable
            # (except the empty tile)
            pos1 = (0, 0)
            pos2 = (0, 1)
            self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = \
                self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]
        
        # Check if the puzzle is already solved after shuffling (rare but possible)
        if self.board == GOAL:
            # If so, make a single move to unsolved state
            if self.empty_pos != (2, 1):  # Move up if possible
                self.move_tile(2, 1, count_move=False)
            else:  # Otherwise move left
                self.move_tile(1, 2, count_move=False)
        
        return True
    
    def is_solvable(self):
        """Check if the current board configuration is solvable"""
        flat_board = [tile for row in self.board for tile in row]
        inversions = 0
        for i in range(len(flat_board)):
            if flat_board[i] == 0:
                continue
            for j in range(i + 1, len(flat_board)):
                if flat_board[j] == 0:
                    continue
                if flat_board[i] > flat_board[j]:
                    inversions += 1
        # For 3x3 puzzle, solvable if inversions is even
        return inversions % 2 == 0
    
    def get_valid_moves(self):
        """Get all valid moves from current position"""
        valid_moves = []
        row, col = self.empty_pos
        
        # Check all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if the new position is within the grid
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                valid_moves.append((new_row, new_col))
        
        return valid_moves
    
    def move_tile(self, row, col, count_move=True):
        """Move a tile to the empty position if it's adjacent"""
        # Check if the selected tile is adjacent to the empty space
        empty_row, empty_col = self.empty_pos
        
        if (abs(row - empty_row) == 1 and col == empty_col) or \
           (abs(col - empty_col) == 1 and row == empty_row):
            # Swap the tile with the empty space
            self.board[empty_row][empty_col] = self.board[row][col]
            self.board[row][col] = 0
            self.empty_pos = (row, col)
            
            if count_move:
                self.moves += 1
                self.hint_pos = None  # Clear hint after a move
            
            # Check if the puzzle is solved
            if self.board == GOAL:
                self.game_solved = True
            
            return True
        return False
    
    def get_hint(self):
        """Provide a hint using Greedy Best-First Search"""
        if self.game_solved or self.solving:
            return False
        
        # Use Greedy Best-First Search to find the best move
        best_move = self.greedy_best_first_search()
        if best_move:
            self.hint_pos = best_move
            print(f"Hint: Move tile at position {best_move}")
        return True
    
    def greedy_best_first_search(self):
        """Use Greedy Best-First Search to find the best next move"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
        
        best_move = None
        best_score = float('inf')
        
        for move in valid_moves:
            # Create a new board with this move
            new_board = deepcopy(self.board)
            empty_row, empty_col = self.empty_pos
            row, col = move
            
            # Swap the tile with the empty space
            new_board[empty_row][empty_col] = new_board[row][col]
            new_board[row][col] = 0
            
            # Calculate Manhattan distance for this new state
            score = self.manhattan_distance(new_board)
            
            if score < best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def manhattan_distance(self, board):
        """Calculate Manhattan distance heuristic for a board state"""
        distance = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = board[i][j]
                if tile != 0:  # Skip the empty tile
                    # Calculate the expected position of this tile in the goal state
                    goal_row, goal_col = (tile - 1) // GRID_SIZE, (tile - 1) % GRID_SIZE
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance
    
    def solve_puzzle(self):
        """Solve the puzzle using A* algorithm"""
        if self.game_solved or self.solving:
            return False
        
        print("Starting A* solver...")
        self.solution_path = self.a_star_solver()
        if self.solution_path:
            print(f"Solution found with {len(self.solution_path)} moves")
            self.solving = True
            self.solution_index = 0
            self.last_move_time = time.time()
            return True
        else:
            print("No solution found")
            return False
    
    def a_star_solver(self):
        """A* algorithm to find the optimal solution path"""
        # Initial state
        initial_state = (self.manhattan_distance(self.board), 0, self.board, self.empty_pos, [])
        visited = set()
        queue = [initial_state]
        heapq.heapify(queue)
        
        max_iterations = 10000  # Limit iterations to prevent infinite loops
        iterations = 0
        
        while queue and iterations < max_iterations:
            iterations += 1
            _, moves, current, empty_pos, path = heapq.heappop(queue)
            
            # Convert the current board to a tuple for hashing
            board_tuple = tuple(tuple(row) for row in current)
            
            # Skip if we've seen this state before
            if board_tuple in visited:
                continue
            
            visited.add(board_tuple)
            
            # Check if we've reached the goal
            if current == GOAL:
                print(f"Solution found in {iterations} iterations")
                return path
            
            # Get valid moves from current state
            row, col = empty_pos
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check if the new position is within the grid
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                    # Create a new board with this move
                    new_board = deepcopy(current)
                    
                    # Swap the tile with the empty space
                    new_board[row][col] = new_board[new_row][new_col]
                    new_board[new_row][new_col] = 0
                    new_empty_pos = (new_row, new_col)
                    
                    # Add the move to the path
                    new_path = path + [(new_row, new_col)]
                    
                    # Calculate Manhattan distance for this new state
                    h_score = self.manhattan_distance(new_board)
                    g_score = moves + 1
                    f_score = g_score + h_score
                    
                    heapq.heappush(queue, (f_score, g_score, new_board, new_empty_pos, new_path))
        
        print(f"No solution found after {iterations} iterations")
        return []  # No solution found
    
    def update(self):
        """Update game state"""
        if self.solving and self.solution_path and time.time() - self.last_move_time > 0.5:
            if self.solution_index < len(self.solution_path):
                move = self.solution_path[self.solution_index]
                self.move_tile(move[0], move[1])
                self.solution_index += 1
                self.last_move_time = time.time()
            else:
                self.solving = False
    
    def draw(self, surface):
        """Draw the game board and UI elements"""
        # Draw background
        surface.fill(BACKGROUND)
        
        # Draw title
        title_text = font.render("8-Puzzle Solver", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, MARGIN))
        surface.blit(title_text, title_rect)
        
        # Draw game board
        board_rect = pygame.Rect(
            (WIDTH - BOARD_SIZE) // 2,
            (HEIGHT - BOARD_SIZE) // 2 - 30,
            BOARD_SIZE,
            BOARD_SIZE
        )
        pygame.draw.rect(surface, BORDER_COLOR, board_rect, 2)
        
        # Draw tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile_value = self.board[i][j]
                
                if tile_value != 0:  # Skip drawing the empty tile
                    tile_x = (WIDTH - BOARD_SIZE) // 2 + j * TILE_SIZE
                    tile_y = (HEIGHT - BOARD_SIZE) // 2 - 30 + i * TILE_SIZE
                    
                    # Check if this tile is being hinted
                    is_hint = self.hint_pos and (i, j) == self.hint_pos
                    
                    # Check if this tile can be moved (adjacent to empty space)
                    can_move = False
                    empty_row, empty_col = self.empty_pos
                    if ((abs(i - empty_row) == 1 and j == empty_col) or 
                        (abs(j - empty_col) == 1 and i == empty_row)):
                        can_move = True
                    
                    # Draw tile background
                    tile_rect = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
                    
                    if is_hint:
                        pygame.draw.rect(surface, HINT_COLOR, tile_rect)
                    elif can_move:
                        # Slightly highlight movable tiles
                        pygame.draw.rect(surface, (240, 240, 240), tile_rect)
                    else:
                        pygame.draw.rect(surface, TILE_COLOR, tile_rect)
                    
                    pygame.draw.rect(surface, BORDER_COLOR, tile_rect, 2)
                    
                    # Draw tile number
                    text = font.render(str(tile_value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(tile_x + TILE_SIZE // 2, tile_y + TILE_SIZE // 2))
                    surface.blit(text, text_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Draw move counter
        moves_text = info_font.render(f"Moves: {self.moves}", True, TEXT_COLOR)
        surface.blit(moves_text, (20, HEIGHT - 30))
        
        # Draw timer
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        time_text = info_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, TEXT_COLOR)
        surface.blit(time_text, (WIDTH - 150, HEIGHT - 30))
        
        # Draw solved message only if the puzzle is actually solved
        if self.game_solved:
            solved_text = font.render("Puzzle Solved!", True, (0, 150, 0))
            solved_rect = solved_text.get_rect(center=(WIDTH // 2, HEIGHT - 120))
            surface.blit(solved_text, solved_rect)
        
        # Draw help information if enabled
        if self.show_help:
            self.draw_help(surface)
    
    def draw_help(self, surface):
        """Draw help information overlay"""
        # Semi-transparent background
        help_surface = pygame.Surface((WIDTH, HEIGHT))
        help_surface.set_alpha(230)
        help_surface.fill((245, 245, 245))
        surface.blit(help_surface, (0, 0))
        
        # Help title
        help_title = font.render("How to Play", True, TEXT_COLOR)
        title_rect = help_title.get_rect(center=(WIDTH // 2, 50))
        surface.blit(help_title, title_rect)
        
        # Help text
        help_texts = [
            "• Click on tiles adjacent to the empty space to move them",
            "• Use 'New Game' to shuffle and start a new puzzle",
            "• Use 'Hint' to get AI-suggested next move (highlighted in yellow)",
            "• Use 'Solve' to let the AI solve the puzzle automatically",
            "• The goal is to arrange tiles in order (1-8) with empty space at bottom right",
            "",
            "AI Features:",
            "• Hint uses Greedy Best-First Search algorithm",
            "• Solve uses A* algorithm with Manhattan Distance heuristic",
            "• All puzzles are guaranteed to be solvable"
        ]
        
        y_pos = 100
        for text in help_texts:
            text_surf = help_font.render(text, True, TEXT_COLOR)
            surface.blit(text_surf, (50, y_pos))
            y_pos += 30
        
        # Close button
        close_text = button_font.render("Click anywhere to close", True, TEXT_COLOR)
        close_rect = close_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        surface.blit(close_text, close_rect)

def main():
    game = PuzzleGame()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle help screen click to close
            if event.type == pygame.MOUSEBUTTONDOWN and game.show_help:
                game.show_help = False
                continue
            
            # Handle button clicks
            for button in game.buttons:
                button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button.handle_event(event)
            
            # Handle tile clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game.solving and not game.show_help:
                # Convert mouse position to grid position
                board_x = (WIDTH - BOARD_SIZE) // 2
                board_y = (HEIGHT - BOARD_SIZE) // 2 - 30
                
                if board_x <= mouse_pos[0] <= board_x + BOARD_SIZE and \
                   board_y <= mouse_pos[1] <= board_y + BOARD_SIZE:
                    grid_x = (mouse_pos[0] - board_x) // TILE_SIZE
                    grid_y = (mouse_pos[1] - board_y) // TILE_SIZE
                    
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        game.move_tile(grid_y, grid_x)
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
