import pygame
from sys import exit


# Medidas da tela
largura  = 800
altura = 400

def display_score(posicao_score):
    current_time = pygame.time.get_ticks() - start_time
    score_atual = int(current_time/500)
    
    score_surface = font.render(f'{score_atual}', False, (64,64,64)) # Renderiza a fonte (texto, arredondar as bordas, cor)
    # elif state == 2:
    #     score_surface = font.render(f'{score_final}', False, (64,64,64))
    # score_rect = score_surface.get_rect(center = (400,50))
    score_rect = score_surface.get_rect(center = posicao_score)
    # Fundo para o score
    pygame.draw.rect(screen,(192,232,236),score_rect)
    pygame.draw.rect(screen,(192,232,236),score_rect,10)
    screen.blit(score_surface,score_rect)

    
    

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

pygame.init() #Inicializar o pygame
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Alien Run')
clock = pygame.time.Clock() # Clock para definir FPS
font = pygame.font.Font("font/Pixeltype.ttf",50) # Escolha da fonte para os textos (font_type,font_size)
game_state = 0 # Define o estado do jogo: 0 = Tela inicial, 1 = in game, 2 = Game Over
start_time = 0

sky_surface = pygame.image.load("graphics/Sky.png").convert() # .convert() ajuda o pygame a trabalhar melhor com as imagens
ground_surface = pygame.image.load("graphics/ground.png").convert()

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # _alpha é utilizado para manter os valores alpha originais
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300)) # Cria um retângulo em volta da imagem e define o ponto de origem
player_gravity = 0

while True: # Tudo que é mostrado e atualizado, fica dentro dessa condição
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Finaliza o .init()
            exit() # Para finalizar sem erro

        # if event.type == pygame.MOUSEBUTTONDOWN: # Mecânica de pulo, mas com o mouse 
        #     if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
        #         player_gravity = -20

        if game_state == 0:
            # Intro screen
            display_title()
        if game_state == 1:
            if event.type == pygame.KEYDOWN: # Verifica se um botão do teclado foi pressionado
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # Verifica se o botão pressionado foi a barra de espaço e se o player está no chão 
                    player_gravity = -20
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                snail_rect.left = 820
                start_time = pygame.time.get_ticks()
                game_state = 1

      

    if game_state == 1: # Estado "jogavel"
        screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
        screen.blit(ground_surface,(0,300))

        display_score((400,50))
       
        # player_rect.left += 1
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 820

        # Snail   
        screen.blit(snail_surface,snail_rect)
         
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface,player_rect)

        # Colisão player snail
        if snail_rect.colliderect(player_rect):
            game_state = 2
    elif game_state == 2: # "Game Over"
        game_over()
        
        

    pygame.display.update()
    clock.tick(60) # FPS
    
    