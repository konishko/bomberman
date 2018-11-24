#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pyganim
from bomb import Bomb, Explosion
from blocks import Block
import config_monsters as cmon
import config_entity as ce
import time
import random
import os


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.dying = False
        self.dead = False
        self.image = pygame.Surface((ce.WIDTH, ce.WIDTH))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.rect = pygame.Rect(x, y, ce.WIDTH, ce.WIDTH)
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))

    def die_update(self):
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimDying.blit(self.image, (0, 0))
        if (time.time() - self.time_of_death > 0.9):
            self.dead = True

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Explosion):
                    self.dying = True
                    self.time_of_death = time.time()
                elif isinstance(p, Block) or isinstance(p, Bomb):
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top

                    if yvel < 0:
                        self.rect.top = p.rect.bottom


class Baloon(Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y)
        self.last_move = 0
        self.last_move_steps = 0

        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in cmon.ANIMATION_RIGHT_DOWN_BALOON:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in cmon.ANIMATION_LEFT_UP_BALOON:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in cmon.ANIMATION_DYING_BALOON:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimDying = pyganim.PygAnimation(boltAnim)
        self.boltAnimDying.play()

    def update(self, platforms):
        if not self.dying:
            if self.last_move == 0 or self.last_move_steps > 47:
                self.last_move_steps = 0
                way = random.randint(1, 4)
            else:
                way = self.last_move

            if way == 1:
                self.yvel = -cmon.MOVE_SPEED
                self.xvel = 0
            elif way == 2:
                self.yvel = cmon.MOVE_SPEED
                self.xvel = 0
            elif way == 3:
                self.xvel = -cmon.MOVE_SPEED
                self.yvel = 0
            else:
                self.xvel = cmon.MOVE_SPEED
                self.yvel = 0

            self.last_move_steps += 1
            self.last_move = way
            self.image.fill(pygame.Color(ce.BASIC_COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)

        else:
            self.die_update()


class Shadow(Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y)
        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in cmon.ANIMATION_RIGHT_DOWN_SHADOW:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in cmon.ANIMATION_LEFT_UP_SHADOW:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in cmon.ANIMATION_DYING_SHADOW:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimDying = pyganim.PygAnimation(boltAnim)
        self.boltAnimDying.play()

    def update(self, left, right, up, down, platforms):
        if not self.dying:
            if up:
                self.yvel = -cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            if down:
                self.yvel = cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

            if left:
                self.xvel = -cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            if right:
                self.xvel = cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

            if not(left or right or up or down):
                self.xvel = 0
                self.yvel = 0
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)

        else:
            self.die_update()


class Chaser(Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y)

        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in cmon.ANIMATION_RIGHT_DOWN_CHASER:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in cmon.ANIMATION_LEFT_UP_CHASER:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in cmon.ANIMATION_DYING_CHASER:
            boltAnim.append((anim, cmon.ANIMATION_DELAY))
        self.boltAnimDying = pyganim.PygAnimation(boltAnim)
        self.boltAnimDying.play()

    def update(self, x, y, platforms):
        if not self.dying:
            if self.rect.x <= x:
                self.xvel = cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

            if self.rect.x > x:
                self.xvel = -cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            if self.rect.y <= y:
                self.yvel = cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

            if self.rect.y > y:
                self.yvel = -cmon.MOVE_SPEED
                self.image.fill(pygame.Color(ce.BASIC_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)

        else:
            self.die_update()
