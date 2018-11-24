#!/usr/bin/env python
# -*- coding: utf-8 -*-

import blocks
import boosts
import monsters
import random
import config_level_generator as clg
from config_entity import WIDTH


class LevelGenerator:
    def __init__(self, game):
        self.game = game
        self.locked_coordinates = []
        self.right_width = clg.WIDTH_IN_BLOCKS - 2
        self.center = self.right_width // 2

    def get_level(self):
        self.choose_booster()
        self.make_exit_hider()
        self.make_booster_hider()
        self.make_hard_platforms()
        self.make_monsters()
        self.make_simple_platforms()

        self.locked_coordinates.clear()

    def choose_booster(self):
        if self.game.hero.level % 20 == 0:
            self.booster = 2
        elif self.game.hero.level % 10 == 0:
            self.booster = 3
        else:
            self.booster = random.randint(0, 1)

    def make_exit_hider(self):
        exit_y = random.randint(1, 9)
        if exit_y < clg.SAFE_ZONE:
            if exit_y % 2 == 0:
                exit_x = random.randint(clg.SAFE_ZONE, self.center * 2 + 1)
            else:
                exit_x = random.randint(clg.SAFE_ZONE, self.right_width)
        else:
            if exit_y % 2 == 0:
                exit_x = random.randint(1, self.center * 2 + 1)
            else:
                exit_x = random.randint(1, self.right_width)

        self.locked_coordinates.append((exit_x, exit_y))

        self.game.exit = blocks.ExitDoor(exit_x * WIDTH, exit_y * WIDTH)
        self.game.exit_hider = blocks.Platform(exit_x * WIDTH, exit_y * WIDTH)
        self.game.add_sprite(self.game.exit_hider)

    def make_booster_hider(self):
        while True:
            boost_y = random.randint(1, clg.HEIGHT_IN_BLOCKS - 3)
            if boost_y < clg.SAFE_ZONE:
                if boost_y % 2 == 0:
                    boost_x = random.randint(clg.SAFE_ZONE,
                                             self.center * 2 + 1)
                else:
                    boost_x = random.randint(clg.SAFE_ZONE, self.right_width)
            else:
                if boost_y % 2 == 0:
                    boost_x = random.randint(1, self.center * 2 + 1)
                else:
                    boost_x = random.randint(1, self.right_width)

            if (boost_x, boost_y) in self.locked_coordinates:
                continue
            else:
                break

        self.locked_coordinates.append((boost_x, boost_y))

        if self.booster == 0:
            self.game.boost = boosts.Additional_Life(boost_x * WIDTH,
                                                     boost_y * WIDTH)
        elif self.booster == 1:
            self.game.boost = boosts.Strength_Up(boost_x * WIDTH,
                                                 boost_y * WIDTH)
        elif self.booster == 2:
            self.game.boost = boosts.Remote_Bombs_Boost(boost_x * WIDTH,
                                                        boost_y * WIDTH)
        else:
            self.game.boost = boosts.Many_Bombs_Boost(boost_x * WIDTH,
                                                      boost_y * WIDTH)

        self.game.boost_hider = blocks.Platform(boost_x * WIDTH,
                                                boost_y * WIDTH)
        self.game.add_sprite(self.game.boost_hider)

    def make_hard_platforms(self):
        for x in range(clg.WIDTH_IN_BLOCKS):
            for y in range(clg.HEIGHT_IN_BLOCKS):
                if(x == 0 or y == 0 or x == clg.WIDTH_IN_BLOCKS - 1
                   or y == clg.HEIGHT_IN_BLOCKS - 1
                   or (x % 2 == 0 and y % 2 == 0)):
                    pf = blocks.Hard_Platform(x * WIDTH, y * WIDTH)
                    self.game.add_sprite(pf)

    def make_monsters(self):
        types_of_monsters = 1
        if self.game.hero.level > 15:
            types_of_monsters = 3
        elif self.game.hero.level > 5:
            types_of_monsters = 2

        for _ in range(1, min(15, 5 + self.game.hero.level // 5)):
            monster_x = monster_y = 0
            while True:
                monster_y = random.randint(1, clg.HEIGHT_IN_BLOCKS - 3)
                if monster_y < clg.SAFE_ZONE - 1:
                    if monster_y % 2 == 0:
                        monster_x = random.randint(clg.SAFE_ZONE - 1,
                                                   self.center * 2 + 1)
                    else:
                        monster_x = random.randint(clg.SAFE_ZONE - 1,
                                                   self.right_width)
                else:
                    if monster_y % 2 == 0:
                        monster_x = random.randint(1, self.center * 2 + 1)
                    else:
                        monster_x = random.randint(1, self.right_width)
                if (monster_x, monster_y) in self.locked_coordinates:
                    continue
                else:
                    break

            monster_type = random.randint(1, types_of_monsters)

            if monster_type == 1:
                monster = monsters.Baloon(monster_x * WIDTH, monster_y * WIDTH)
                self.game.baloon_monsters.append(monster)
            elif monster_type == 2:
                monster = monsters.Shadow(monster_x * WIDTH, monster_y * WIDTH)
                self.game.shadow_monsters.append(monster)
            else:
                monster = monsters.Chaser(monster_x * WIDTH, monster_y * WIDTH)
                self.game.chaser_monsters.append(monster)

            self.game.add_sprite(monster)
            self.locked_coordinates.append((monster_x, monster_y))

    def make_simple_platforms(self):
        for _ in range(1, 60):
            block_x = block_y = 0
            while True:
                block_y = random.randint(1, 9)
                if block_y < clg.SAFE_ZONE - 3:
                    if block_y % 2 == 0:
                        block_x = random.randint(clg.SAFE_ZONE - 3,
                                                 self.center * 2 + 1)
                    else:
                        block_x = random.randint(clg.SAFE_ZONE - 3,
                                                 self.right_width)
                else:
                    if block_y % 2 == 0:
                        block_x = random.randint(1, self.center * 2 + 1)
                    else:
                        block_x = random.randint(1, self.right_width)

                if (block_x, block_y) in self.locked_coordinates:
                    continue
                else:
                    break

            pf = blocks.Platform(block_x * WIDTH, block_y * WIDTH)
            self.game.add_sprite(pf)
            self.locked_coordinates.append((block_x, block_y))
