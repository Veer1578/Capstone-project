import math
import random
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Player starting position
PLAYER_START_X = 370
PLAYER_START_Y = 380

# Enemy settings
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 1
ENEMY_SPEED_Y = 20

# Bullet settings
BULLET_SPEED = 10
COLLISION_DISTANCE = 27

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerx = PLAYER_START_X
playery = PLAYER_START_Y
playerx_change = 0

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyy.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyx_change.append(ENEMY_SPEED_X)
    enemyy_change.append(ENEMY_SPEED_Y)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = playery
bulletx_change = 0
bullety_change = BULLET_SPEED
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Functions


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 220))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bulletimg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    # Use center alignment for better accuracy
    distance = math.sqrt((enemyX + 32 - (bulletX + 16)) **
                         2 + (enemyY + 32 - bulletY) ** 2)
    return distance < COLLISION_DISTANCE


# Game Loop
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -4
            if event.key == pygame.K_RIGHT:
                playerx_change = 4
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bulletx = playerx
                bullety = playery
                fire_bullet(bulletx, bullety)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerx_change = 0

    # Player movement
    playerx += playerx_change
    playerx = max(0, min(playerx, SCREEN_WIDTH - 64))

    # Enemy movement
    if not game_over:
        for i in range(num_of_enemies):
            if enemyy[i] > 340:
                game_over = True
                break

            enemyx[i] += enemyx_change[i]
            if enemyx[i] <= 0 or enemyx[i] >= SCREEN_WIDTH - 64:
                enemyx_change[i] *= -1
                enemyy[i] += enemyy_change[i]

            # Collision
            if is_collision(enemyx[i], enemyy[i], bulletx, bullety):
                bullety = playery
                bullet_state = 'ready'
                score_value += 1
                enemyx[i] = random.randint(0, SCREEN_WIDTH - 64)
                enemyy[i] = random.randint(
                    ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

            enemy(enemyx[i], enemyy[i], i)

    # Bullet movement
    if bullet_state == 'Fire':
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change
        if bullety <= 0:
            bullety = playery
            bullet_state = 'ready'

    # Show player and score
    player(playerx, playery)
    show_score(textx, texty)

    if game_over:
        for j in range(num_of_enemies):
            enemyy[j] = 2000
        game_over_text()

    pygame.display.update()
