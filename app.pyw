import pygame
from pygame import mixer
from math import sqrt, pow
from random import randint
from button import Button

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

screen_w = screen.get_width()
screen_h = screen.get_height()
# background
background = pygame.image.load('img/background.png')
# Musics
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

bullet_sound = mixer.Sound('sounds/laser.wav')
explosion_sound = mixer.Sound('sounds/explosion.wav')

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

def setEnemies():
    for e in range(num_of_enemies):
        enemyImg.append(pygame.image.load('img/enemy.png'))
        enemyX.append(randint(0, 735))
        enemyY.append(randint(50, 150))
        enemyX_change.append(3)
        enemyY_change.append(40)

# Player 1
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 2
enemy_lock = False

setEnemies()

# Bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 6
bullet_state = 'ready'
# Score text
score_value = 0
font = pygame.font.Font('font.ttf', 32)
scoreX = 10
scoreY = 10
# Game over text
over_font = pygame.font.Font('font.ttf', 64)
# Enemies count text
enemy_textY = 550
enemy_textX = 10
# Restart button
res_btn_w = 210
res_btn_h = 65
res_btn_x = screen_w/2 - res_btn_w/2
res_btn_y = screen_h/2 - res_btn_h/2 + 70
rest_btn_text = 'RESTART'
rest_btn_color = (100,100,255)
restart_btn = Button(rest_btn_color, res_btn_x, res_btn_y, res_btn_w, res_btn_h, rest_btn_text)
# Mode text
mode_font = pygame.font.SysFont('comicsans', 32)
mode = 'stopping at the walls'
mode_textX = screen_w - len(mode) * 16
mode_textY = screen_h - 35

def show_mode(x, y):
    mode_text = mode_font.render('[B]Mode: ' + str(mode), True, (210, 255, 255))
    screen.blit(mode_text, (x, y))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (210, 255, 255))
    screen.blit(score, (x, y))

def show_enemies_count(x, y):
    enemy_count_text = font.render('Enemies Count: ' + str(num_of_enemies), True, (210, 255, 255))
    screen.blit(enemy_count_text, (x, y))

def game_over():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    mixer.music.stop()
    restart_btn.draw(screen, (0,0,0), (255,255,255))

def drawPlayer(x, y):
    screen.blit(playerImg, (x, y))

def drawEnemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))

def drawFire_Bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(x1, y1, x2, y2):
    distance = sqrt((pow(x1 - x2, 2)) + (pow(y1 - y2, 2)))
    if distance < 27:
        return True
    return False

def reset_game():
    screen.fill((0,0,0))
    global score_value, num_of_enemies
    score_value = 0
    num_of_enemies = 4
    setEnemies()
    mode = 'Stopping at the walls'
    for i in range(num_of_enemies):
        enemyY[i] = randint(50, 150)
    mixer.music.play()


# Game loop
while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.QUIT()

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 4.2
            # Fire bullet
            if not event.key == pygame.K_LEFT and not event.key == pygame.K_RIGHT and not event.key == pygame.K_b and bullet_state == 'ready':
                bullet_sound.play()
                bulletX = playerX
                drawFire_Bullet(bulletX, bulletY)
            if event.key == pygame.K_b and mode == 'crossing the wall':
                mode = 'stopping at the walls'
            elif event.key == pygame.K_b and mode == 'stopping at the walls':
                mode = 'crossing the wall'

        # Reset player movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change

    if mode == 'crossing the wall':
         ###### PRZECHODZENIE PRZEZ ŚCIANY
        if playerX > 787:
            playerX = -51
        elif playerX <= -51:
            playerX = 787
    else:
         ###### ZATRZYMYWANIE PRZY SCIANACH
        if playerX >= 736:
            playerX = 736
        elif playerX <= 0:
            playerX = 0


    if score_value % 10 == 0 and not enemy_lock:
        enemy_lock = True
        num_of_enemies += 2
        setEnemies()

    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            
        # Enemy movement
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_lock = False
            enemyX[i] = randint(0, 736)
            enemyY[i] = randint(50, 150)

        drawEnemy(i, enemyX[i], enemyY[i])


    # Bullet movement
    if bulletY <= -52:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        drawFire_Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if restart_btn.isHover(pos):
        restart_btn.color = (0,0,255)
    else:
        restart_btn.color = rest_btn_color

    if event.type == pygame.MOUSEBUTTONDOWN:
        if restart_btn.isHover(pos):
            reset_game()

    drawPlayer(playerX, playerY)
    show_score(scoreX, scoreY)
    show_enemies_count(enemy_textX, enemy_textY)
    show_mode(mode_textX, mode_textY)
    pygame.display.update()