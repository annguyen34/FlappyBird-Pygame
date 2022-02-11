import pygame
import button

#create display window
SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1024

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird By Quan Khu 2')

#load button images
start_img = pygame.image.load('E:/Project/Python/FlappyBird/assets/start_btn.png').convert_alpha()
exit_img = pygame.image.load('E:/Project/Python/FlappyBird/assets/exit_btn.png').convert_alpha()

#create button instances
start_button = button.Button(200, 768/2-20, start_img, 0.8)
exit_button = button.Button(630, 768/2-20, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		import game    # Chạy game 
	if exit_button.draw(screen):
		pygame.quit()
	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()