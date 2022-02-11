from os import pipe
from typing import Tuple
import pygame,sys,random

#function
def velai_floor():
    DISPLAYSURF.blit(floor,(floor_x_pos,632))
    DISPLAYSURF.blit(floor,(floor_x_pos+432,632))
def createpipe():
    random_pipepos=random.choice(pipe_height) 
    bottompipe=pipe_surface.get_rect(midtop=(1000,random_pipepos))
    toppipe=pipe_surface.get_rect(midtop=(1000,random_pipepos-850))
    return bottompipe,toppipe 
def movepipe(pipes):
    for pipe in pipes:
        pipe.centerx-=1
    return pipes
def drawpipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=600:
            DISPLAYSURF.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            DISPLAYSURF.blit(flip_pipe,pipe)
def checkvacham(pipes):
    for pipe in pipes:
        if bird_pos.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_pos.top<=-75 or bird_pos.bottom>=650:
            return False
    return True
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_pos=new_bird.get_rect(center=(100,bird_pos.centery))
    return new_bird,new_bird_pos
def score_display(game_state):
    if game_state=='main game':
        score_show=game_font.render(str(int(game_score)),True,(255,255,255)) 
        score_rect=score_show.get_rect(center=(1024/2,100))
        DISPLAYSURF.blit(score_show,score_rect)
    if game_state=='game over':
        score_show=game_font.render(f'Score:{int(game_score)}',True,(255,255,255))
        score_rect=score_show.get_rect(center=(1024/2,100))
        DISPLAYSURF.blit(score_show,score_rect)
        
        high_score_show=game_font.render(f'High Score:{int(high_score)}',True,(255,255,255))
        high_score_rect=high_score_show.get_rect(center=(1024/2,610))
        DISPLAYSURF.blit(high_score_show,high_score_rect)
def update_highscore(game_score,high_score):
    if game_score>high_score:
        high_score=game_score
    return high_score

from pygame.locals import*

#khoitao
pygame.mixer.pre_init()
pygame.init()
DISPLAYSURF=pygame.display.set_mode((1024,768))
pygame.display.set_caption('Flappy Bird By Quan Khu 2')
clock = pygame.time.Clock()
game_font=pygame.font.Font('E:/Project/Python/FlappyBird/04B_19.TTF',40)
#background
bg_surface=pygame.image.load('E:/Project/Python/FlappyBird/assets/background-day.png').convert()
bg_surface=pygame.transform.scale2x(bg_surface) 
bg_posx=0;
#sàn
floor=pygame.image.load('E:/Project/Python/FlappyBird/assets/base.png').convert()
floor=pygame.transform.scale2x(floor)
floor_x_pos=0
#conchim
bird_down=pygame.transform.scale2x(pygame.image.load('E:/Project/Python/FlappyBird/assets/redbird-downflap.png').convert_alpha())
bird_up=pygame.transform.scale2x(pygame.image.load('E:/Project/Python/FlappyBird/assets/redbird-upflap.png').convert_alpha())
bird_mid=pygame.transform.scale2x(pygame.image.load('E:/Project/Python/FlappyBird/assets/redbird-midflap.png').convert_alpha())
#bird=pygame.image.load('E:/Project/Python/FlappyBird/assets/redbird-midflap.png').convert_alpha()
#bird=pygame.transform.scale2x(bird)
bird_list=[bird_up,bird_mid,bird_up]
bird_index=0
bird=bird_list[bird_index]
bird_pos=bird.get_rect(center=(100,300))
#trongluc+hethong
gravity=0.25
bird_movement=0
game_active=True
game_score=0
high_score=0
#taoong
pipe_surface=pygame.image.load('E:/Project/Python/FlappyBird/assets/pipe-green.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#timer
timespawn=4000
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe,timespawn)
pipe_height=[200,300,400]
#timer bird
bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
#sound
flap_sound=pygame.mixer.Sound('E:/Project/Python/FlappyBird/audio/wing.wav')
hit_sound=pygame.mixer.Sound('E:/Project/Python/FlappyBird/audio/hit.wav')
score_sound=pygame.mixer.Sound('E:/Project/Python/FlappyBird/audio/point.wav')
score_countdown=100
#manhinhketthuc
game_over_surface=pygame.image.load('E:/Project/Python/FlappyBird/assets/message.png').convert_alpha()
game_over_rect=game_over_surface.get_rect(center=(1024/2,384))
#gameevent
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_movement=-6  
                flap_sound.play()
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_pos.center=(100,300)
                bird_movement=0
                game_score=0
        if event.type==spawnpipe:
            pipe_list.extend(createpipe())
        if event.type==bird_flap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,bird_pos=bird_animation()
    DISPLAYSURF.blit(bg_surface,(bg_posx,0))
    bg_posx-=0.5
    if bg_posx<-1534*2:
        bg_posx=0
    if game_active==True:
        #chim
        rotated_bird=rotate_bird(bird)
        bird_movement+=gravity
        bird_pos.centery+=bird_movement
        DISPLAYSURF.blit(rotated_bird,bird_pos)
        game_active=checkvacham(pipe_list)
        #ống
        pipe_list=movepipe(pipe_list)
        drawpipe(pipe_list)
        #hiendiem
        score_countdown-=1
        if score_countdown==0:
            score_sound.play()
            score_countdown=100
        game_score+=0.01
        if game_score%100==0:
            timespawn-=100
        score_display('main game')
    else:
        high_score=update_highscore(game_score,high_score)
        score_display('game over')
        DISPLAYSURF.blit(game_over_surface,game_over_rect)
    #sàn
    floor_x_pos-=1
    velai_floor()
    if floor_x_pos<=-432:
        floor_x_pos=0
    pygame.display.update()
    clock.tick(120)
    