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
pygame.display.set_caption("TEST ::::: Zelda-like Fase 3")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (50, 180, 50)

# ----------------- MAPA POR TILES -----------------
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

# ----------------- CARGA DE SPRITES -----------------
def load_animation(prefix, count):
    return [pygame.image.load(f"link/{prefix}_{i}.png").convert_alpha() for i in range(count)]

idle_front = pygame.image.load("link/idle_front.png").convert_alpha()
idle_back  = pygame.image.load("link/idle_back.png").convert_alpha()
idle_left  = pygame.image.load("link/idle_left.png").convert_alpha()

walk_front = load_animation("walk_front", 3)
walk_back  = load_animation("walk_back", 3)
walk_left  = load_animation("walk_left", 3)

# ----------------- CLASE JUGADOR -----------------
class Player:
    def __init__(self, x, y):
        self.rect = idle_front.get_rect(center=(x, y))
        self.speed = 2

        self.state = "idle"       # idle, walk
        self.direction = "front"  # front, back, left, right

        self.idle_sprites = {
            "front": idle_front,
            "back": idle_back,
            "left": idle_left
        }

        self.walk_sprites = {
            "front": walk_front,
            "back": walk_back,
            "left": walk_left
        }

        self.frame_index = 0
        self.anim_speed = 0.2

        self.image = self.idle_sprites["front"]

    def handle_input(self):
        dx = 0
        dy = 0
        moving = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
            moving = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "back"
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "front"
            moving = True

        self.state = "walk" if moving else "idle"
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

    def update_animation(self):
        if self.state == "idle":
            if self.direction == "right":
                self.image = pygame.transform.flip(self.idle_sprites["left"], True, False)
            else:
                self.image = self.idle_sprites.get(self.direction, self.idle_sprites["front"])
        else:
            base_dir = self.direction
            if base_dir == "right":
                base_dir = "left"

            sprites = self.walk_sprites[base_dir]

            self.frame_index += self.anim_speed
            if self.frame_index >= len(sprites):
                self.frame_index = 0

            self.image = sprites[int(self.frame_index)]

            if self.direction == "right":
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        prev_state = self.state
        self.handle_input()

        if self.state != prev_state:
            self.frame_index = 0

        self.update_animation()

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
player = Player(50, 50)
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
