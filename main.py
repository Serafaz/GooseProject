import pygame
import pygame_gui
import time
import sys
import os

FPS = 120
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
network_sprites = pygame.sprite.Group()
pygame.mixer.music.load('data/sound.mp3')
color_button = 'white'
playing_music = True
platforms_arr = []
G = 0.04
start = time.time()
rect_hero = pygame.Rect(400, 350, 30, 30)
reverse_hero = 1
need_to_load_menu = False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def update_event(last_event, start):
    global rect_hero, reverse_hero
    end = time.time()
    if last_event is not None and rect_hero is not None:
        if last_event.type == pygame.MOUSEBUTTONDOWN and end - start < 1:
            screen.fill((0, 0, 0))
            if reverse_hero == 1:
                rect_hero.x += 1
            else:
                rect_hero.x -= 1
            rect_hero.y -= 1
        if last_event.type == pygame.MOUSEBUTTONDOWN and end - start > 1.5:
            start = time.time()
            falling(rect_hero)


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


tile_images = {
    'platform': load_image('platform_tile.jpg', None, False, (50, 50)),
    'background-tile': load_image('background_tile.jpg', None, False, (50, 50))
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(platforms_group)
        self.image = tile_images['platform']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 15, tile_height * pos_y - 15)


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


def load_menu():
    pygame.init()
    size_menu = width_menu, height_menu = 600, 600
    menu_screen = pygame.display.set_mode(size_menu)
    background = pygame.image.load("data/background.jpg")
    menu_screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption('Гусь-Стеночник. Меню')
    playing_font = load_image('font.png', None, False, (600, 400))
    menu_screen.blit(playing_font, (50, 0))
    pygame.display.flip()
    while True:
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                terminate()
            elif menu_event.type == pygame.MOUSEBUTTONDOWN:
                main_game()
        pygame.display.flip()


def lose_screen():
    lose_image = load_image('lose_screen.png', None, False, (600, 600))
    running = True
    screen.blit(lose_image, (0, 0))
    text = pygame.font.Font(None, 50)
    rendered_text = text.render('CLICK <<R>> TO TRY AGAIN', True, (255, 255, 255))
    place = rendered_text.get_rect(center=(300, 500))
    screen.blit(rendered_text, place)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                load_menu()


def terminate():
    pygame.quit()
    sys.exit()


def pause(screen):
    global playing_music, pause_mode, need_to_load_menu
    manager = pygame_gui.UIManager((800, 600))
    music_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 250), (100, 100)),
        text='',
        manager=manager
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 350), (100, 100)),
        text='',
        manager=manager
    )
    music_image = load_image('music_image.png', None, False, (100, 100))
    exit_image = load_image('exit_image.png', None, False, (130, 130))
    pygame.draw.rect(screen, (125, 125, 125), (150, 50, 300, 450))
    font = pygame.font.Font(None, 100)
    pause_text = font.render('Пауза', True, (25, 25, 25))
    text_place = pause_text.get_rect(center=(300, 150))
    screen.blit(pause_text, text_place)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == music_button:
                        if playing_music is True:
                            playing_music = False
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                            playing_music = True
                    elif event.ui_element == exit_button:
                        pause_mode = False
                        need_to_load_menu = True
                        return
            if event.type == pygame.KEYDOWN:
                pause_pressed_keys = pygame.key.get_pressed()
                if pause_pressed_keys[pygame.K_ESCAPE]:
                    pause_mode = False
                    return
            elif event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        screen.blit(music_image, (255, 240))
        screen.blit(exit_image, (230, 340))
        if not playing_music:
            pygame.draw.line(screen, pygame.Color('red'),
                             (250, 343), (348, 258), 13)
        pygame.display.flip()


def get_collide(rect_hero):
    return False


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('background-tile', x, y)
            elif level[y][x] == '#':
                Platform(x, y)
                Tile('platform', x, y)
            elif level[y][x] == '@':
                Tile('background-tile', x, y)
    return x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def falling(rect_hero):
    rate_of_fall = 0.01
    while not get_collide(rect_hero):
        if reverse_hero == 1:
            rect_hero.x -= 1
            rect_hero.y += rate_of_fall
        else:
            rect_hero.x += 1
            rect_hero.y += rate_of_fall
        if rect_hero.y > 570:
            lose_screen()
        rate_of_fall += 0.01
        all_sprites.update(rect_hero.x, rect_hero.y, reverse_hero)
        all_sprites.draw(screen)
        pygame.display.flip()


def main_game():
    camera = Camera()
    global need_to_load_menu, rect_hero, reverse_hero
    clock = pygame.time.Clock()
    reverse_hero = 1
    rect_hero = pygame.Rect(400, 350, 30, 30)
    level_x, level_y = generate_level(load_level('level1.txt'))
    main_hero = MainHero(0, 0)
    all_sprites.add(main_hero)
    running = True
    pause_mode = False
    load_music()
    start = time.time()
    last_event = None
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 255))
        for event in pygame.event.get():
            if last_event is not None and event.type == pygame.MOUSEBUTTONUP and \
                    last_event.type != pygame.MOUSEBUTTONUP:
                start = time.time()
                if reverse_hero == 2:
                    reverse_hero = 1
                else:
                    reverse_hero = 2
                falling(rect_hero)
            last_event = event
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.unicode == '\x1b':
                    if pause_mode:
                        pause_mode = False
                    else:
                        pause_mode = True
                        pause(screen)
                        if need_to_load_menu:
                            need_to_load_menu = False
                            load_menu()
        update_event(last_event, start)
        if not pause_mode:
            all_sprites.update(rect_hero.x, rect_hero.y, reverse_hero)
            all_sprites.draw(screen)
            pygame.display.flip()


load_menu()
