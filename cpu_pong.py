import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER1_COLOR = (0, 255, 255)
PLAYER2_COLOR = (255, 100, 100)
BALL_COLOR = (255, 255, 0)
BG_COLOR = (20, 20, 60)
FLASH_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CPU Pong")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Ball setup
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = random.choice([-5, 5])  # Adjusted for moderate speed
ball_dy = random.choice([-5, 5])

# Paddle setup
paddle1_x = 10
paddle1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_x = SCREEN_WIDTH - 10 - PADDLE_WIDTH
paddle2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle_speed = 10  # Adjusted paddle speed

# Game state variables
running = True
game_active = False
score1 = 0
score2 = 0
flash_counter = 0

# -------------------------------
# Functions
# -------------------------------

# Reset the ball to the center of the screen
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = random.choice([-5, 5])  # Reset ball speed and direction
    ball_dy = random.choice([-5, 5])

# Draw paddles, ball, and scores
def draw_objects():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PLAYER1_COLOR, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, PLAYER2_COLOR, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, BALL_COLOR, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    score_text = font_large.render(f"{score1}  {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

# Draw the start screen
def draw_start_screen():
    global flash_counter
    screen.fill(BG_COLOR)
    current_color = FLASH_COLORS[(flash_counter // 20) % len(FLASH_COLORS)]
    flash_counter += 1
    title_text = font_large.render("CPU Pong", True, current_color)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    start_text = font_small.render("Press SPACE to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))

# Check for collisions
def check_collision():
    global ball_dx, ball_dy, score1, score2, game_active

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collision with paddles
    if (
        paddle1_x < ball_x < paddle1_x + PADDLE_WIDTH
        and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT
    ) or (
        paddle2_x < ball_x + BALL_SIZE < paddle2_x + PADDLE_WIDTH
        and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT
    ):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:  # Player 2 scores
        score2 += 1
        reset_ball()
    if ball_x > SCREEN_WIDTH:  # Player 1 scores
        score1 += 1
        reset_ball()

    # Check for winner
    if score1 == 10 or score2 == 10:  # First to 10 wins
        game_active = False
        winner = "Player 1" if score1 == 10 else "Player 2"
        draw_winner_screen(winner)
        pygame.time.wait(3000)

# Draw winner screen
def draw_winner_screen(winner):
    screen.fill(BG_COLOR)
    winner_text = font_large.render(f"{winner} Wins!", True, WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.flip()

# Move the CPU paddles with independent behavior
def move_paddles():
    global paddle1_y, paddle2_y

    # Player 1 (CPU): Slower and more likely to miss
    if random.randint(0, 20) > 10:  # Slower reaction threshold
        if ball_y > paddle1_y + PADDLE_HEIGHT // 2 and paddle1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle1_y += paddle_speed - random.randint(1, 3)  # Slower speed with randomness
        elif ball_y < paddle1_y + PADDLE_HEIGHT // 2 and paddle1_y > 0:
            paddle1_y -= paddle_speed - random.randint(1, 3)  # Slower speed with randomness

    # Player 2 (CPU): Faster and more accurate
    if random.randint(0, 15) > 5:  # Faster reaction threshold
        if ball_y > paddle2_y + PADDLE_HEIGHT // 2 and paddle2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle2_y += paddle_speed + random.randint(2, 4)  # Faster speed with randomness
        elif ball_y < paddle2_y + PADDLE_HEIGHT // 2 and paddle2_y > 0:
            paddle2_y -= paddle_speed + random.randint(2, 4)  # Faster speed with randomness

    # Introduce a deliberate "miss"
    if random.randint(0, 100) > 90:  # 10% chance to miss
        if random.choice([True, False]):  # Randomly pick a paddle
            paddle1_y += random.choice([-20, 20])  # Move Player 1 erratically
        else:
            paddle2_y += random.choice([-20, 20])  # Move Player 2 erratically


# -------------------------------
# Main Game Loop
# -------------------------------

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start the game with SPACE key
        if not game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True
                score1, score2 = 0, 0  # Reset scores

    if game_active:
        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Move CPU paddles
        move_paddles()

        # Check for collisions
        check_collision()

        # Draw game objects
        draw_objects()
    else:
        # Draw start screen
        draw_start_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
