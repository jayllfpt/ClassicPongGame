import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Load the background images
background_images = [
    pygame.image.load("ClassicPongGame/background1.jpg"),
    pygame.image.load("ClassicPongGame/background2.jpg"),
    pygame.image.load("ClassicPongGame/background3.jpg"),
    pygame.image.load("ClassicPongGame/background4.jpg")
]

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the paddles
paddle_width = 15
paddle_height = 60
paddle_speed = 5
left_paddle_pos = pygame.Rect(50, height / 2 - paddle_height / 2, paddle_width, paddle_height)
right_paddle_pos = pygame.Rect(width - 50 - paddle_width, height / 2 - paddle_height / 2, paddle_width, paddle_height)

# Set up the ball
ball_radius = 10
ball_pos = pygame.Rect(width / 2 - ball_radius / 2, height / 2 - ball_radius / 2, ball_radius, ball_radius)
ball_speed_x = random.choice([-2, 2])
ball_speed_y = random.choice([-2, 2])

# Set up the score variables
left_score = 0
right_score = 0
font = pygame.font.Font(None, 36)

# Load sound effects
paddle_hit_sound = pygame.mixer.Sound("ClassicPongGame/paddle_hit.wav")
wall_hit_sound = pygame.mixer.Sound("ClassicPongGame/wall_hit.wav")
score_sound = pygame.mixer.Sound("ClassicPongGame/score.wav")

# Set the default background image
current_background_index = 0
current_background = background_images[current_background_index]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                current_background_index = 1
                current_background = background_images[current_background_index]
            elif event.key == pygame.K_n:
                current_background_index = 2
                current_background = background_images[current_background_index]
            elif event.key == pygame.K_m:
                current_background_index = 3
                current_background = background_images[current_background_index]
            elif event.key == pygame.K_v:
                current_background_index = 0
                current_background = background_images[current_background_index]

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and left_paddle_pos.y > 0:
        left_paddle_pos.y -= paddle_speed
    if keys[pygame.K_f] and left_paddle_pos.y < height - paddle_height:
        left_paddle_pos.y += paddle_speed
    if keys[pygame.K_u] and right_paddle_pos.y > 0:
        right_paddle_pos.y -= paddle_speed
    if keys[pygame.K_j] and right_paddle_pos.y < height - paddle_height:
        right_paddle_pos.y += paddle_speed

    # Move the ball
    ball_pos.x += ball_speed_x
    ball_pos.y += ball_speed_y

    # Check collision with paddles
    if ball_pos.colliderect(left_paddle_pos) or ball_pos.colliderect(right_paddle_pos):
        ball_speed_x *= -1
        paddle_hit_sound.play()

    # Check collision with walls
    if ball_pos.y > height - ball_radius or ball_pos.y < 0:
        ball_speed_y *= -1
        wall_hit_sound.play()

    # Check if ball goes off the screen
    if ball_pos.x < 0:
        right_score += 1
        score_sound.play()
        ball_pos.x = width / 2 - ball_radius / 2
        ball_pos.y = height / 2 - ball_radius / 2
        ball_speed_x = random.choice([-2, 2])
        ball_speed_y = random.choice([-2, 2])
    elif ball_pos.x > width:
        left_score += 1
        score_sound.play()
        ball_pos.x = width / 2 - ball_radius / 2
        ball_pos.y = height / 2 - ball_radius / 2
        ball_speed_x = random.choice([-2, 2])
        ball_speed_y = random.choice([-2, 2])

    # Draw the background image
    screen.blit(current_background, (0, 0))

    # Draw the paddles and the ball
    pygame.draw.rect(screen, BLUE, left_paddle_pos)
    pygame.draw.rect(screen, RED, right_paddle_pos)
    pygame.draw.ellipse(screen, WHITE, ball_pos)

    # Draw the score
    left_score_text = font.render(str(left_score), True, GREEN if left_score > right_score else RED if left_score < right_score else WHITE)
    right_score_text = font.render(str(right_score), True, GREEN if right_score > left_score else RED if right_score < left_score else WHITE)
    screen.blit(left_score_text, (width / 4, 10))
    screen.blit(right_score_text, (width * 3 / 4, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
