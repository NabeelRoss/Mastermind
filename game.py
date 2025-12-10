import pygame
import random

# --- Constants & Configuration ---
GAME_WIDTH = 500       # Width of the playable game area
SIDEBAR_WIDTH = 400    # Width of the rules sidebar
WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
HEIGHT = 800           # Increased height to 800 for better spacing
FPS = 60
TITLE = "Mastermind: Pygame Edition"

# Colors (R, G, B)
DARK_BG = (30, 30, 30)
PANEL_BG = (50, 50, 50)
SIDEBAR_BG = (40, 40, 40)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GOLD = (241, 196, 15)
HOVER_COLOR = (100, 100, 100)

# Game Colors Map
COLOR_MAP = {
    "R": (231, 76, 60),   # Red
    "G": (46, 204, 113),  # Green
    "B": (52, 152, 219),  # Blue
    "Y": (241, 196, 15),  # Yellow
    "W": (236, 240, 241), # White
    "O": (230, 126, 34)   # Orange
}
COLORS_LIST = ["R", "G", "B", "Y", "W", "O"]

# Game Settings
TRIES = 10
CODE_LENGTH = 4
PEG_RADIUS = 18
SMALL_PEG_RADIUS = 8
SPACING_Y = 55  # Space between rows

# --- Game Logic Functions ---

def generate_code():
    code = []
    for _ in range(CODE_LENGTH):
        color = random.choice(COLORS_LIST)
        code.append(color)
    return code

def check_code(guess, real_code):
    color_counts = {}
    correct_pos = 0
    incorrect_pos = 0

    # Create a frequency map for the real code
    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1
      
    # First pass: Check for correct positions (Black pegs)
    temp_real = list(real_code)
    temp_guess = list(guess)
    matched_indices = [False] * CODE_LENGTH

    for i in range(CODE_LENGTH):
        if temp_guess[i] == temp_real[i]:
            correct_pos += 1
            color_counts[temp_guess[i]] -= 1
            matched_indices[i] = True

    # Second pass: Check for wrong positions (White pegs)
    for i in range(CODE_LENGTH):
        if not matched_indices[i]: 
            color = temp_guess[i]
            if color in color_counts and color_counts[color] > 0:
                incorrect_pos += 1
                color_counts[color] -= 1
    
    return correct_pos, incorrect_pos

# --- UI Drawing Functions ---

def draw_text(screen, text, font, color, x, y, align="center"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if align == "center":
        rect.center = (x, y)
    elif align == "left":
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect

def draw_circle_button(screen, color, x, y, radius, outline=None):
    if outline:
        pygame.draw.circle(screen, outline, (x, y), radius + 2)
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_sidebar(screen, title_font, body_font):
    # Draw Background for sidebar
    rect = pygame.Rect(GAME_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, SIDEBAR_BG, rect)
    pygame.draw.line(screen, WHITE, (GAME_WIDTH, 0), (GAME_WIDTH, HEIGHT), 2)

    # Margins
    x_start = GAME_WIDTH + 30
    y = 30

    # Title
    draw_text(screen, "HOW TO PLAY", title_font, GOLD, GAME_WIDTH + SIDEBAR_WIDTH // 2, y)
    y += 50

    # Rules Text
    rules = [
        "1. Guess the secret 4-color code.",
        "2. You have 10 attempts.",
        "3. Colors can be repeated.",
        "4. Click colors to fill the row.",
        "5. Press GUESS to submit."
    ]

    for line in rules:
        draw_text(screen, line, body_font, WHITE, x_start, y, align="left")
        y += 35

    y += 20
    draw_text(screen, "FEEDBACK PEGS:", title_font, GOLD, GAME_WIDTH + SIDEBAR_WIDTH // 2, y)
    y += 50

    # Explanation of Pegs
    # Black/Red Peg
    draw_circle_button(screen, (0, 0, 0), x_start + 10, y + 10, SMALL_PEG_RADIUS)
    draw_circle_button(screen, (200, 50, 50), x_start + 10, y + 10, SMALL_PEG_RADIUS - 2)
    draw_text(screen, "Right Color, Right Position", body_font, WHITE, x_start + 40, y, align="left")
    y += 40

    # White Peg
    draw_circle_button(screen, (0, 0, 0), x_start + 10, y + 10, SMALL_PEG_RADIUS)
    draw_circle_button(screen, (255, 255, 255), x_start + 10, y + 10, SMALL_PEG_RADIUS - 2)
    draw_text(screen, "Right Color, Wrong Position", body_font, WHITE, x_start + 40, y, align="left")
    y += 40
    
    # Empty
    draw_text(screen, "No Peg: Color not in code", body_font, GRAY, x_start + 40, y, align="left")

    # Footer
    draw_text(screen, "Good Luck!", title_font, GOLD, GAME_WIDTH + SIDEBAR_WIDTH // 2, HEIGHT - 50)


def draw_ui(screen, current_guess, attempts, game_state, message, font, small_font):
    # Draw Background (Game Area Only)
    pygame.draw.rect(screen, DARK_BG, (0, 0, GAME_WIDTH, HEIGHT))

    # 1. Draw Title
    draw_text(screen, "MASTERMIND", font, WHITE, GAME_WIDTH // 2, 30)

    # 2. Draw Board (Rows)
    for i in range(TRIES):
        y = 80 + i * SPACING_Y
        # Row background (alternating slightly)
        if i == attempts and game_state == "PLAYING":
            # Highlight active row
            pygame.draw.rect(screen, PANEL_BG, (20, y - 25, GAME_WIDTH - 40, 50), border_radius=10)
            pygame.draw.rect(screen, (100, 100, 255), (20, y - 25, GAME_WIDTH - 40, 50), 2, border_radius=10)
        else:
            pygame.draw.rect(screen, PANEL_BG, (20, y - 25, GAME_WIDTH - 40, 50), border_radius=10)

        draw_text(screen, str(i + 1), small_font, GRAY, 40, y)

    # 3. Draw Color Picker (Positioned lower than before)
    picker_y = 670   # Moved down slightly to center in the gap
    picker_x_start = 80
    gap = 60
    
    buttons = []
    for idx, color_key in enumerate(COLORS_LIST):
        x = picker_x_start + idx * gap
        color = COLOR_MAP[color_key]
        draw_circle_button(screen, color, x, picker_y, 22, outline=WHITE)
        buttons.append({"color": color_key, "rect": pygame.Rect(x-22, picker_y-22, 44, 44)})

    # 4. Action Buttons (Positioned with margin from bottom)
    button_y = 730   # Moved down, but leaves ~35px margin at bottom
    
    # GUESS Button (Left side)
    submit_btn_rect = pygame.Rect(GAME_WIDTH // 2 - 110, button_y, 100, 35)
    color_submit = (50, 200, 50) if len(current_guess) == CODE_LENGTH else GRAY
    pygame.draw.rect(screen, color_submit, submit_btn_rect, border_radius=5)
    draw_text(screen, "GUESS", small_font, WHITE, submit_btn_rect.centerx, submit_btn_rect.centery)

    # DELETE Button (Right side)
    del_btn_rect = pygame.Rect(GAME_WIDTH // 2 + 10, button_y, 100, 35)
    pygame.draw.rect(screen, (200, 50, 50), del_btn_rect, border_radius=5)
    draw_text(screen, "DELETE", small_font, WHITE, del_btn_rect.centerx, del_btn_rect.centery)

    return buttons, del_btn_rect, submit_btn_rect

def draw_guesses(screen, history, current_guess, active_row, game_state):
    # Draw History
    for row, (guess, feedback) in enumerate(history):
        y = 80 + row * SPACING_Y
        start_x = 100
        
        # Draw the code pegs
        for i, color_key in enumerate(guess):
            draw_circle_button(screen, COLOR_MAP[color_key], start_x + i * 50, y, PEG_RADIUS)

        # Draw feedback pegs (Right side)
        correct, incorrect = feedback
        fx, fy = 350, y - 10
        
        # Draw correct (Black/Red)
        for _ in range(correct):
            pygame.draw.circle(screen, (0, 0, 0), (fx, fy), SMALL_PEG_RADIUS) # Black
            pygame.draw.circle(screen, (200, 50, 50), (fx, fy), SMALL_PEG_RADIUS - 1) # Red center
            fx += 20
        
        # Draw incorrect (White)
        for _ in range(incorrect):
            pygame.draw.circle(screen, (0, 0, 0), (fx, fy), SMALL_PEG_RADIUS) # Black border
            pygame.draw.circle(screen, (255, 255, 255), (fx, fy), SMALL_PEG_RADIUS - 1) # White center
            fx += 20

    # Draw Current Active Guess
    if game_state == "PLAYING" and active_row < TRIES:
        y = 80 + active_row * SPACING_Y
        start_x = 100
        for i, color_key in enumerate(current_guess):
            draw_circle_button(screen, COLOR_MAP[color_key], start_x + i * 50, y, PEG_RADIUS)

def draw_game_over(screen, game_state, secret_code, font, large_font):
    # Overlay covers only the game width area, not the sidebar
    overlay = pygame.Surface((GAME_WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Semi-transparent black
    screen.blit(overlay, (0, 0))

    if game_state == "WON":
        msg = "YOU WON!"
        color = (46, 204, 113)
    else:
        msg = "GAME OVER"
        color = (231, 76, 60)

    draw_text(screen, msg, large_font, color, GAME_WIDTH // 2, HEIGHT // 2 - 50)
    
    # Reveal Code
    draw_text(screen, "The code was:", font, WHITE, GAME_WIDTH // 2, HEIGHT // 2 + 10)
    start_x = GAME_WIDTH // 2 - ((CODE_LENGTH * 50) // 2) + 25
    y = HEIGHT // 2 + 60
    for i, color_key in enumerate(secret_code):
        draw_circle_button(screen, COLOR_MAP[color_key], start_x + i * 50, y, PEG_RADIUS)

    # Restart Prompt
    draw_text(screen, "Press SPACE to Play Again", font, WHITE, GAME_WIDTH // 2, HEIGHT // 2 + 120)

# --- Main Execution ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    font_large = pygame.font.SysFont("arial", 48, bold=True)
    font_med = pygame.font.SysFont("arial", 28, bold=True)
    font_small = pygame.font.SysFont("arial", 18)
    font_rules = pygame.font.SysFont("arial", 20)

    # Game State Variables
    running = True
    
    # Reset loop variables
    while running:
        secret_code = generate_code()
        current_guess = []
        history = [] 
        attempts = 0
        game_state = "PLAYING" 
        message = ""

        # Round Loop
        playing_round = True
        while playing_round:
            clock.tick(FPS)
            
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing_round = False
                    running = False
                
                if game_state == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        
                        # Only handle clicks inside Game Area
                        if mx < GAME_WIDTH:
                            # Check Color Picker Clicks
                            for btn in color_buttons:
                                if btn["rect"].collidepoint(mx, my):
                                    if len(current_guess) < CODE_LENGTH:
                                        current_guess.append(btn["color"])
                            
                            # Check Delete Button
                            if del_rect.collidepoint(mx, my):
                                if len(current_guess) > 0:
                                    current_guess.pop()

                            # Check Submit Button
                            if submit_rect.collidepoint(mx, my):
                                if len(current_guess) == CODE_LENGTH:
                                    # Logic Check
                                    correct, incorrect = check_code(current_guess, secret_code)
                                    history.append((current_guess, (correct, incorrect)))
                                    
                                    if correct == CODE_LENGTH:
                                        game_state = "WON"
                                    elif len(history) >= TRIES:
                                        game_state = "LOST"
                                    else:
                                        attempts += 1
                                        current_guess = []
                
                # Check for Restart
                if game_state in ["WON", "LOST"]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            playing_round = False 

            # 2. Drawing
            color_buttons, del_rect, submit_rect = draw_ui(screen, current_guess, attempts, game_state, message, font_med, font_small)
            draw_guesses(screen, history, current_guess, attempts, game_state)
            draw_sidebar(screen, font_med, font_rules) # Draw the new sidebar

            if game_state != "PLAYING":
                draw_game_over(screen, game_state, secret_code, font_med, font_large)

            # 3. Update Display
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()