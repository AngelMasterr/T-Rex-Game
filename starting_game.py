import pygame
import random
import time

pygame.init()
win_width = 600
win_height = 150
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino Game")


dino_img = pygame.image.load('assets/Dino/DinoStartM.png')
cactus_img = pygame.image.load('assets/Cactus/LargeCactus1M.png')
bird_img = pygame.image.load('assets/Bird/Bird1M.png')

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.jump_vel = 8
        self.gravity = 0.5
        self.is_jump = False
        self.img = dino_img

    def jump(self):
        if not self.is_jump:
            self.is_jump = True

    def move(self):
        if self.is_jump:
            self.vel += self.gravity
            self.y += self.vel
            if self.y >= 100:
                self.y = 100
                self.vel = 0
                self.is_jump = False

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = 110
        self.vel = 5
        self.img = cactus_img

    def move(self):
        self.x -= self.vel

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Bird:
    def __init__(self, x):
        self.x = x
        self.y = random.choice([75, 90, 105])
        self.vel = 5
        self.img = bird_img

    def move(self):
        self.x -= self.vel

    def draw(self):
        win.blit(self.img, (self.x, self.y))

def game():
    dino = Dinosaur(50, 100)
    obstacles = []
    score = 0
   
