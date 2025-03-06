import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Difficulty settings (Adjust FPS for different speeds)
DIFFICULTY = 25

# Window size
FRAME_SIZE_X = 900
FRAME_SIZE_Y = 480

# Initialize game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# FPS Controller
fps_controller = pygame.time.Clock()

# Snake default position and body
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food Position
def spawn_food():
    while True:
        food = [random.randrange(1, (FRAME_SIZE_X // 10)) * 10, random.randrange(1, (FRAME_SIZE_Y // 10)) * 10]
        if food not in snake_body:
            return food

food_pos = spawn_food()
food_spawn = True

# Direction control
direction = 'RIGHT'
change_to = direction

# Score
score = 0

# Function to display the score
def show_score(color, font, size, position='center'):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score: {score}', True, color)
    score_rect = score_surface.get_rect()

    if position == 'left':
        score_rect.midtop = (FRAME_SIZE_X / 10, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 1.25)

    game_window.blit(score_surface, score_rect)

# Game Over Function
def game_over():
    game_window.fill(BLACK)
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('GAME OVER', True, RED)
    game_over_rect = game_over_surface.get_rect(center=(FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4))
    game_window.blit(game_over_surface, game_over_rect)

    show_score(RED, 'times new roman', 30)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, ord('w')] and direction != 'DOWN':
                change_to = 'UP'
            elif event.key in [pygame.K_DOWN, ord('s')] and direction != 'UP':
                change_to = 'DOWN'
            elif event.key in [pygame.K_LEFT, ord('a')] and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key in [pygame.K_RIGHT, ord('d')] and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Validate direction change
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_pos = spawn_food()
    food_spawn = True

    # Update screen
    game_window.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(game_window, WHITE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over Conditions
    if snake_pos[0] < 0 or snake_pos[0] >= FRAME_SIZE_X or snake_pos[1] < 0 or snake_pos[1] >= FRAME_SIZE_Y:
        game_over()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Display Score
    show_score(WHITE, 'consolas', 20, 'left')

    # Refresh game screen
    pygame.display.update()

    # Frame Rate Control
    fps_controller.tick(DIFFICULTY)
