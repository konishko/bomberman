#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config_hero as chero
import config_entity as ce
from config_window import DIR as ICON_DIR
from bomb import Explosion
from boosts import Additional_Life, Strength_Up
from boosts import Remote_Bombs_Boost, Many_Bombs_Boost
from monsters import Monster
from blocks import Platform, Hard_Platform, ExitDoor
import pyganim
import os
import time


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.dying = self.dead = False
        self.lifes = 3
        self.scores = 0
        self.speed = chero.MOVE_SPEED
        self.max_count_of_bombs = 1
        self.remote_bombs_boost = False
        self.strength_of_bombs = 1
        self.is_game_over = False
        self.is_game_won = False
        self.reload = False
        self.level = 1
        self.buddy_exist = False
        self.is_boost_picked = False
        self.god_cheat = False
        self.fly_cheat = False

        self.image = pygame.Surface((ce.WIDTH, ce.WIDTH))
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.rect = pygame.Rect(x, y, ce.WIDTH, ce.WIDTH)
        self.image.set_colorkey(pygame.Color(ce.BASIC_COLOR))

        self._init_anim()

    def _init_anim(self):
        boltAnim = []
        for anim in chero.ANIMATION_RIGHT:
            boltAnim.append((anim, chero.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in chero.ANIMATION_LEFT:
            boltAnim.append((anim, chero.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in chero.ANIMATION_UP:
            boltAnim.append((anim, chero.ANIMATION_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()

        boltAnim = []
        for anim in chero.ANIMATION_DOWN:
            boltAnim.append((anim, chero.ANIMATION_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

        boltAnim = []
        for anim in chero.ANIMATION_DYING:
            boltAnim.append((anim, chero.ANIMATION_DELAY))
        self.boltAnimDie = pyganim.PygAnimation(boltAnim)
        self.boltAnimDie.play()

        self.boltAnimStay = pyganim.PygAnimation(chero.ANIMATION_STAY)
        self.boltAnimStay.play()

    def die_update(self):
        self.image.fill(pygame.Color(ce.BASIC_COLOR))
        self.boltAnimDie.blit(self.image, (0, 0))

        if (time.time() - self.time_of_death > 0.7):
            if self.buddy_exist:
                self.lifes += 1
            self.lifes -= 1
            self.scores -= 1000
            self.reload = True
            if self.lifes == 0:
                self.is_game_over = True
            self.dying = False

    def update(self, left, right, up, down, platforms):
        if not self.dying:
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

        else:
            self.die_update()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if not self.god_cheat and (isinstance(p, Explosion)
                                           or isinstance(p, Monster)):
                    self.dying = True
                    self.time_of_death = time.time()

                if not self.fly_cheat and (isinstance(p, Platform)
                                           or isinstance(p, Hard_Platform)):
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                            self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top

                    if yvel < 0:
                        self.rect.top = p.rect.bottom

                elif isinstance(p, ExitDoor) and not self.is_game_won:
                    if self.buddy_exist:
                        self.lifes += 1
                    self.is_game_won = True
                    self.scores += 10000

                elif (isinstance(p, Many_Bombs_Boost)
                      and not self.is_boost_picked):
                    if self.max_count_of_bombs < 6:
                        self.max_count_of_bombs += 1
                    self.is_boost_picked = True
                    self.scores += 1000

                elif (isinstance(p, Remote_Bombs_Boost)
                      and not self.is_boost_picked):
                    self.remote_bombs_boost = True
                    self.is_boost_picked = True
                    self.scores += 1000

                elif (isinstance(p, Strength_Up)
                      and not self.is_boost_picked):
                    if self.strength_of_bombs < 9:
                        self.strength_of_bombs += 1
                    self.is_boost_picked = True
                    self.scores += 1000

                elif (isinstance(p, Additional_Life)
                      and not self.is_boost_picked):
                    self.lifes += 1
                    self.is_boost_picked = True
                    self.scores += 1000
