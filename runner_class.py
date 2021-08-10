import pygame
from sys import exit


# Medidas da tela
largura  = 800
altura = 400

pygame.init() #Inicializar o pygame
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() # Clock para definir FPS
font = pygame.font.Font("font/Pixeltype.ttf",50) # Escolha da fonte para os textos (font_type,font_size)

# test_surface = pygame.Surface((100,200)) #Criação da nova superficie
# test_surface.fill('red') # Prenche a superficie com uma cor

sky_surface = pygame.image.load("graphics/Sky.png").convert() # .convert() ajuda o pygame a trabalhar melhor com as imagens
ground_surface = pygame.image.load("graphics/ground.png").convert()

score_surface = font.render('My game', False, (64,64,64)) # Renderiza a fonte (texto, arredondar as bordas, cor)
score_rect = score_surface.get_rect(center = (400,50))

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

        if event.type == pygame.MOUSEBUTTONDOWN: # Mecânica de pulo, mas com o mouse 
            if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                player_gravity -= 5

        if event.type == pygame.KEYDOWN: # Verifica se um botão do teclado foi pressionado
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # Verifica se o botão pressionado foi a barra de espaço e se o player está no chão 
                player_gravity -= 5
        # if event.type == pygame.KEYUP: # Verifica se o botão não está mais sendo pressionado
        #     player_rect.bottom += 20
    screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
    screen.blit(ground_surface,(0,300))

    # Fundo para o score
    pygame.draw.rect(screen,(192,232,236),score_rect)
    pygame.draw.rect(screen,(192,232,236),score_rect,10)
    
    screen.blit(score_surface,score_rect)
    # player_rect.left += 1
    snail_rect.x -= 3
    if snail_rect.right <= 0:
        snail_rect.left = 820

    # Snail   
    screen.blit(snail_surface,snail_rect)
    
    
    # Player
    player_gravity += 0.05
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
    
    screen.blit(player_surface,player_rect)


    # if player_rect.colliderect(snail_rect):
    #     print("Colidiu")


    pygame.display.update()
    clock.tick(60) # FPS
    
    