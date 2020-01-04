import pygame
import random
import math
import time

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((900, 800))

#background image 
game_background_level_one = pygame.image.load('space.png')

#Title and icon
pygame.display.set_caption("Space Fight")
icon = pygame.image.load('ship.png')
pygame.display.set_icon(icon)

#Adding player image on exact coordinate
playerImage = pygame.image.load('player.png')

#initital player position
playerX = 370
playerY = 650
playerX_Change = 0
PLAYER_SPEED_CONST = 4

#Enemy
enemyImage = pygame.image.load('enemy.png')
enemyX = random.randint(0,835)
enemyY = random.randint(0,200)
ENEMY_SPEED_CONST = 3
enemyX_Change = ENEMY_SPEED_CONST
enemyY_Change = 40

#Bullet
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 600
BULLET_SPEED_CONST = 3
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "ready"

#score details
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

#Game over text
gameover_font = pygame.font.Font('freesansbold.ttf', 72)


def player(x, y): 
    #drawing player
    screen.blit( playerImage, (x, y))

def enemy(x, y):
    #drawing player
    screen.blit( enemyImage, (x, y))

def fire_bullet(x, y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bulletImage,(x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt( (math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    # distance = 40 is from trial and error 
    if distance < 40: 
        return True
    else:
        return False

def display_score(x,y):
    score_displayed = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_displayed,(x,y))

def display_gameover():
    over_text = gameover_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

running = True

while running:
   
    #RGB values
    screen.fill((0, 0, 0))

    # Background Image fron top left corner
    screen.blit(game_background_level_one,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #key stroke: check right or left and move accordingly
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
           playerX_Change = -PLAYER_SPEED_CONST
        if event.key == pygame.K_RIGHT:
           playerX_Change = PLAYER_SPEED_CONST
        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                #getting the current positon of player
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_Change = 0

    #player need to be always on thr screen thats why it is in the loop
    playerX += playerX_Change
    
    #setting the boundry for player 
    if(playerX <= 0):
        playerX = 0
    elif(playerX >= 836):
        playerX = 836
    
    #enemy moments
    enemyX += enemyX_Change

    if enemyY > 700:
        display_gameover()
        

    if(enemyX <= 0):
        enemyX_Change = ENEMY_SPEED_CONST
        enemyY += enemyY_Change
    elif(enemyX >= 836):
        enemyX_Change = -ENEMY_SPEED_CONST
        enemyY += enemyY_Change

    #bullet movment 
    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"

    if bullet_state is 'fire':
         fire_bullet(bulletX, bulletY)
         bulletY -= bulletY_Change
    
    # Collision 
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 600
        bullet_state = "ready"
        score += 1
        enemyX = random.randint(0,835)
        enemyY = random.randint(0,200)

    enemy(enemyX, enemyY)
    display_score(scoreX, scoreY)
    player(playerX, playerY)
    pygame.display.update()