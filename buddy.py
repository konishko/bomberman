#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from bomb import Explosion
from monsters import Monster
from blocks import Platform, Hard_Platform
import config_buddy as cbuddy
import config_entity as ce
from config_window import DIR
import pyganim
import os
import time


class Buddy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.xvel = 0
        self.yvel = 0
        self.dying = self.died = False
        self.spawning = self.deleting = self.deleted = False
        self.speed = cbuddy.MOVE_SPEED

        self.image = pygame.Surface((ce.WIDTH, ce.WIDTH))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.rect = pygame.Rect(x, y, ce.WIDTH, ce.WIDTH)
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))

        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in cbuddy.ANIMATION_RIGHT:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_LEFT:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_UP:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_DOWN:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_DYING:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimDie = pyganim.PygAnimation(boltAnim)
        self.boltAnimDie.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_SPAWN:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimSpawn = pyganim.PygAnimation(boltAnim)
        self.boltAnimSpawn.play()

        boltAnim = []
        for anim in cbuddy.ANIMATION_STAY:
            boltAnim.append((anim, cbuddy.ANIMATION_DELAY))
        self.boltAnimStay = pyganim.PygAnimation(boltAnim)
        self.boltAnimStay.play()

    def spawn_update(self):
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimSpawn.blit(self.image, (0, 0))

        if (time.time() - self.time_of_spawning > 0.7):
            self.spawning = False

    def deleting_update(self):
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimDie.blit(self.image, (0, 0))

        if (time.time() - self.time_of_deleting > 0.7):
            self.deleted = True

    def die_update(self):
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimDie.blit(self.image, (0, 0))

        if (time.time() - self.time_of_death > 0.7):
            self.died = True

    def update(self, left, right, up, down, platforms):
        if not (self.dying or self.deleting or self.spawning):
            if up:
                self.yvel = -self.speed
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimUp.blit(self.image, (0, 0))

            if down:
                self.yvel = self.speed
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimDown.blit(self.image, (0, 0))

            if not (up or down):
                self.yvel = 0

            if left:
                self.xvel = -self.speed
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            if right:
                self.xvel = self.speed
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

            if not (left or right):
                self.xvel = 0

            if not(left or right or up or down):
                self.xvel = 0
                self.yvel = 0
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)

        elif self.dying:
            self.die_update()

        elif self.spawning:
            self.spawn_update()

        elif self.deleting:
            self.deleting_update()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Explosion) or isinstance(p, Monster):
                    self.dying = True
                    self.time_of_death = time.time()

                if isinstance(p, Platform) or isinstance(p, Hard_Platform):
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
