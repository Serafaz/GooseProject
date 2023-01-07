import pygame
import sys
import os


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
