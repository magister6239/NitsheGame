import pygame
pygame.init()
from objects import *

ZERO = (0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
CENTER = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)

font = pygame.font.Font("fonts/Second.ttf", 100)
