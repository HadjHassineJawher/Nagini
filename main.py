import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
SCORE_SECTION_HEIGHT = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - SCORE_SECTION_HEIGHT) // GRID_SIZE
WHITE = (255, 255, 255)
SNAKE_COLOR = (22, 37, 33)
SNAKE_HEAD_COLOR = (60, 71, 75)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)
SCORE_FONT_SIZE = 24
GAME_OVER_FONT_SIZE = 48
RESTART_FONT_SIZE = 24
HIGH_SCORE_FONT_SIZE = 24
HEIGHT_SCORE_COLOR = (80, 21, 55)
# New Food colors
FOOD_COLORS = [(176, 152, 164), (69, 80, 59), (252, 208, 161), (11, 85, 99), (111, 88, 75), (125, 223, 100), (131, 33, 97), (218, 65, 103)]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Djo's First Game ")

# Initialize Snake
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (0, 0)

# Initialize Food
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
food_color = random.choice(FOOD_COLORS)

# Initialize Score
score = 0

# Initialize High Score
high_score = 0
high_score_font = pygame.font.Font(None, HIGH_SCORE_FONT_SIZE)

# Initialize Fonts with the specified sizes
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
restart_font = pygame.font.Font(None, RESTART_FONT_SIZE)

game_over = False
game_over_text = None

# Flag to check if the user beat the high score
beat_high_score = False

# Function to reset the game
def reset_game():
    global snake, snake_direction, food, score, game_over, game_over_text, food_color, beat_high_score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (0, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    food_color = random.choice(FOOD_COLORS)  # Randomize food color
    score = 0
    game_over = False
    game_over_text = None
    if beat_high_score:
        beat_high_score = False

# Load High Score from a file (if it exists)
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score to a file before quitting
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()

    if game_over:
        # Display game over message and offer a restart option
        if game_over_text is None:
            game_over_text = game_over_font.render("Game Over!", True, (209, 17, 73))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (WIDTH // 2, HEIGHT // 2 - 20)
            screen.blit(game_over_text, game_over_rect)
            restart_text = restart_font.render("Press R to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect()
            restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 40)
            screen.blit(restart_text, restart_rect)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                reset_game()
                if beat_high_score:
                    high_score_font = pygame.font.Font(None, HIGH_SCORE_FONT_SIZE)
                    beat_high_score = False
    else:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_direction != (0, 1):
            snake_direction = (0, -1)
        elif keys[pygame.K_DOWN] and snake_direction != (0, -1):
            snake_direction = (0, 1)
        elif keys[pygame.K_LEFT] and snake_direction != (1, 0):
            snake_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
            snake_direction = (1, 0)


        new_head = (
            (snake[0][0] + snake_direction[0]) % GRID_WIDTH,
            (snake[0][1] + snake_direction[1]) % GRID_HEIGHT
        )
        snake.insert(0, new_head)

        # Check if the snake eats the food
        if snake[0] == food:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            food_color = random.choice(FOOD_COLORS)
            score += 1
            if score > high_score:
                high_score = score
                beat_high_score = True

        else:
            snake.pop()

        if snake[0] in snake[1:]:
            game_over = True

        screen.fill(WHITE)

        for i, segment in enumerate(snake):
            x, y = segment
            if i == 0:

                pygame.draw.rect(
                    screen, SNAKE_HEAD_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )

                eye_size = GRID_SIZE // 5
                eye_spacing = GRID_SIZE // 4
                eye_height = GRID_SIZE // 3
                eye_center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + eye_height)
                left_eye_pos = (eye_center[0] - eye_spacing, eye_center[1])
                right_eye_pos = (eye_center[0] + eye_spacing, eye_center[1])
                pygame.draw.circle(screen, EYE_COLOR, left_eye_pos, eye_size)
                pygame.draw.circle(screen, EYE_COLOR, right_eye_pos, eye_size)
                # Draw pupils
                pupil_size = eye_size // 2
                left_pupil_pos = (left_eye_pos[0] + pupil_size, left_eye_pos[1])
                right_pupil_pos = (right_eye_pos[0] + pupil_size, right_eye_pos[1])
                pygame.draw.circle(screen, PUPIL_COLOR, left_pupil_pos, pupil_size)
                pygame.draw.circle(screen, PUPIL_COLOR, right_pupil_pos, pupil_size)
            else:
                pygame.draw.rect(
                    screen, SNAKE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )


        pygame.draw.circle(
            screen, food_color, (food[0] * GRID_SIZE + GRID_SIZE // 2, food[1] * GRID_SIZE + GRID_SIZE // 2),
            GRID_SIZE // 2
        )


        pygame.draw.rect(screen, (200, 200, 200), (0, HEIGHT - SCORE_SECTION_HEIGHT, WIDTH, SCORE_SECTION_HEIGHT))

        # Display Score and High Score in the score section at the bottom, centered
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.center = (WIDTH // 4, HEIGHT - SCORE_SECTION_HEIGHT // 2)
        screen.blit(score_text, score_rect)

        if beat_high_score:
            high_score_text = high_score_font.render(f"High Score: {high_score}", True, HEIGHT_SCORE_COLOR)
        else:
            high_score_text = high_score_font.render(f"High Score: {high_score}", True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (3 * WIDTH // 4, HEIGHT - SCORE_SECTION_HEIGHT // 2)
        screen.blit(high_score_text, high_score_rect)

    pygame.display.flip()
    clock.tick(10)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score to a file before quitting
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
