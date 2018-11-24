#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from config_entity import WIDTH
from config_window import DIR
import os


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, WIDTH, WIDTH)


class Platform(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/b.png" % DIR)


class Hard_Platform(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/hb.png" % DIR)


class ExitDoor(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/exit.png" % DIR)
