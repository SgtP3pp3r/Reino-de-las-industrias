import pygame
import sys

pygame.init()

# ----------------- CONFIG -----------------
WIDTH, HEIGHT = 800, 450
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Personaje con Idle y Walk")

# ----------------- COLORES -----------------
WHITE = (255, 255, 255)

# ----------------- CARGA DE SPRITES -----------------
# FUNCION PARA CARGAR LAS IMAGENES DE LAS ANIMACIONES
def load_animation(prefix, count):
    
    # CARGAMOS LAS IMAGENES DE LAS ANIMACIONES
    # f"assets/{prefix}_{i}.png" es la ruta de las imagenes
    # convert_alpha() es para que las imagenes se carguen en formato transparente   
    return [pygame.image.load(f"assets/{prefix}_{i}.png").convert_alpha() for i in range(count)]

# CARGAMOS LAS IMAGENES DE LAS ANIMACIONES
# idle_sprites es el nombre de la variable que va a contener las imagenes de la animacion de idle
# walk_sprites es el nombre de la variable que va a contener las imagenes de la animacion de walk
# load_animation es la funcion que carga las imagenes de las animaciones, transformandolas en una lista de imagenes
idle_sprites = load_animation("idle", 3)
walk_sprites = load_animation("walk", 4)

# ----------------- CLASE PERSONAJE -----------------
# CLASE PARA CREAR EL PERSONAJE
# self.x = WIDTH // 2 es para que el personaje se centre en la pantalla
# self.y = HEIGHT - 150 es para que el personaje se ubique en la parte inferior de la pantalla
# self.speed = 4 es la velocidad del personaje
# self.state = "idle" es el estado inicial del personaje
# self.direction = "right" es la direccion inicial del personaje
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 150
        self.speed = 4

        self.state = "idle"
        self.direction = "right"

        # self.animations = { "idle": idle_sprites, "walk": walk_sprites } es el diccionario que contiene las animaciones del personaje
        self.animations = {
            "idle": idle_sprites,
            "walk": walk_sprites
        }

        # self.frame_index = 0 es el indice de la imagen actual
        # self.anim_speed = 0.2 es la velocidad de la animacion
        # self.image = self.animations[self.state][0] es la imagen actual
        # self.rect = self.image.get_rect(midbottom=(self.x, self.y)) es el rectangulo de la imagen
        self.frame_index = 0
        self.anim_speed = 0.2
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        
        
    # FUNCION PARA MANEJAR LAS ENTRADAS DEL PERSONAJE
    # keys es el diccionario que contiene las teclas presionadas
    # moving es una variable que indica si el personaje esta moviendose
    # self.x -= self.speed es para que el personaje se mueva a la izquierda
    # self.x += self.speed es para que el personaje se mueva a la derecha
    # self.direction = "left" es para que el personaje se mueva a la izquierda
    # self.direction = "right" es para que el personaje se mueva a la derecha
    # moving = True es para que el personaje se mueva
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
        
        # LÍMITES DE PANTALLA
        # max(0, min(WIDTH - self.rect.width, self.x)) es para que el personaje no se salga de la pantalla
        # 0 es el valor minimo
        # WIDTH - self.rect.width es el valor maximo
        # self.x es la posicion del personaje
        self.x = max(0, min(WIDTH - self.rect.width, self.x))

        # CAMBIO DE ESTADO
        # "walk" es el estado de movimiento
        # "idle" es el estado de reposo
        # if moving es una condicion que indica si el personaje esta moviendose
        # else es una condicion que indica si el personaje no esta moviendose
        self.state = "walk" if moving else "idle"
        
    
    # FUNCION PARA ACTUALIZAR LA ANIMACION DEL PERSONAJE
    # sprites es el diccionario que contiene las animaciones del personaje
    # self.frame_index += self.anim_speed es para que la animacion avance
    # if self.frame_index >= len(sprites): es una condicion que indica si la animacion ha llegado al final
    # self.frame_index = 0 es para que la animacion vuelva al inicio
    # self.image = sprites[int(self.frame_index)] es para que la imagen actual sea la imagen de la animacion
    # if self.direction == "left": es una condicion que indica si el personaje esta mirando a la izquierda
    # pygame.transform.flip(self.image, True, False) es para que la imagen se espeje
    def update_animation(self):
        sprites = self.animations[self.state]

        self.frame_index += self.anim_speed
        if self.frame_index >= len(sprites):
            self.frame_index = 0

        self.image = sprites[int(self.frame_index)]

        # ESPEJO SI VA A LA IZQUIERDA
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    # FUNCION PARA ACTUALIZAR EL PERSONAJE
    # keys es el diccionario que contiene las teclas presionadas
    # self.handle_input(keys) es para que el personaje se mueva
    # self.update_animation() es para que la animacion del personaje se actualice
    def update(self, keys):
        self.handle_input(keys)
        self.update_animation()

    # FUNCION PARA DIBUJAR EL PERSONAJE
    # surface es la superficie de la pantalla
    # self.image es la imagen del personaje
    # self.rect es el rectangulo del personaje
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ----------------- LOOP PRINCIPAL -----------------
clock = pygame.time.Clock()
player = Player()

running = True
while running:
    clock.tick(FPS)

    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TECLAS PRESIONADAS    
    keys = pygame.key.get_pressed()
    # ACTUALIZAMOS EL PERSONAJE

    player.update(keys)

    # LIMPIAMOS LA PANTALLA
    SCREEN.fill(WHITE)
    # DIBUJAMOS EL PERSONAJE
    player.draw(SCREEN)
    # ACTUALIZAMOS LA PANTALLA
    pygame.display.update()

pygame.quit()
sys.exit()
