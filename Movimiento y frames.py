import pygame
import sys

pygame.init()

# ----------------- CONFIG -----------------
WIDTH, HEIGHT = 400, 225
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Personaje Idle + Walk Direccional")

# ----------------- COLORES -----------------
WHITE = (255, 255, 255)

# ----------------- CARGA DE SPRITES -----------------
idle_front = pygame.image.load("link/idle_front.png").convert_alpha()
idle_back  = pygame.image.load("link/idle_back.png").convert_alpha()
idle_left  = pygame.image.load("link/idle_left.png").convert_alpha()

def load_animation(prefix, count):
    return [pygame.image.load(f"link/{prefix}_{i}.png").convert_alpha() for i in range(count)]

walk_front = load_animation("walk_front", 3)
walk_back  = load_animation("walk_back", 3)
walk_left  = load_animation("walk_left", 3)

# ----------------- CLASE PERSONAJE -----------------
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 150
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
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def handle_input(self, keys):
        moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            moving = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            moving = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "back"
            moving = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "front"
            moving = True

        # LÍMITES DE PANTALLA
        self.x = max(0, min(WIDTH - self.rect.width, self.x))

        # CAMBIO DE ESTADO
        self.state = "walk" if moving else "idle"

    def update_animation(self):
        # -------- IDLE --------
        if self.state == "idle":
            if self.direction == "right":
                self.image = pygame.transform.flip(self.idle_sprites["left"], True, False)
            else:
                self.image = self.idle_sprites.get(self.direction, self.idle_sprites["front"])

        # -------- WALK --------
        else:
            # siempre usar sprites base: front / back / left
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

        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def update(self, keys):
        prev_state = self.state
        self.handle_input(keys)

        if self.state != prev_state:
            self.frame_index = 0

        self.update_animation()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ----------------- LOOP PRINCIPAL -----------------
clock = pygame.time.Clock()
player = Player()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.update(keys)

    SCREEN.fill(WHITE)
    player.draw(SCREEN)
    pygame.display.update()

pygame.quit()
sys.exit()
