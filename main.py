# X axis in normal Y axis is mirror of cartesian axis

import pygame
import random
import math

# inialize the pygame
pygame.init()

# creates the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space_background3.png')

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceshipblue.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(80)

# single enemy
'''
enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 2
enemyY_change = 20
'''
# bullet
# ready - You can't see the bullet on the screen
# fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = 'ready'

# score
score_value = 0
# font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('Gameshow.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('Gameshow.ttf', 128)


def game_over():
    over = over_font.render('GAME OVER' + str(score_value), True, (255, 255, 255))
    screen.blit(over, (100, 250))


# display score on screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit is used to draw the acrade symbol on the screen blit means to draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit is used to draw the acrade symbol on the screen blit means to draw
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))  # 16 and 10 are to make the bullet appears in between the spaceship


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # Screen Background RGB
    screen.fill((0, 0, 0))

    # background img placing
    screen.blit(background, (0, 0))

    # pygame.event.get(): lists out all the events in the game
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:  # means pressing
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # get the x cood of the spcaeship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # means releasing key stroke
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # adding the boundary so that the spaceship doesnot go out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # its 736 not 800 as we need to consider the size of the spaceship
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # its 736 not 800 as we need to consider the size of the spaceship
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value = score_value + 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change

    # call the player function to display the symbol after fill otherwise the symbol will be under the screen
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # update the screen with the selected colour
