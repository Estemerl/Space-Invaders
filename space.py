import random
from re import I
import pygame
import math
from pygame import mixer

pygame.init()
screen_width=800
screen_height=600

size=(screen_width, screen_height)

screen=pygame.display.set_mode(size)

background=pygame.image.load("espacio.jpg")


mixer.music.load("fondo.wav")
mixer.music.play(-1)

bullet_sound=mixer.Sound("disparo.wav")
bullet_sound.set_volume(0.5)


explosion_sound=mixer.Sound("colicion.wav")
explosion_sound2=mixer.Sound("colicion.wav")
explosion_sound3=mixer.Sound("colicion.wav")


pygame.display.set_caption("Space Invader")

icon=pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

go_font=pygame.font.Font("score.otf", 64)
go_x=200
go_y=250

player_x=350
player_y=500
player_img=pygame.image.load("space.png")
player_x_change=0

enemy_img=[]
enemy_x=[]
enemy_y=[]
enemy_x_change=[]
enemy_y_change=[]

numer_enemies=8
for item in range(numer_enemies):
    hola = ["alien.png", "monster.png", "ufo.png"]
    enemy_img.append(pygame.image.load(random.choice(hola)))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(1)
    enemy_y_change.append(50)

bullet_img = pygame.image.load("bala.png")
bullet_x = 0 
bullet_y = 480
bullet_y_change = 2
bullet_state="ready"

score = 0
score_font=pygame.font.Font("score.otf", 40)

text_X=10
text_y=10
def show_text(x,y):
    score_text=score_font.render("Score :"+str(score), True, (246, 178, 0,))
    screen.blit(score_text, (x,y))

def enemy(x,y):
   screen.blit(enemy_img[item], (x,y))

def fire(x,y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bullet_img, (x+16, y+10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance=math.sqrt((enemy_x-bullet_x)**2+(enemy_y-bullet_y)**2)

    if distance<27:
        return True
    else:
        return False


def player(x,y):
    screen.blit(player_img, (x,y))


def game_over(x,y):
    go_text= go_font.render("GAME OVER", True, (255, 255, 255)) 
    screen.blit(go_text, (x,y))

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_z:
                player_x_change=-1
            if event.key==pygame.K_x:
                player_x_change=1
            
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound("disparo.wav")
                    bullet_sound.play()
                    bullet_x=player_x
                fire(player_x, bullet_y)
        
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_z or event.key==pygame.K_x:
                player_x_change=0

    rgb=(15,98,250)
    screen.fill(rgb)
    screen.blit(background, (0,0))    
    
    player_x +=player_x_change
    
    if player_x<=0:
        player_x=0
    elif player_x>=767:
        player_x=767
    
    for item in range(numer_enemies):
    
        enemy_x[item] += enemy_x_change[item]

        if enemy_y[item]>440:
            for j in range(numer_enemies):
                enemy_y[j]=2000
            game_over(go_x, go_y)
            break
        if enemy_x[item] <= 0:
            enemy_x_change[item]=0.5
            enemy_y[item]+=enemy_y_change[item]
        
        elif enemy_x[item]>=767:
            enemy_x_change[item]=-0.5
            enemy_y[item]+=enemy_y_change[item]

        collision=is_collision(enemy_x[item],enemy_y[item],bullet_x,bullet_y) 
            
        if collision:
            explosion_sound.play()
            bullet_y=400
            bullet_state="ready"
            score+=1
            enemy_x[item]=random.randint(0, 755)
            enemy_y[item]=random.randint(50, 150)

        enemy(enemy_x[item],enemy_y[item])



    if bullet_y<=0:
        bullet_y=480
        bullet_state="ready"

    if bullet_state == "fire":
        fire(bullet_x, bullet_y)
        bullet_y-=bullet_y_change   

    player(player_x, player_y)

    show_text(text_X, text_y)

    pygame.display.update()
    
    

    
