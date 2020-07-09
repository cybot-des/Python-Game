import pygame
import random
import math
from pygame import mixer
import time


# initializing pygame module
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))
running = True

# background details
background = pygame.image.load('spooky.jpg')

#background music
mixer.music.load('scary.wav')
mixer.music.play(-1)

# Display settings
pygame.display.set_caption('shoot d ghost !!!')
icon1 = pygame.image.load('enemy.png')
pygame.display.set_icon(icon1)

# player dimensions
playerImg = pygame.image.load('ghost2.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemmy dimensions
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 20
for i in range(num):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(0.6)


# sparks dimensions
sparkImg = pygame.image.load('clean.png')
sparkX = 0
sparkY = 480
sparkX_change = 0
sparkY_change = 10
spark_state = "ready"

# score board
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#game_over label
over = pygame.font.Font('freesansbold.ttf',64)

#coin dimensions
coinX = random.randint(0,768)
coinY = random.randint(0,568)


def game_over():

    gameOver = font.render("GAME OVER !!!",True,(255,255,255))
    screen.blit(gameOver, (200, 250))
    time.sleep(5.0)
    exit()



def score_board(x,y):
    score_val=font.render("Score :"+str(score),True,(255,255,255))
    screen.blit(score_val,(x,y))


def player(m, n):
    screen.blit(playerImg, (m, n))




def enemy(m, n, i):
    screen.blit(enemyImg[i], (m, n))

def fire_spark(x,y):
    global spark_state
    spark_state = "fire"
    screen.blit(sparkImg,(x+16,y+10))

def isShooted(enemyX,enemyY,sparkX,sparkY):
    dist=math.sqrt(math.pow(enemyX-sparkX,2)+ math.pow(enemyY-sparkY,2))
    if dist<20 :
        return True
    else:
        return False




# gaming loop (main while loop for event)
while running:
    screen.fill((50, 0, 50))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # making controls for ghost
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_UP:
                playerY_change = -5
            elif event.key == pygame.K_DOWN:
                playerY_change = 5
            elif event.key == pygame.K_SPACE:
                if spark_state == "ready":
                    sparkX=playerX
                    fire_spark(sparkX,sparkY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # player movement
    playerX += playerX_change
    playerY += playerY_change

    # putting restriction on movement of ghost with boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    if playerY >= 536:
        playerY = 536

    for i in range(num):
        #game-over
        dist1 = math.sqrt(math.pow(enemyX[i] - playerX, 2) + math.pow(enemyY[i] - playerY, 2))
        if dist1 < 27:

            game_over()



        # enemy movement
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        # putting restriction on movement of enemy with boundaries
        if enemyX[i] <= 0:
            enemyX_change[i] = 1

        if enemyX[i] >= 736:
            enemyX_change[i] = -1

        if enemyY[i] <= 0:
            enemyY[i] = 10
        if enemyY[i] >= 536:
            enemyY[i] = -10
        enemy(enemyX[i], enemyY[i], i)


    if sparkY <= 0:
        
        sparkY = playerY
        spark_state = "ready"

    if spark_state == "fire":
        fire_sound = mixer.Sound('fire.wav')
        fire_sound.play()
        fire_spark(sparkX,sparkY)
        sparkY -= sparkY_change

    # collision
    for i in range(num):
        collision = isShooted(enemyX[i], enemyY[i], sparkX, sparkY)
        if collision:
            collision_sound = mixer.Sound('collision.wav')
            collision_sound.play()
            sparkY = 480
            spark_state = "ready"
            score += 1
            print(score)
            enemyX[i]=random.randint(0,800)
            enemyY[i]=random.randint(50,150)

    player(playerX, playerY)
    score_board(textX,textY)
    pygame.display.update()
