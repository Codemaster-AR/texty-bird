# --- INITIAL SETUP MESSAGE ---
import time
print("Initializing Texty Bird...")
print("Please maximize your terminal window for the best experience.")
print("Works on Mac and Linux by default.")
print("On Windows, you may need to install the 'windows-curses' package via pip.")
print("Starting the game in 3 seconds")
time.sleep(3) # Small pause to allow the user to read the message and resize if needed
# --- END INITIAL SETUP MESSAGE ---

import curses
import time
import random
import sys
import os



def clear_screen():
    # Check the operating system and use the appropriate command
    if os.name == 'nt':  # 'nt' is used for Windows
        os.system('cls')
    else:  # 'posix' is used for Linux, macOS, and other Unix-like systems
        os.system('clear')


# --- Configuration & Constants ---
TICK_RATE = 0.05  # Lower value = faster game (20 FPS)
BIRD_X = 10       # Fixed horizontal position of the bird
COUNTDOWN_TIME = 3 # Seconds for the pre-game delay

# --- Physics Constants ---
GRAVITY = 1.0
JUMP_STRENGTH = -3.0

# --- Pipe Constants ---
PIPE_GAP = 7
PIPE_WIDTH = 2
PIPE_SPAWN_INTERVAL = 50 # *** Increased for maximum horizontal space ***
PIPE_SPEED = 1

# --- Global Game State ---
bird_y = 0.0
bird_velocity = 0.0
pipes = []
score = 0
game_tick = 0
game_over = False

def initialize_game(stdscr):
    """Resets all game variables and configures curses."""
    global bird_y, bird_velocity, pipes, score, game_tick, game_over
    
    # Get screen dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    # Reset state
    bird_y = max_y // 2
    bird_velocity = 0.0
    pipes = []
    score = 0
    game_tick = 0
    game_over = False
    
    # Configure curses for non-blocking input and no echo
    stdscr.nodelay(True) # Non-blocking read
    stdscr.timeout(0)   # Set timeout for getch() to 0
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

def draw_pipe(stdscr, p_x, p_center, max_y):
    """Draws a single pipe column."""
    
    gap_top = p_center['center'] - PIPE_GAP // 2
    gap_bottom = p_center['center'] + PIPE_GAP // 2

    for y in range(max_y):
        if y < gap_top or y > gap_bottom:
            try:
                stdscr.addch(y, p_x, '#') 
            except curses.error:
                pass

def draw_game(stdscr, max_y, max_x):
    """Refreshes the screen state."""
    
    stdscr.clear()
    
    # 1. Draw Pipes
    for p_x, p_center in pipes:
        draw_pipe(stdscr, int(p_x), p_center, max_y)
        draw_pipe(stdscr, int(p_x) + 1, p_center, max_y)

    # 2. Draw Bird
    bird_display_y = int(round(bird_y))
    if 0 <= bird_display_y < max_y:
        bird_char = 'V' if bird_velocity > 0.5 else '>'
        try:
            stdscr.addch(bird_display_y, BIRD_X, bird_char, curses.A_BOLD)
        except curses.error:
             pass
    
    # 3. Draw Score and Instructions
    stdscr.addstr(0, 0, f"Score: {score} | Press SPACE or 'f' to JUMP. | Ticks: {game_tick}", curses.A_REVERSE)

    # 4. Refresh Screen
    stdscr.refresh()


def update_game(max_y, max_x):
    """Updates game physics and logic."""
    global bird_y, bird_velocity, pipes, score, game_tick, game_over
    
    # --- 1. Physics Update ---
    bird_velocity += GRAVITY * TICK_RATE * 5
    bird_y += bird_velocity * TICK_RATE * 5
    
    # --- 2. Pipe Logic ---
    game_tick += 1
    
    # Move pipes left and check for scoring
    new_pipes = []
    for p_x, p_center_dict in pipes:
        p_x -= PIPE_SPEED
        
        if int(p_x) + PIPE_WIDTH < BIRD_X and not p_center_dict.get('passed'):
             score += 1
             p_center_dict['passed'] = True
        
        if p_x > -PIPE_WIDTH:
            new_pipes.append([p_x, p_center_dict])
            
    pipes = new_pipes
    
    # Spawn new pipe
    if game_tick % PIPE_SPAWN_INTERVAL == 0:
        min_center = PIPE_GAP // 2 + 1
        max_center = max_y - PIPE_GAP // 2 - 1
        gap_center = random.randint(min_center, max_center)
        pipes.append([max_x - PIPE_WIDTH, {'center': gap_center, 'passed': False}])

    # --- 3. Collision Detection ---
    bird_display_y = int(round(bird_y))

    # Boundary collision
    if bird_display_y < 1 or bird_display_y >= max_y:
        game_over = True
        return

    # Pipe collision
    for p_x, p_center_dict in pipes:
        p_center = p_center_dict['center']
        
        is_colliding_x = BIRD_X >= int(p_x) and BIRD_X < int(p_x) + PIPE_WIDTH
        
        if is_colliding_x:
            gap_top = p_center - PIPE_GAP // 2
            gap_bottom = p_center + PIPE_GAP // 2
            
            if not (bird_display_y > gap_top and bird_display_y < gap_bottom):
                game_over = True
                return

def show_countdown(stdscr, max_y, max_x):
    """Displays a countdown before starting the game."""
    stdscr.clear()
    
    center_y = max_y // 2
    
    title = "Texty Bird - Get Ready!"
    stdscr.addstr(center_y - 2, max_x // 2 - len(title) // 2, title, curses.A_BOLD)
    
    for i in range(COUNTDOWN_TIME, 0, -1):
        stdscr.clear()
        stdscr.addstr(center_y - 2, max_x // 2 - len(title) // 2, title, curses.A_BOLD)
        
        count_msg = f"Starting in... {i}"
        stdscr.addstr(center_y, max_x // 2 - len(count_msg) // 2, count_msg, curses.A_REVERSE)
        
        stdscr.refresh()
        time.sleep(1.0) # Use time.sleep for countdown
        
    stdscr.clear()

def main(stdscr):
    """The main game wrapper function with a replay loop."""
    
    while True:
        global bird_velocity, game_over, score
        
        # 1. Initialize Curses and Game State
        initialize_game(stdscr)
        
        # 2. Run the Countdown
        max_y, max_x = stdscr.getmaxyx()
        show_countdown(stdscr, max_y, max_x)

        # 3. Re-initialize game state to ensure clean start after the timer
        initialize_game(stdscr)
        
        # 4. Main Game Loop
        while not game_over:
            max_y, max_x = stdscr.getmaxyx()
            
            # --- Input Handling (Non-Blocking) ---
            key = stdscr.getch()
            if key == ord(' ') or key == ord('f'):
                bird_velocity = JUMP_STRENGTH
            
            # --- Game Loop ---
            update_game(max_y, max_x)
            draw_game(stdscr, max_y, max_x)
            
            time.sleep(TICK_RATE)

        # 5. Game Over Screen and Replay Prompt
        stdscr.clear()
        
        max_y, max_x = stdscr.getmaxyx()
        
        message = f"!!! GAME OVER !!! | Final Score: {score}"
        prompt = "Play Again? (Y/N)"
        
        stdscr.addstr(max_y // 2 - 2, max_x // 2 - len(message) // 2, message, curses.A_BOLD | curses.A_REVERSE)
        stdscr.addstr(max_y // 2, max_x // 2 - len(prompt) // 2, prompt, curses.A_BOLD)
        
        stdscr.refresh()
        
        # Wait for Y or N input
        stdscr.nodelay(False) 
        while True:
            choice = stdscr.getch()
            if choice == ord('y') or choice == ord('Y'):
                break
            elif choice == ord('n') or choice == ord('N') or choice == 27:
                return # Exit main function

# curses.wrapper safely initializes and shuts down the terminal environment
if __name__ == "__main__":
    # Ensure the clear_screen function is called before starting the curses environment
    clear_screen()
    
    if os.name == 'nt' and not sys.modules.get('curses'):
        print("NOTE: On Windows, you likely need to install the 'windows-curses' library.")
        print("Run: pip install windows-curses")
        time.sleep(2)
        
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The game might have crashed because the terminal window is too small or 'curses' is not installed correctly.")
        print("Please ensure your terminal is large and try again.")
