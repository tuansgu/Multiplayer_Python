import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stress Fight")
bg_image = pygame.image.load("assets/bggame.jpg")
screen.blit(bg_image, (0,0))