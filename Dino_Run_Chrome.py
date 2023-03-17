import pygame
import sys
import random

pygame.init()
widht_x = 1280
hight_y = 720
screen = pygame.display.set_mode((widht_x, hight_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)

# Classes

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino/DinoRun1a.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino/DinoRun2a.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/Dino/DinoDuck1a.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/Dino/DinoDuck2a.png"), (110, 60)))
        
        self.jumping_sprites = pygame.transform.scale(pygame.image.load("assets/Dino/DinoJumpa.png"), (80, 100))
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 0.3
        self.ducking = False
        self.jumping = False
        self.on_ground = True
        self.jump_force = -12
        self.vel_y = 0

    def jump(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            jump_sfx.play()
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jumping = True
        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            # check for collision with ground
            if self.rect.bottom >= 410:
                self.rect.bottom = 410
                self.on_ground = True
                self.jumping = False
                self.vel_y = 0                                                       

    def duck(self):
        self.ducking = True
        self.rect.centery = 400

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360
        
    def update(self):        
        self.jump() 
        self.animate()         
    
    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        elif self.jumping:
            self.image = self.jumping_sprites
        else:
            self.image = self.running_sprites[int(self.current_image)]

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = [pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus1a.png"),(70, 100)),
                        pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus2a.png"),(110, 100)),
                        pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus3a.png"),(150, 100)),
                        pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus4a.png"),(60, 80)),
                        pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus5a.png"),(90, 80)),
                        pygame.transform.scale(pygame.image.load("assets/Cactus/Cactus6a.png"),(120, 80))]
        """for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/Cactus/Cactus{i}a.png"), (90, 100))
            self.sprites.append(current_sprite)"""
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()#center=(self.x_pos, self.y_pos))
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos - self.rect.height

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect()#center=(self.x_pos, self.y_pos)
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos - self.rect.height
        #self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([270, 310, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird1a.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird2a.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

# Variables
game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Surfaces
ground = pygame.image.load("assets/Other/Track.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
cloud = pygame.image.load("assets/Other/Cloud.png")
cloud = pygame.transform.scale(cloud, (160, 160))

# Groups
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Functions
def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #or event.key == pygame.K_UP:
                #dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    # Ground
    screen.fill("white")
    ground_x -= game_speed
    screen.blit(ground, (ground_x, 380))
    screen.blit(ground, (ground_x + 1280, 380))
    if ground_x <= -1280:
        ground_x = 0
    
    # Collisions
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    # Play Game
    if not game_over:
        game_speed += 0.0015
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 400)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update()
        cloud_group.draw(screen)       

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)
        

    clock.tick(120)
    pygame.display.update()