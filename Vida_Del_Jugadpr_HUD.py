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
pygame.display.set_caption("Zelda-like Fase 5.3")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (50, 180, 50)

# ----------------- MAPA POR TILES -----------------
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
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

# ----------------- SPRITES TEMPORALES -----------------
player_image = pygame.Surface((28, 28))
player_image.fill((50, 100, 255))

enemy_image = pygame.Surface((28, 28))
enemy_image.fill((200, 50, 50))

object_image = pygame.Surface((32, 32))
object_image.fill((180, 120, 50))

rupee_image = pygame.Surface((20, 20))
rupee_image.fill((0, 200, 255))

door_image = pygame.Surface((32, 48))
door_image.fill((120, 80, 40))

switch_image = pygame.Surface((32, 16))
switch_image.fill((200, 200, 50))

key_image = pygame.Surface((16, 16))
key_image.fill((255, 215, 0))

heart_image = pygame.Surface((16, 16))
heart_image.fill((220, 40, 40))


# ----------------- CLASE JUGADOR -----------------
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.direction = "front"
        self.keys = 0
        self.sword_hitbox = pygame.Rect(0, 0, 20, 20)
        self.attacking = False
        self.max_health = 5
        self.health = 5

        self.invulnerable = False
        self.invuln_timer = 0

        self.knockback = pygame.Vector2(0, 0)

    def handle_input(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "back"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "front"

        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.update_sword_hitbox()
        else:
            self.attacking = False

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

    def update(self):
        self.handle_input()
        # --- Knockback ---
        self.rect.x += int(self.knockback.x)
        self.rect.y += int(self.knockback.y)
        self.knockback *= 0.8

        # --- Inmunidad ---
        if self.invulnerable:
            self.invuln_timer -= 1
            if self.invuln_timer <= 0:
                self.invulnerable = False


    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        if self.attacking:
            pygame.draw.rect(surface, (255, 0, 0),
                (self.sword_hitbox.x - camera_x, self.sword_hitbox.y - camera_y,
                 self.sword_hitbox.width, self.sword_hitbox.height), 2)

    def take_damage(self, direction):
        if self.invulnerable:
            return

        self.health -= 1
        self.invulnerable = True
        self.invuln_timer = 60  # 1 segundo

        # Knockback
        if direction == "front":
            self.knockback = pygame.Vector2(0, 8)
        elif direction == "back":
            self.knockback = pygame.Vector2(0, -8)
        elif direction == "left":
            self.knockback = pygame.Vector2(-8, 0)
        elif direction == "right":
            self.knockback = pygame.Vector2(8, 0)

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

# ----------------- ENEMIGO -----------------
class Enemy:
    def __init__(self, x, y):
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = "left"
        self.health = 3
        self.alive = True
        self.knockback = pygame.Vector2(0, 0)

    def move(self):
        if not self.alive:
            return

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        for wall in walls:
            if self.rect.colliderect(wall):
                if self.direction == "left":
                    self.rect.left = wall.right
                    self.direction = "right"
                else:
                    self.rect.right = wall.left
                    self.direction = "left"

        self.rect.x += int(self.knockback.x)
        self.rect.y += int(self.knockback.y)
        self.knockback *= 0.8

    def take_damage(self, direction):
        self.health -= 1

        if direction == "front":
            self.knockback = pygame.Vector2(0, 6)
        elif direction == "back":
            self.knockback = pygame.Vector2(0, -6)
        elif direction == "left":
            self.knockback = pygame.Vector2(-6, 0)
        elif direction == "right":
            self.knockback = pygame.Vector2(6, 0)

        if self.health <= 0:
            self.alive = False

    def update(self):
        self.move()

    def draw(self, surface, camera_x, camera_y):
        if not self.alive:
            return

        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

# ----------------- OBJETOS -----------------
class GameObject:
    def __init__(self, x, y, image, solid=False, interactable=False, name="", requires_key=False):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = solid
        self.interactable = interactable
        self.name = name
        self.requires_key = requires_key
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

        elif self.name == "key":
            print("¡Obtuviste una llave!")
            player.keys += 1
            self.active = False

        elif self.name == "switch":
            print("¡Activaste un interruptor!")
            self.active = False
            for obj in objects:
                if obj.name == "door":
                    obj.active = False
                    obj.solid = False

        elif self.name == "door":
            if self.requires_key and player.keys > 0:
                print("¡Abriste la puerta con una llave!")
                player.keys -= 1
                self.active = False
                self.solid = False
            else:
                print("La puerta está cerrada.")

    def draw(self, surface, camera_x, camera_y):
        if not self.active:
            return

        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

# ----------------- INIT -----------------
clock = pygame.time.Clock()
player = Player(50, 50)
camera = Camera(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)

enemies = [
    Enemy(300, 200)
]

objects = [
    GameObject(200, 150, object_image, solid=True, interactable=True, name="chest"),
    GameObject(400, 220, rupee_image, solid=False, interactable=True, name="rupee"),
    GameObject(120, 120, key_image, solid=False, interactable=True, name="key"),
    GameObject(300, 96, door_image, solid=True, interactable=True, name="door", requires_key=True),
    GameObject(500, 160, switch_image, solid=False, interactable=True, name="switch"),
]

# ----------------- LOOP -----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.health <= 0:
        print("GAME OVER")
        running = False

    
    player.update()
    camera.update(player)

    # --- Golpes a enemigos ---
    for enemy in enemies:
        if enemy.alive and player.attacking:
            if player.sword_hitbox.colliderect(enemy.rect):
                enemy.take_damage(player.direction)

    for enemy in enemies:
        if enemy.alive and player.rect.colliderect(enemy.rect):
            player.take_damage(enemy.direction)

    
    # --- Interacción con objetos (E) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        for obj in objects:
            if obj.interactable and obj.active:
                if player.rect.colliderect(obj.rect.inflate(10, 10)):
                    obj.interact(player)

    for enemy in enemies:
        enemy.update()

    SCREEN.fill(GRAY)

    # --- MAPA ---
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

    for obj in objects:
        obj.draw(SCREEN, camera.x, camera.y)

    for enemy in enemies:
        enemy.draw(SCREEN, camera.x, camera.y)

    player.draw(SCREEN, camera.x, camera.y)
    
    for i in range(player.health):
      SCREEN.blit(heart_image, (10 + i * 20, 10))


    pygame.display.update()

pygame.quit()
sys.exit()
