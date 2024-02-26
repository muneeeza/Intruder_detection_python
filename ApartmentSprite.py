import pygame
import random

class Apartment(pygame.sprite.Sprite):

    window_path = 'images/nothing_broken.png'
    broken_window_path = 'images/broken_window_only.png'
    broken_lock_path = 'images/broken_lock_only.png'
    both_broken_path = 'images/broken_window_lock.png'

    def __init__(self, x, y, width, height, broken_window, broken_lock):
        super().__init__()
        self.image = None  # Initialize image as None

        if broken_window == True and broken_lock == True:
            self.image = pygame.image.load(self.both_broken_path)
        elif broken_lock == True:
            self.image = pygame.image.load(self.broken_lock_path)
        elif broken_window == True:
            self.image = pygame.image.load(self.broken_window_path)
        else:
            self.image = pygame.image.load(self.window_path)

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.broken_window = broken_window
        self.broken_lock = broken_lock

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

