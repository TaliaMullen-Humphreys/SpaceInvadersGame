import pygame
from pygame import mixer
import random
import math

# Initialise The Pygame
pygame.init()

# Create The Screen (X Axis , Y Axis)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player (The Y Axis Goes Down -> 600 Is The Bottom Of The Screen)
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Respawns In Random Places
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  # Same As Space Ship
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # Means You Can't See The Bullet / When = "Fire" The Bullet Will Move

# Score Variable
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Font , Font Size

textX = 10
textY = 10

# Game Over Text Function
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Shows Score On The Screen (Text Must Be Rendered Before Blit)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Function Draws Player On The Screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# Function Draws Enemy On The Screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Function To Fire Bullet When Space Bar Pressed

def fire_bullet(x, y):
    global bullet_state  # Allows Variable To Be Accessed In Function
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Ensures The Bullet Shoots From The Centre Of SpaceShip


# Collision Between Bullet And Enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop (Everything In The Game Must Be In The Main Gain Loop)
running = True

while running:

    # RGB - Red, Green, Blue (Goes Up To 255)
    screen.fill((0, 0, 0))
    # Add Background Image
    screen.blit(background, (0, 0))

    # Allows You To Quit The Game (Otherwise You Are Stuck In An Infinite Loop)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If Keystroke Is Pressed Check Whether It Is Right Or Left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get Current X Coordinate Of The Player
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Call Player After Filling Screen Otherwise It Won't Appear On Screen
    playerX += playerX_change

    # This Stops The Player From Going Off The Screen
    if playerX <= 0:
        playerX = 0
    # We Take 64 Off The X Coordinate Limit Because Out Image Is 64 Pixels Large
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
