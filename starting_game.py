import pygame
import random
import time

pygame.init()
win_width = 1000
win_height = 300
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino Game")


dino_img = pygame.image.load('assets/Dino/DinoStartM.png')
dino_img = pygame.transform.scale(dino_img, (80, 80))
cactus_img = pygame.image.load('assets/Cactus/LargeCactus1M.png')
cactus_img = pygame.transform.scale(cactus_img, (80, 80))
bird_img = pygame.image.load('assets/Bird/Bird1M.png')
bird_img = pygame.transform.scale(bird_img, (80, 80))

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.jump_vel = -12
        self.gravity = 0.5
        self.is_jump = False
        self.img = dino_img

    def jump(self):
        if not self.is_jump:
            self.is_jump = True

    def move(self):
        if self.is_jump:            
            self.vel += self.gravity
            self.y += self.jump_vel + self.vel
            if self.y >= 150:
                self.y = 150
                self.vel = 0
                self.is_jump = False

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = 50
        self.vel = 1
        self.img = cactus_img

    def move(self):
        self.x -= self.vel

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Bird:
    def __init__(self, x):
        self.x = x
        self.y = random.choice([75, 90, 105])
        self.vel = 1
        self.img = bird_img

    def move(self):
        self.x -= self.vel

    def draw(self):
        win.blit(self.img, (self.x, self.y))

def game():
    dino = Dinosaur(50, 150)
    obstacles = []
    score = 0

    while True:
        # Manejar eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # Actualizar posición de personajes
        dino.move()
        for obstacle in obstacles:
            obstacle.move()

        # Crear nuevos obstáculos
        if len(obstacles) < 1:
            obstacle_type = random.choice(['cactus', 'bird'])
            if obstacle_type == 'cactus':
                obstacles.append(Cactus(600))
            elif obstacle_type == 'bird':
                obstacles.append(Bird(600))

        # Eliminar obstáculos antiguos
        if len(obstacles) > 0 and obstacles[0].x < -50:
            obstacles.pop(0)

        # Detectar colisiones
        for obstacle in obstacles:
            if (obstacle.x <= dino.x + 50 <= obstacle.x + 25 or
                obstacle.x <= dino.x + 95 <= obstacle.x + 25) and dino.y >= 100:
                pygame.quit()
                quit()

        # Aumentar puntuación
        score += 1

        # Dibujar personajes
        win.fill((255, 255, 255))
        dino.draw()
        for obstacle in obstacles:
            obstacle.draw()
        pygame.display.update()

        # Pausar juego
        time.sleep(0.02)

    pygame.quit()
    quit()
game()
