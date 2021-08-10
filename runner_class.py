import pygame
from sys import exit


# Medidas da tela
largura  = 800
altura = 400

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f'{int(current_time/500)}', False, (64,64,64)) # Renderiza a fonte (texto, arredondar as bordas, cor)
    score_rect = score_surface.get_rect(center = (400,50))
    # Fundo para o score
    pygame.draw.rect(screen,(192,232,236),score_rect)
    pygame.draw.rect(screen,(192,232,236),score_rect,10)
    screen.blit(score_surface,score_rect)



pygame.init() #Inicializar o pygame
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() # Clock para definir FPS
font = pygame.font.Font("font/Pixeltype.ttf",50) # Escolha da fonte para os textos (font_type,font_size)
game_active = True # Define o estado do jogo
start_time = 0


# test_surface = pygame.Surface((100,200)) #Criação da nova superficie
# test_surface.fill('red') # Prenche a superficie com uma cor

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
        if game_active:
            if event.type == pygame.KEYDOWN: # Verifica se um botão do teclado foi pressionado
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # Verifica se o botão pressionado foi a barra de espaço e se o player está no chão 
                    player_gravity = -20
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                snail_rect.left = 820
                start_time = pygame.time.get_ticks()
                game_active = True

      

    if game_active: # Estado "jogavel"
        screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
        screen.blit(ground_surface,(0,300))

        display_score()
       
        
        
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
            game_active = False
    else: # "Game Over"
        font_game_over = pygame.font.Font("font/Pixeltype.ttf",90) # Escolha da fonte para os textos (font_type,font_size)
        game_over_surface = font.render('GAME OVER', False, "RED") # Renderiza a fonte (texto, arredondar as bordas, cor)
        game_over_rect = game_over_surface.get_rect(center = (400,200))
        screen.blit(game_over_surface,game_over_rect)
        
        
        

    pygame.display.update()
    clock.tick(60) # FPS
    
    