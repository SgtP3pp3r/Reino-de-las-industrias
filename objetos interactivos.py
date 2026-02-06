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
pygame.display.set_caption("TEST ::::: INTERACTIVE OBJECTS")

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
# ----------------- CARGA DE SPRITES DE ATAQUE -----------------
attack_front = load_animation("atack_front", 3)
attack_back  = load_animation("atack_back", 3)
attack_left  = load_animation("atack_left", 3)

object_image = pygame.Surface((32, 32))
object_image.fill((180, 120, 50))

rupee_image = pygame.Surface((20, 20))
rupee_image.fill((0, 200, 255))

# ----------------- CLASE JUGADOR -----------------
class Player:
    def __init__(self, x, y):
        self.rect = idle_front.get_rect(center=(x, y))
        self.speed = 4

        self.state = "idle"       # idle, walk, attack
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

        self.attack_sprites = {
            "front": attack_front,
            "back": attack_back,
            "left": attack_left
        }

        self.frame_index = 0
        self.anim_speed = 0.25
        self.image = self.idle_sprites["front"]

        self.attacking = False
        self.attack_cooldown = 0

        self.sword_hitbox = pygame.Rect(0, 0, 20, 20)

    def handle_input(self):
        dx = 0
        dy = 0
        moving = False

        keys = pygame.key.get_pressed()

        # ---- ATAQUE ----
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.state = "attack"
            self.frame_index = 0
            return

        # ---- NO MOVERSE SI ATACA ----
        if self.attacking:
            return

        # ---- MOVIMIENTO ----
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

        for obj in objects:
            if obj.solid and obj.active and self.rect.colliderect(obj.rect):
                if dx > 0:
                    self.rect.right = obj.rect.left
                if dx < 0:
                    self.rect.left = obj.rect.right

        # --- EJE Y ---
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

        for obj in objects:
            if obj.solid and obj.active and self.rect.colliderect(obj.rect):
                if dy > 0:
                    self.rect.bottom = obj.rect.top
                if dy < 0:
                    self.rect.top = obj.rect.bottom

    
    def update_sword_hitbox(self):
        if self.direction == "front":
            self.sword_hitbox.center = (self.rect.centerx, self.rect.bottom + 10)
        elif self.direction == "back":
            self.sword_hitbox.center = (self.rect.centerx, self.rect.top - 10)
        elif self.direction == "left":
            self.sword_hitbox.center = (self.rect.left - 10, self.rect.centery)
        elif self.direction == "right":
            self.sword_hitbox.center = (self.rect.right + 10, self.rect.centery)

    def update_animation(self):
        # -------- IDLE --------
        if self.state == "idle":
            if self.direction == "right":
                self.image = pygame.transform.flip(self.idle_sprites["left"], True, False)
            else:
                self.image = self.idle_sprites.get(self.direction, self.idle_sprites["front"])

        # -------- WALK --------
        elif self.state == "walk":
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

        # -------- ATTACK --------
        elif self.state == "attack":
            base_dir = self.direction
            if base_dir == "right":
                base_dir = "left"

            sprites = self.attack_sprites[base_dir]

            self.frame_index += self.anim_speed
            if self.frame_index >= len(sprites):
                self.attacking = False
                self.state = "idle"
                self.frame_index = 0
                return

            self.image = sprites[int(self.frame_index)]

            if self.direction == "right":
                self.image = pygame.transform.flip(self.image, True, False)

            self.update_sword_hitbox()

    def update(self):
        self.handle_input()
        self.update_animation()

    def draw(self, surface, camera_x, camera_y):
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        surface.blit(self.image, (screen_x, screen_y))

        # DEBUG: dibujar hitbox de espada
        if self.attacking:
            hx = self.sword_hitbox.x - camera_x
            hy = self.sword_hitbox.y - camera_y
            pygame.draw.rect(surface, (255, 0, 0), (hx, hy, self.sword_hitbox.width, self.sword_hitbox.height), 2)

class GameObject:
    def __init__(self, x, y, image, solid=False, interactable=False, name=""):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = solid
        self.interactable = interactable
        self.name = name
        self.active = True

    def interact(self, player):
        if not self.active:
            return

        if self.name == "chest":
            print("¡Abriste un cofre!")
            self.active = False

        elif self.name == "rupee":
            print("¡Recogiste una rupia!")
            self.active = False

    def draw(self, surface, camera_x, camera_y):
        if not self.active:
            return

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
objects = [
    GameObject(200, 150, object_image, solid=True, interactable=True, name="chest"),
    GameObject(400, 220, rupee_image, solid=False, interactable=True, name="rupee")
]

# ----------------- LOOP -----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        keys = pygame.key.get_pressed()

    if keys[pygame.K_e]:
        for obj in objects:
            if obj.interactable and obj.active:
                if player.rect.colliderect(obj.rect.inflate(10, 10)):
                    obj.interact(player)


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
    for obj in objects:
        obj.draw(SCREEN, camera.x, camera.y)
    pygame.display.update()

pygame.quit()
sys.exit()
