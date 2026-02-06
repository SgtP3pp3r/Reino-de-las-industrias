import pygame
import sys

pygame.init()

# ----------------- CONFIG -----------------
TILE_SIZE = 32
MAP_WIDTH = 25
MAP_HEIGHT = 18
WIDTH = MAP_WIDTH * TILE_SIZE
HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST ::: Zelda-like Fase 2")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (50, 180, 50)

# ----------------- MAPA POR TILES -----------------
# 0 = suelo
# 1 = pared
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# ----------------- GENERAR PAREDES -----------------
walls = []
for y, row in enumerate(MAP):
    for x, tile in enumerate(row):
        if tile == 1:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            walls.append(rect)

# ----------------- CLASE JUGADOR -----------------
class Player:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y
        self.speed = 4

        self.image = pygame.Surface((28, 28))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(self.world_x, self.world_y))

    def handle_input(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed

        self.move(dx, dy)

    def move(self, dx, dy):
        # --- EJE X ---
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right

        # --- EJE Y ---
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

        self.world_x = self.rect.centerx
        self.world_y = self.rect.centery

    def update(self):
        self.handle_input()

    def draw(self, surface, camera_x, camera_y):
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        surface.blit(self.image, (screen_x, screen_y))


# ----------------- CÁMARA -----------------
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def update(self, target):
        self.x = target.rect.centerx - WIDTH // 2
        self.y = target.rect.centery - HEIGHT // 2

        self.x = max(0, min(self.x, MAP_WIDTH * TILE_SIZE - WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT * TILE_SIZE - HEIGHT))


# ----------------- INIT -----------------
clock = pygame.time.Clock()
player = Player(100, 100)
camera = Camera(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)

# ----------------- LOOP -----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    camera.update(player)

    SCREEN.fill(GRAY)

    # --- DIBUJAR MAPA ---
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE
            screen_x = world_x - camera.x
            screen_y = world_y - camera.y

            if tile == 0:
                pygame.draw.rect(SCREEN, GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            elif tile == 1:
                pygame.draw.rect(SCREEN, (80, 80, 80), (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

    player.draw(SCREEN, camera.x, camera.y)

    pygame.display.update()

pygame.quit()
sys.exit()
