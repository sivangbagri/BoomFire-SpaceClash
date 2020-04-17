"""
Author:Shivang
Started on: 18/2/20
Ended on: 22/2/20

"""

import pygame
import math
import random

pygame.init()
FPS=300
fpsClock=pygame.time.Clock()
screen = pygame.display.set_mode((800,500))




print("\nMy first pygame Boom fire\nDeveloper-sivangbagri@gmail.com\n ")


#title and icon
pygame.display.set_caption("Boom Fire")
icon = pygame.image.load("first_assests/space.png")
pygame.display.set_icon(icon)

# background
bg=pygame.image.load("first_assests/bg.jpg")

# player sprite
playerim=pygame.image.load("first_assests/rocket.png")
playerX=360
playerY=436
playerX_change=0
playerY_change=0

pygame.mixer.music.load("first_assests/music.mp3")
pygame.mixer.music.play(-1)

# enemy sprite
enemyim=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemies=7
for i in range (enemies):  # for multiple enemies

    enemyim.append(pygame.image.load("first_assests/monster.png"))
    enemyX.append(random.randint(0,739))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(random.randint(1,3))
    enemyY_change.append(40)

# bullet sprite
bulletim=pygame.image.load("first_assests/bullets.png")
bulletX=0
bulletY=436
bulletX_change=0
bulletY_change=15


bullet_state="ready"    # bullet state before firing & is not visible

# score
font=pygame.font.Font('first_assests/BRLNSR.ttf',25)
textX=10
textY=10
score_value=0
font2 = pygame.font.Font('first_assests/BRLNSR.ttf', 35)
font3=pygame.font.Font('first_assests/BRLNSR.ttf',25)
def game_txt():
    """ Displayed when game overs"""
    gameover=font2.render("GAME OVER",True,(255,255,255))
    by = font3.render('CREATED BY SHIVANG', True, (255, 255, 255))
    screen.blit(gameover,(350,200))
    screen.blit(by,(0,470))


def show_score(x,y):
    score=font.render('Score = '+str(score_value),True,(0,255,0))
    screen.blit(score,(x,y))


def player(x,y):
    screen.blit(playerim,(x,y))

def enemy(x,y,i):
    screen.blit(enemyim[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletim ,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    """ collision between bullet and enemy"""
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#game loop
run= True
while run:

    screen.fill((0, 0, 55))
    screen.blit(bg,(0,0))
    #screen.blit(text, textrect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False

    #movement
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_LEFT:
                playerX_change=-3
            if event.key==pygame.K_RIGHT:
                playerX_change=+3
            if event.key==pygame.K_SPACE:
                bulletX=playerX
                fire_bullet(bulletX,bulletY)


        if event.type==pygame.KEYUP:
            playerX_change=0
            playerY_change=0

    playerX=playerX+playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=740:
        playerX=740

    for i in range(enemies):
        if enemyY[i] > 380:
            for j in range(enemies):
                enemyY[j] = 4000
            game_txt()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # collison
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            sound = pygame.mixer.Sound('first_assests/rifle.wav')
            sound.play()

            bulletY = 436
            bullet_state = "ready"
            score_value+=1

            enemyX[i] = random.randint(0, 739)      # spawning new enemies
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)





# bullet movement

    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


# playerY=playerY+playerY_change

    player(playerX,playerY)
    show_score(textX,textY)



    pygame.display.update()
    fpsClock.tick(FPS)
