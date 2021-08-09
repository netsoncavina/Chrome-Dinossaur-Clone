import pygame
from sys import exit


# Medidas da tela
largura  = 800
altura = 400

pygame.init() #Inicializar o pygame
screen = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() # Clock para definir FPS
test_font = pygame.font.Font("font/Pixeltype.ttf",50) # Escolha da fonte para os textos (font_type,font_size)

# test_surface = pygame.Surface((100,200)) #Criação da nova superficie
# test_surface.fill('red') # Prenche a superficie com uma cor

sky_surface = pygame.image.load("graphics/Sky.png")
ground_surface = pygame.image.load("graphics/ground.png")
text_surface = test_font.render('My game', False, 'black') # Renderiza a fonte (texto, arredondar as bordas, cor)


while True: # Tudo que é mostrado e atualizado, fica dentro dessa condição
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Finaliza o .init()
            exit() # Para finalizar sem erro
    screen.blit(sky_surface,(0,0)) # Coloca uma superficie sobre a outra (superficie,posição) 
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))
    pygame.display.update()
    clock.tick(60) # FPS
    
    