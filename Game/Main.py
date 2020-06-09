import pygame
import math
import random

from pygame import font, mixer
from pygame.math import Vector2
import threading

# Initialize the game

pygame.init()
screen = pygame.display.set_mode((500, 500))

# Background
background = pygame.image.load("space.jpg")

# Sounds
bullet_sound = mixer.Sound("shoot.wav")
explosion_sound = mixer.Sound("explosion.wav")
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Asteroid Shooter")
icon = pygame.image.load("asteroid.png")
pygame.display.set_icon(icon)

# Player
playerImage = pygame.image.load("space-invaders.png")
playerSpeed = 5;
player_position = Vector2(436, 426)

# Asteroid
asteroidImage = pygame.image.load("asteroid.png")
asteroid_speed = 1;
asteroid_position = Vector2(random.randint(0, 436), 50)

# Bullet
bullet_image = pygame.image.load("bullet.png")
bulletSpeed = 10
bullet_position = Vector2(0, player_position.y)
bullet_state = "Ready"

# Score
score_value = 0;
score_font = pygame.font.Font('ExpressionPro.ttf', 32)
score_position = Vector2(10, 10)

# Game Over
game_over_font = pygame.font.Font('ExpressionPro.ttf',50)
game_over_position = Vector2(150,200)

def game_over():
    game_over = game_over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over,game_over_position)
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(200,250))


def show_score():
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, score_position)


def player():
    screen.blit(playerImage, player_position)


def asteroid():
    screen.blit(asteroidImage, asteroid_position)


def asteroid_respawn():
    global asteroid_position

    asteroid_position.x = random.randint(0, 436)
    asteroid_position.y = 50


def speed_up():
    global asteroid_speed
    t = threading.Timer(5.0, speed_up)
    t.setDaemon(True)
    t.start()
    asteroid_speed += 0.2


def check_bounds():
    global player_position
    if player_position.x <= 0:
        player_position.x = 0
    elif player_position.x >= 436:
        player_position.x = 436

    if player_position.y <= 0:
        player_position.y = 0
    elif player_position.y >= 436:
        player_position.y = 436


def fire_bullet():
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_image, (bullet_position.x, bullet_position.y - 20))


def is_collision():
    distance = math.hypot(asteroid_position.x - bullet_position.x, asteroid_position.y - bullet_position.y)
    return distance < 50

def is_dead():
    global asteroid_speed
    distance = math.hypot(asteroid_position.x - player_position.x, asteroid_position.y - player_position.y)
    if distance < 30:
        asteroid_speed = 0
        return True

pressed_keys = {"Left": False, "Right": False, "Up": False, "Down": False}
# Game Loop
speed_up()
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not is_dead():
            if event.key == pygame.K_LEFT:
                pressed_keys["Left"] = True
            if event.key == pygame.K_RIGHT:
                pressed_keys["Right"] = True

            if event.key == pygame.K_SPACE and bullet_state is "Ready":
                bullet_position.x = player_position.x - (-16)
                bullet_position.y = player_position.y
                fire_bullet()
                bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressed_keys["Left"] = False
            if event.key == pygame.K_RIGHT:
                pressed_keys["Right"] = False
            if event.key == pygame.K_UP:
                pressed_keys["Up"] = False
            if event.key == pygame.K_DOWN:
                pressed_keys["Down"] = False

    if pressed_keys["Left"]:
        player_position.x -= playerSpeed
    if pressed_keys["Right"]:
        player_position.x += playerSpeed

    check_bounds()

    # Check Collision
    if is_collision():
        bullet_position.y = 0
        explosion_sound.play()
        asteroid_respawn()
        bullet_state = "Ready"
        score_value += 1

    # Bullet Movement
    if bullet_position.y <= 0:
        bullet_state = "Ready"

    if bullet_state is "Fire":
        fire_bullet()
        bullet_position.y -= bulletSpeed

    # Asteroid Movement
    if asteroid_position.y >= 436:
        asteroid_respawn()
    asteroid_position.y += asteroid_speed

    if is_dead():
        game_over()
    else:
        player()
        asteroid()
        show_score()

    pygame.display.update()
