import pygame
import pickle
from random import randint
from sys import exit

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

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # Deleta os obstaculos que sairem da tela

        return obstacle_list
    else: return []

def collision(player,obstacle):
    for obstacle in obstacle_rect_list:
        if obstacle.colliderect(player):
            return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

def snail_animation():
    global snail_surface, snail_index

    snail_index += 0.05
    if snail_index >= len(snail_walk):
        snail_index = 0
    snail_surface = snail_walk[int(snail_index)]

def fly_animation():
    global fly_surface, fly_index

    fly_index += 0.05
    if fly_index >= len(fly_fly):
        fly_index = 0
    fly_surface = fly_fly[int(fly_index)]


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

sky_surface = pygame.image.load("graphics/Sky.png").convert() # .convert() ajuda o pygame a trabalhar melhor com as imagens
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Obstacles 
snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # _alpha é utilizado para manter os valores alpha originais
snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_walk = [snail_1,snail_2]
snail_index = 0
snail_surface = snail_walk[snail_index]

fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_fly = [fly_1,fly_2]
fly_index = 0
fly_surface = fly_fly[fly_index]



obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300)) # Cria um retângulo em volta da imagem e define o ponto de origem
player_gravity = 0

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
            if event.type == pygame.KEYDOWN: # Verifica se um botão do teclado foi pressionado
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # Verifica se o botão pressionado foi a barra de espaço e se o player está no chão 
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                obstacle_rect_list = []
                start_time = pygame.time.get_ticks()
                game_state = 1

    if game_state == 1: # Estado "jogavel"
        screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
        screen.blit(ground_surface,(0,300))

        score = display_score()
       
        # snail_rect.x -= 5
        # if snail_rect.right <= 0:
        #     snail_rect.left = 820
        # screen.blit(snail_surface,snail_rect)
         
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface,player_rect)

        # Obstacle movement
        snail_animation()
        fly_animation()
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Colisão 
        if collision(player_rect, obstacle_rect_list):
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
    
    