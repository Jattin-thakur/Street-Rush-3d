import pygame
# -------------------------------
# Initialize Pygame
# -------------------------------
pygame.init()
# -------------------------------
# Create the game window
# -------------------------------
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Arrow Key Demo")
# -------------------------------
# Game control variable
# -------------------------------
game_exit = False
x=400
y=300
speed= 5
# -------------------------------
# Game Loop
# -------------------------------
while not game_exit:
    # Check for events
    for event in pygame.event.get():
        # Close the window
        if event.type == pygame.QUIT:
            game_exit = True
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y+=speed
            elif event.key == pygame.K_UP:
                y-=speed
            elif event.key == pygame.K_RIGHT:
                x-=speed
            elif event.key == pygame.K_LEFT:
                x+=speed
    # Fill the screen with red
    screen.fill((48, 204, 237))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 10, 20))
    
    # Update the display
    pygame.display.update()
# -------------------------------
# Quit Pygame
# -------------------------------
pygame.quit()
quit()