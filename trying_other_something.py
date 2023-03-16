import pygame
import random
import time

pygame.init()
win_width = 1000
win_height = 300
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino Game")


dino_img = pygame.image.load('assets/Dino/DinoStartM.png')
cactus_img = pygame.image.load('assets/Cactus/LargeCactus1M.png')
bird_img = pygame.image.load('assets/Bird/Bird1M.png')
#bird_img = pygame.transform.scale(bird_img, (80, 80))
