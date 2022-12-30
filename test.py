import pygame
import sys
import os

FPS = 120
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
network_sprites = pygame.sprite.Group()
pygame.mixer.music.load('data/sound.mp3')


def load_music():
    pygame.mixer.music.play(33333)


def load_image(name, colorkey=None, reverse=False, size_image=None):
    fullname = os.path.join('data/', name)
    if not os.path.isfile(fullname):
        print(f'Файл с рисунком "{fullname}" не найден!')
        sys.exit()
    image = pygame.image.load(fullname)
    if reverse:
        image = pygame.transform.flip(image, True, False)
    if size_image is not None:
        image = pygame.transform.scale(image, size_image)
    if colorkey is None:
        image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class MusicButton(pygame.sprite.Sprite):
    image = load_image('music_image.png')

    def __init__(self, x, y):
        super().__init__(network_sprites)
        self.image = MusicButton.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MainHero(pygame.sprite.Sprite):
    image = load_image("main_goose.png", None, False, (100, 100))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = MainHero.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y, reverse_hero):
        self.rect.x = x
        self.rect.y = y
        if reverse_hero == 1:
            self.image = load_image('main_goose.png', None, True, (100, 100))
        elif reverse_hero == 2:
            self.image = load_image('main_goose.png', None, False, (100, 100))


def pause(screen):
    pygame.draw.rect(screen, (0, 0, 0), (150, 150, 300, 400))
    font = pygame.font.Font(None, 100)
    pause_text = font.render('Пауза', True, (125, 125, 125))
    text_place = pause_text.get_rect(center=(300, 250))
    screen.blit(pause_text, text_place)
    pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


def load_menu():
    pygame.init()
    size_menu = width_menu, height_menu = 600, 600
    menu_screen = pygame.display.set_mode(size_menu)
    background = pygame.image.load("data/background.jpg")
    menu_screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption('Гусь-Стеночник')
    playing_font = load_image('font.png', None, False, (600, 400))
    menu_screen.blit(playing_font, (50, 0))
    pygame.display.flip()
    while True:
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                terminate()
            elif menu_event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


clock = pygame.time.Clock()
rect_hero = pygame.Rect(400, 350, 30, 30)
speed = 10
jump = False
jump_count = 0
jump_max = 15
main_hero = MainHero(0, 0)
all_sprites.add(main_hero)
music_button = MusicButton(520, 0)
network_sprites.add(music_button)
running = True
running_menu = True
pause_mode = False
load_menu()
load_music()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.unicode == '\x1b':
                if pause_mode:
                    pause_mode = False
                else:
                    pause_mode = True
                    pause(screen)
            if not jump and event.key == pygame.K_SPACE:
                jump = True
                jump_count = jump_max
    pressed_keys = pygame.key.get_pressed()
    reverse_hero = 0
    if pressed_keys[pygame.K_a]:
        reverse_hero = 1
    elif pressed_keys[pygame.K_d]:
        reverse_hero = 2
    if not pause_mode:
        rect_hero.centerx = (rect_hero.centerx + (pressed_keys[pygame.K_d] -
                                                  pressed_keys[pygame.K_a]) * speed) % 800
        if jump:
            rect_hero.y -= jump_count
            if jump_count > -jump_max:
                jump_count -= 1
            else:
                jump = False
        all_sprites.update(rect_hero.x, rect_hero.y, reverse_hero)
        screen.fill((0, 0, 255))
        pygame.draw.rect(screen, pygame.Color('brown'), (0, 435, 800, 600))
        all_sprites.draw(screen)
        pygame.display.flip()
