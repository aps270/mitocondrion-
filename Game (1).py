import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
GLUCOSE_SIZE = 30
OBSTACLE_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mitochondria Master")

# Player settings
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player_color = GREEN
player_speed_x = 0
player_speed_y = 0
player_atp = 0

# Glucose molecules
glucose_list = []
glucose_speed = 3

# Obstacles
obstacle_list = []
obstacle_speed = 2

# Timer
game_over = False
game_start_time = pygame.time.get_ticks()
game_duration = 120000  # 2 minutes

# Fonts
font = pygame.font.Font(None, 36)

def draw_player():
    pygame.draw.rect(screen, player_color, player)

def draw_glucose(glucose):
    glucose_center = (glucose.x + GLUCOSE_SIZE // 2, glucose.y + GLUCOSE_SIZE // 2)
    pygame.draw.circle(screen, WHITE, glucose_center, GLUCOSE_SIZE // 2)

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, RED, obstacle)

def draw_score(atp):
    score_text = font.render(f"ATP: {atp}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_timer():
    current_time = pygame.time.get_ticks()
    remaining_time = max(0, (game_start_time + game_duration - current_time) // 1000)
    timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
    screen.blit(timer_text, (WIDTH - 150, 10))

def check_collision(obj1, obj2):
    return obj1.colliderect(obj2)

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed_x = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    player_speed_x = PLAYER_SPEED
                if event.key == pygame.K_UP:
                    player_speed_y = -PLAYER_SPEED
                if event.key == pygame.K_DOWN:
                    player_speed_y = PLAYER_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed_y = 0

    if not game_over:
        player.x += player_speed_x
        player.y += player_speed_y

        # Keep the player within the game window
        player.x = max(0, min(player.x, WIDTH - PLAYER_SIZE))
        player.y = max(0, min(player.y, HEIGHT - PLAYER_SIZE))

        # Generate glucose
        if random.randint(1, 100) < 2:
            glucose_list.append(pygame.Rect(random.randint(0, WIDTH - GLUCOSE_SIZE), 0, GLUCOSE_SIZE, GLUCOSE_SIZE))

        # Generate obstacles
        if random.randint(1, 100) < 2:
            obstacle_list.append(pygame.Rect(random.randint(0, WIDTH - OBSTACLE_SIZE), 0, OBSTACLE_SIZE, OBSTACLE_SIZE))

        # Move and draw glucose
        for glucose in glucose_list:
            glucose.y += glucose_speed
            draw_glucose(glucose)

        # Move and draw obstacles
        for obstacle in obstacle_list:
            obstacle.y += obstacle_speed
            draw_obstacle(obstacle)

        # Check for collisions with glucose
        for glucose in glucose_list[:]:
            if check_collision(player, glucose):
                glucose_list.remove(glucose)
                player_atp += 1

        # Check for collisions with obstacles
        for obstacle in obstacle_list[:]:
            if check_collision(player, obstacle):
                obstacle_list.remove(obstacle)
                player_atp -= 1

        draw_player()
        draw_score(player_atp)
        draw_timer()

        # Check if the game time is up
        current_time = pygame.time.get_ticks()
        if current_time - game_start_time >= game_duration:
            game_over = True

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
sys.exit()