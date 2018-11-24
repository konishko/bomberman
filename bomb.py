#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from blocks import Block, Platform, Hard_Platform
import config_entity as ce
import config_bomb as cbomb
from config_window import DIR as ICON_DIR
import os
import time
import pyganim


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, strength):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("%s/images/bomb1.png" % ICON_DIR)
        e_x, e_y = x % ce.WIDTH, y % ce.WIDTH
        correct_x, correct_y = x // ce.WIDTH, y // ce.WIDTH
        if e_x > ce.WIDTH / 2:
            correct_x += 1
        if e_y > ce.WIDTH / 2:
            correct_y += 1
        self.rect = pygame.Rect(correct_x * ce.WIDTH,
                                correct_y * ce.WIDTH,
                                ce.WIDTH,
                                ce.WIDTH)
        self.is_blowed = False
        self.strength = strength
        self.time_of_planting = time.time()

        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in cbomb.ANIMATION_BOOM:
            boltAnim.append((anim, cbomb.ANIMATION_DELAY))
        self.boltAnimBlow = pyganim.PygAnimation(boltAnim)
        self.boltAnimBlow.play()

    def update(self, platforms):
        for pf in platforms:
            if pygame.sprite.collide_rect(self, pf):
                if isinstance(pf, Explosion):
                    self.is_blowed = True
                    return
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimBlow.blit(self.image, (0, 0))

        if (time.time() - self.time_of_planting) > 3:
            self.is_blowed = True


class BuddyBomb(Bomb):
    def __init__(self, x, y):
        Bomb.__init__(self, x, y, 1)
        self.image = pygame.image.load("%s/images/buddybomb1.png" % ICON_DIR)

    def _init_anim(self):
        boltAnim = []
        for anim in cbomb.ANIMATION_BOOM_BUDDY:
            boltAnim.append((anim, cbomb.ANIMATION_DELAY))
        self.boltAnimBlow = pyganim.PygAnimation(boltAnim)
        self.boltAnimBlow.play()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms, is_appendage, entities, strength):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("%s/images/c1.png" % ICON_DIR)
        self.rect = pygame.Rect(x, y, ce.WIDTH, ce.WIDTH)
        self.strength = strength
        self.is_ended = False
        self.time_of_exploding = time.time()

        if not is_appendage:
            self._init_anim()
            self.appendages = []
            self.make_appendages(platforms, entities)
            self.update(platforms, entities)

    def _init_anim(self):
        boltAnim = []
        for anim in cbomb.ANIMATION_BOOM_CENTER:
            boltAnim.append((anim, cbomb.ANIMATION_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def make_appendages(self, platforms, entities):
        up_ended = down_ended = left_ended = riht_ended = False

        for i in range(1, self.strength + 1):
            up_app = Platform(self.rect.x, self.rect.y - ce.WIDTH * i)
            down_app = Platform(self.rect.x, self.rect.y + ce.WIDTH * i)
            left_app = Platform(self.rect.x - ce.WIDTH * i, self.rect.y)
            right_app = Platform(self.rect.x + ce.WIDTH * i, self.rect.y)
            up_exist = down_exist = left_exist = right_exist = True

            for p in platforms:
                if not up_ended and pygame.sprite.collide_rect(p, up_app):
                    if isinstance(p, Block):
                        up_exist = False
                        up_ended = True
                    if isinstance(p, Platform):
                        platforms.remove(p)
                        entities.remove(p)
                elif up_ended:
                    up_exist = False

                if not down_ended and pygame.sprite.collide_rect(p, down_app):
                    if isinstance(p, Block):
                        down_exist = False
                        down_ended = True
                    if isinstance(p, Platform):
                        platforms.remove(p)
                        entities.remove(p)
                elif down_ended:
                    down_exist = False

                if not left_ended and pygame.sprite.collide_rect(p, left_app):
                    if isinstance(p, Block):
                        left_exist = False
                        left_ended = True
                    if isinstance(p, Platform):
                        platforms.remove(p)
                        entities.remove(p)
                elif left_ended:
                    left_exist = False

                if not riht_ended and pygame.sprite.collide_rect(p, right_app):
                    if isinstance(p, Block):
                        right_exist = False
                        riht_ended = True
                    if isinstance(p, Platform):
                        platforms.remove(p)
                        entities.remove(p)
                elif riht_ended:
                    right_exist = False

            if up_exist:
                appendage = AppendageExplosion(up_app.rect.x,
                                               up_app.rect.y,
                                               'up', platforms, entities)
                self.appendages.append(appendage)
            if down_exist:
                appendage = AppendageExplosion(down_app.rect.x,
                                               down_app.rect.y,
                                               'down', platforms, entities)
                self.appendages.append(appendage)
            if left_exist:
                appendage = AppendageExplosion(left_app.rect.x,
                                               left_app.rect.y,
                                               'left', platforms, entities)
                self.appendages.append(appendage)
            if right_exist:
                appendage = AppendageExplosion(right_app.rect.x,
                                               right_app.rect.y,
                                               'right', platforms, entities)
                self.appendages.append(appendage)

    def update(self, platforms, entities):
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        for app in self.appendages:
            app.update()
            if app.is_ended:
                platforms.remove(app)
                entities.remove(app)
                self.appendages.remove(app)

        if (time.time() - self.time_of_exploding) > 0.9:
            self.is_ended = True


class AppendageExplosion(Explosion):
    def __init__(self, x, y, orientation, platforms, entities):
        Explosion.__init__(self, x, y, platforms, True, entities, 1)
        self._init_anim(orientation)

        platforms.append(self)
        entities.add(self)

    def _init_anim(self, orientation):
        if orientation == 'up':
            self.image = pygame.image.load("%s/images/upb1.png" % ICON_DIR)
            boltAnim = []
            for anim in cbomb.ANIMATION_BOOM_UP:
                boltAnim.append((anim, cbomb.ANIMATION_DELAY))
            self.boltAnim = pyganim.PygAnimation(boltAnim)
            self.boltAnim.play()

        if orientation == 'down':
            self.image = pygame.image.load("%s/images/db1.png" % ICON_DIR)
            boltAnim = []
            for anim in cbomb.ANIMATION_BOOM_DOWN:
                boltAnim.append((anim, cbomb.ANIMATION_DELAY))
            self.boltAnim = pyganim.PygAnimation(boltAnim)
            self.boltAnim.play()

        if orientation == 'left':
            self.image = pygame.image.load("%s/images/lb1.png" % ICON_DIR)
            boltAnim = []
            for anim in cbomb.ANIMATION_BOOM_LEFT:
                boltAnim.append((anim, cbomb.ANIMATION_DELAY))
            self.boltAnim = pyganim.PygAnimation(boltAnim)
            self.boltAnim.play()

        if orientation == 'right':
            self.image = pygame.image.load("%s/images/rb1.png" % ICON_DIR)
            boltAnim = []
            for anim in cbomb.ANIMATION_BOOM_RIGHT:
                boltAnim.append((anim, cbomb.ANIMATION_DELAY))
            self.boltAnim = pyganim.PygAnimation(boltAnim)
            self.boltAnim.play()

    def update(self):
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        if (time.time() - self.time_of_exploding) > 0.7:
            self.is_ended = True
