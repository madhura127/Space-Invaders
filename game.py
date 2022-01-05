import pygame
import math
import random
from pygame import mixer

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True,(255, 255, 255))      #show score of game
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True,(255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))                        #drawing image of player on the window


def enemy(x, y, i):                                       #Blit funtion is used to draw player image on screen
    screen.blit(enemyImg[i], (x, y))                      #drawing image of enemy on the window

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"                                 #Bullet is in motion
    screen.blit(bulletImg, (x + 16, y + 10))              #Bullet will appear at the center of the spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):        #using distance between 2 points and midpoint formula
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

pygame.init()

screen = pygame.display.set_mode((800, 600))                   #create the screen,mode(width, height)

background = pygame.image.load("Background.png")               # Set Background image

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")                  #Set Title and Icon image
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)
 
playerImg = pygame.image.load("rocket.png")                   # Player
playerX = 370
playerY = 480
playerX_change = 0
                                                           
enemyImg = []                                                # Enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))                    #Method inside random package to choose a random integer between 2 values
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")                 # Bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"                                      #you can't see the bullet on the screen .Bullet is set to ready
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)               #Adding font and size of the font
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)        #Game Over Text



running = True                                              #Game Loop
while running:
    screen.fill((0, 0, 0))                               #color of background
    screen.blit(background, (0, 0))                      #draw background on screen

    for event in pygame.event.get():                     #Till quit button is not pressed on window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:                 #When key is pressed
            if event.key == pygame.K_LEFT:                 #if it is left key then  .Left arrow is pressed
                playerX_change = -5                           #decrease x axis distance by 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5                             #else if right key then increase distance by 5
            if event.key == pygame.K_SPACE:                     #when space bar is pressed
                if bullet_state =="ready":                        #check state of bullet
                    bullet_Sound = mixer.Sound('laser.wav')           #background sound is given
                    bullet_Sound.play()                              
                    bulletX = playerX                                  #position of bullet will be initially same as that of spacecraft
                    fire_bullet(bulletX, bulletY)                      #then call function to fire bullet

        if event.type == pygame.KEYUP:                                   #key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  #if key is released then spacecraft should not move
                playerX_change = 0

    playerX += playerX_change                          
    if playerX <= 0:                                       #Creating a boundary for spacship
        playerX = 0                                         #if spaceship goes beyond x axis on left side then it should again comeback to 0 th 
    elif playerX >= 736:                                     #position
        playerX = 736

    for i in range (num_of_enemies):                       #creating game over condition

        if enemyY[i] > 440:                                
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]                      #enenmy movement
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)              #collision of bullet and enemy
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')                           #give sound when collision happens
            explosion_Sound.play()                                                   
            bulletY = 480                                                             
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:                                      #bullet movement
        bulletY = 480
        bullet_state = "ready"

    if bullet_state =="fire":                           #if bullet state is fire then call fire_bullet function and change it's Y coordinates 
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)                          #function call
    show_score(textX, textY)
    pygame.display.update()