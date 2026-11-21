import pygame
status = pygame.init()
print(status)
dis =pygame.display.set_mode((800,300))
pygame.display.set_caption("Py Games")

exit_game=False #to make the game run until the user wants to exit
game_over=False
while not exit_game:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit_game=True
        
quit()