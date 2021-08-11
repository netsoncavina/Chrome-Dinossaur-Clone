import pygame
import pickle
import random 
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        self.player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [self.player_walk_1,self.player_walk_2]
        self.player_index = 0  
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()      
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300 
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:  
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # _alpha é utilizado para manter os valores alpha originais
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def display_title():
    player_stand = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,2)
    player_stand_rect = player_stand.get_rect(center = (400,200))
    title_surface = font.render("Alien Run", False, (111,196,169)) 
    title_rect = title_surface.get_rect(center = (400,50))
    screen.fill((94,129,162))
    screen.blit(player_stand,player_stand_rect)
    screen.blit(title_surface,title_rect)
    start_surface = font.render("Pressione o mouse",False,(111,196,169))
    start_rect = start_surface.get_rect(center = (400,350))
    screen.blit(start_surface,start_rect)

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_atual = int(current_time/500)
    score_surface = font.render(f'{score_atual}', False, (64,64,64)) # Renderiza a fonte (texto, arredondar as bordas, cor)
    score_rect = score_surface.get_rect(center = (400,50))
    # Fundo para o score
    pygame.draw.rect(screen,(192,232,236),score_rect)
    pygame.draw.rect(screen,(192,232,236),score_rect,10)
    screen.blit(score_surface,score_rect)
    return score_atual

def high_score_update(score_atual, high_score):
    if score_atual > high_score:
            high_score = score_atual
            # Saving score
            pickle.dump(high_score, open("high_score.dat", "wb"))

def high_score_show():
    high_score_data = pickle.load(open("high_score.dat", "rb"))
    high_score_surface = font.render(f'High Score: {high_score_data}', True, "Red")
    high_score_rect = high_score_surface.get_rect(center = (130,120))
    screen.blit(high_score_surface,high_score_rect)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return True
    else: return False

def game_over():
    screen.fill("Black")
    player_stand = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,180,2)
    player_stand_rect = player_stand.get_rect(center = (400,200))
    font_game_over = pygame.font.Font("font/Pixeltype.ttf",90) # Escolha da fonte para os textos (font_type,font_size)
    game_over_surface = font_game_over.render('GAME OVER', False, "RED") # Renderiza a fonte (texto, arredondar as bordas, cor)
    game_over_rect = game_over_surface.get_rect(center = (400,50))
    continue_surface = font.render("Pressione o mouse para continuar",False,"red")
    continue_rect = continue_surface.get_rect(center = (400,350))
    screen.blit(continue_surface,continue_rect)
    screen.blit(player_stand,player_stand_rect)
    screen.blit(game_over_surface,game_over_rect)

pygame.init() #Inicializar o pygame

# Medidas da tela
largura  = 800
altura = 400
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Alien Run')
clock = pygame.time.Clock() # Clock para definir FPS
font = pygame.font.Font("font/Pixeltype.ttf",50) # Escolha da fonte para os textos (font_type,font_size)
game_state = 0 # Define o estado do jogo: 0 = Tela inicial, 1 = in game, 2 = Game Over
start_time = 0
score = 0
high_score = 0

# Music and sounds
bg_music =  pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.0)
bg_music.play(loops = -1)
start_sound = pygame.mixer.Sound("audio/start.wav")
start_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound("audio/death.wav")
game_over_sound = pygame.mixer.Sound("audio/game_over.wav")

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player()) 

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("graphics/Sky.png").convert() # .convert() ajuda o pygame a trabalhar melhor com as imagens
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True: # Tudo que é mostrado e atualizado, fica dentro dessa condição
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Finaliza o .init()
            exit() # Para finalizar sem erro

        if game_state == 0:
            # Intro screen
            display_title()

        if game_state == 1:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(["fly","snail","snail","snail"])))
           
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_sound.play()
                obstacle_rect_list = []
                start_time = pygame.time.get_ticks()
                game_state = 1

    if game_state == 1: # Estado "jogavel"
        bg_music.set_volume(0.5)
        screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
        screen.blit(ground_surface,(0,300))

        score = display_score()
       
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Colisão 
        if collision_sprite():
            bg_music.set_volume(0.0)
            death_sound.play()
            game_over_sound.play()
            game_state = 2

    elif game_state == 2: # "Game Over"
        game_over()
        high_score = pickle.load(open("high_score.dat", "rb"))
        high_score_update(score,high_score)
        high_score_show()
        score_surface = font.render(f'Score: {score}', True, "Red") # Renderiza a fonte (texto, arredondar as bordas, cor)
        score_rect = score_surface.get_rect(center = (100,200))
        screen.blit(score_surface,score_rect)
        
    pygame.display.update()
    clock.tick(60) # FPS