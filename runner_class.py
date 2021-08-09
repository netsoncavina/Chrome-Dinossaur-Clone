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
text_surface = font.render('My game', False, 'black') # Renderiza a fonte (texto, arredondar as bordas, cor)

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # _alpha é utilizado para manter os valores alpha originais
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300)) # Cria um retângulo em volta da imagem e define o ponto de origem


while True: # Tudo que é mostrado e atualizado, fica dentro dessa condição
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Finaliza o .init()
            exit() # Para finalizar sem erro
    screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))
    player_rect.left += 1
    snail_rect.x -= 3
    if snail_rect.right <= 0:
        snail_rect.left = 820
        
    screen.blit(snail_surface,snail_rect)
    screen.blit(player_surface,player_rect)

    pygame.display.update()
    clock.tick(60) # FPS
    
    