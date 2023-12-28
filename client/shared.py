import os
import pygame

pygame.init()
pygame.mixer.init()

FPS = 30
RESOLUTION = (600, 800)
WINDOW = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('Морской Бой!')
TORPEDO_SIZE = 16

SERVER_ADDRESS = ('127.0.0.1', 7878)

SPRITES_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'client', 'sprites')
SOUNDS_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'client', 'sounds')
FONTS_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'client', 'fonts')

SHIP_SPRITE = pygame.image.load(os.path.join(SPRITES_PATH, 'ship.png'))
SUBMARINE_SPRITE = pygame.image.load(
    os.path.join(SPRITES_PATH, 'submarine.png'))
TORPEDO_SPRITE = pygame.image.load(
    os.path.join(SPRITES_PATH, 'torpedo.png'))
WATER_SPRITE = pygame.image.load(
    os.path.join(SPRITES_PATH, 'water.png'))
EXPLOSION_SPRITE = pygame.image.load(
    os.path.join(SPRITES_PATH, 'explosion.png'))

EXPLOSION_SOUND = pygame.mixer.Sound(
    os.path.join(SOUNDS_PATH, 'explosion.wav'))
EXPLOSION_SOUND.set_volume(0.3)

GAME_FONT = pygame.freetype.Font(
    os.path.join(FONTS_PATH, 'Comic Sans MS.ttf'), 25)

CURRENT_STATE = 'game'  # scores, menu
