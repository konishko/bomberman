#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from config_entity import WIDTH
from config_window import DIR as ICON_DIR
import os


class Boost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, WIDTH, WIDTH)


class Many_Bombs_Boost(Boost):
    def __init__(self, x, y):
        Boost.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/manybomb.png" % ICON_DIR)


class Remote_Bombs_Boost(Boost):
    def __init__(self, x, y):
        Boost.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/remote.png" % ICON_DIR)


class Strength_Up(Boost):
    def __init__(self, x, y):
        Boost.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/strofbomb.png" % ICON_DIR)


class Additional_Life(Boost):
    def __init__(self, x, y):
        Boost.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/addlife.png" % ICON_DIR)


class Speed_Up(Boost):
    def __init__(self, x, y):
        Boost.__init__(self, x, y)
        self.image = pygame.image.load("%s/images/speedup.png" % ICON_DIR)
