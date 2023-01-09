import pygame
import pygame_gui
import pytmx
import sys
import os

FPS = 120
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
network_sprites = pygame.sprite.Group()
pygame.mixer.music.load('data/sound.mp3')
color_button = 'white'
playing_music = True
need_to_load_menu = False


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
                return
        pygame.display.flip()


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


if __name__ == '__main__':
    clock = pygame.time.Clock()
    rect_hero = pygame.Rect(400, 350, 30, 30)
    speed = 10
    jump = False
    jump_count = 0
    jump_max = 15
    main_hero = MainHero(0, 0)
    all_sprites.add(main_hero)
    running = True
    running_menu = True
    pause_mode = False
    load_menu()
    load_music()
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 255))
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
                        if need_to_load_menu:
                            need_to_load_menu = False
                            load_menu()
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
            pygame.draw.rect(screen, pygame.Color('brown'), (0, 435, 800, 600))
            all_sprites.draw(screen)
            pygame.display.flip()

