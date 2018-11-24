import pygame
import config_entity as ce
import config_main as cmain
import config_window as cwin
import config_level_generator as clg
from hero import Hero
from bomb import Bomb, BuddyBomb, Explosion, AppendageExplosion
from monsters import Baloon, Shadow, Chaser
from menues import MainMenu, PauseMenu
from collections import deque
from blocks import Block
from buddy import Buddy
from math import sqrt
from levelgenerator import LevelGenerator
import os
import time
import random


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move((self.state.left,
                                 self.state.top + cwin.INFO_PANEL_HEIGHT))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def big_camera_configure(camera, target_rect):
    left, top, _, _ = target_rect
    _, _, width, height = camera
    left, top = -left + cwin.WIN_WIDTH / 2, -top + cwin.WIN_HEIGHT / 2

    left = min(0, left)
    left = max(-(camera.width - cwin.WIN_WIDTH), left)
    top = max(-(camera.height - cwin.WIN_HEIGHT), top)
    top = min(0, top)

    return pygame.Rect(left, top, width, height)


def small_camera_configure(camera, target_rect):
    left, top, _, _ = target_rect
    _, _, width, height = camera
    left, top = (-left + ((cwin.WIN_WIDTH - cwin.CUTTER_WIDTH) / 2) / 2,
                 -top + cwin.WIN_HEIGHT / 2)

    left = min(0, left)
    left = max(-(camera.width - (cwin.WIN_WIDTH - 20) / 2), left)
    top = max(-(camera.height - cwin.WIN_HEIGHT), top)
    top = min(0, top)

    return pygame.Rect(left, top, width, height)


class Game:
    def __init__(self):
        pygame.init()
        self.first_launch = True
        self.testing = True

        self.big_bg = pygame.Surface((cwin.WIN_WIDTH, cwin.WIN_HEIGHT))
        self.first_small_bg = pygame.Surface(
                              ((cwin.WIN_WIDTH - cwin.CUTTER_WIDTH) / 2,
                               cwin.WIN_HEIGHT))
        self.second_small_bg = pygame.Surface(
                               ((cwin.WIN_WIDTH - cwin.CUTTER_WIDTH) / 2,
                                cwin.WIN_HEIGHT))
        self.info = pygame.Surface((cwin.WIN_WIDTH, cwin.INFO_PANEL_HEIGHT))

        self.big_bg.fill(pygame.Color(cmain.BACKGROUND_COLOR))
        self.first_small_bg.fill(pygame.Color(cmain.BACKGROUND_COLOR))
        self.second_small_bg.fill(pygame.Color(cmain.BACKGROUND_COLOR))
        self.info.fill(pygame.Color("#000000"))

        pygame.font.init()
        self.inf_font = pygame.font.Font('%s/fonts/visitor1.ttf' % cwin.DIR,
                                         cwin.INFO_PANEL_HEIGHT - 4)
        self.message_font = pygame.font.Font('%s/fonts/visitor1.ttf'
                                             % cwin.DIR,
                                             ce.WIDTH)

        self.baloon_monsters = []
        self.chaser_monsters = []
        self.shadow_monsters = []

        self.entities = pygame.sprite.Group()
        self.platforms = []

        self.timer = pygame.time.Clock()

        self.queue_of_bombs = deque()
        self.queue_of_explosions = deque()

        self.bombs_pops = self.explosions_pops = 0
        self.left = self.right = self.down = self.up = self.space = False
        self.boom = self.is_remote = False
        self.is_exit_hider_broken = self.is_boost_hider_broken = False

        self.buttons_queue = deque()

        self.total_level_width = ce.WIDTH * clg.WIDTH_IN_BLOCKS
        self.total_level_height = ce.WIDTH * clg.HEIGHT_IN_BLOCKS

        self.big_camera = Camera(big_camera_configure,
                                 self.total_level_width,
                                 self.total_level_height)
        self.small_camera = Camera(small_camera_configure,
                                   self.total_level_width,
                                   self.total_level_height)

    def init_main_menu(self):
        self.testing = False
        main_menu = MainMenu(self)
        main_menu.menu()

    def start(self):
        self.save_data = '1 3 0 5 0 0 1 1 0'

        for p in self.entities:
            if isinstance(p, Hero):
                self.entities.remove(p)

        self.hero = Hero(ce.WIDTH, ce.WIDTH)
        self.entities.add(self.hero)

        data = self.save_data.split()

        self.hero.level = int(data[0])
        self.hero.lifes = int(data[1])
        self.hero.scores = int(data[2])
        self.hero.speed = int(data[3])
        self.hero.fly_cheat = bool(int(data[4]))
        self.hero.god_cheat = bool(int(data[5]))
        self.hero.strength_of_bombs = int(data[6])
        self.hero.max_count_of_bombs = int(data[7])
        self.hero.remote_bombs_boost = bool(int(data[8]))

    def play(self):
        while True:
            self.timer.tick(60)
            self.get_events()

            if self.hero.buddy_exist:
                self.buddy.update(self.buddy_left, self.buddy_right,
                                  self.buddy_up, self.buddy_down,
                                  self.platforms)

                if self.buddy.died or self.buddy.deleted:
                    self.delete_buddy()

            self.check_cheats()
            self.hero.update(self.left, self.right,
                             self.up, self.down,
                             self.platforms)

            if (self.hero.is_game_over or self.hero.is_game_won
               or self.hero.reload):
                break

            self.is_remote = self.hero.remote_bombs_boost
            self.monsters_update()
            self.bombs_update()
            self.explosions_update()
            self.hiders_update()
            self.update_screen()

    def update_screen(self):
        if not self.first_launch:
            if not self.hero.buddy_exist:
                target = self.hero
                self.update_big_background(target)

            elif(abs(self.hero.rect.x - self.buddy.rect.x)
                 < (cwin.WIN_WIDTH + cwin.CUTTER_WIDTH) / 2):
                target = Block((self.hero.rect.x + self.buddy.rect.x) / 2,
                               (self.hero.rect.y + self.buddy.rect.y) / 2)
                self.update_big_background(target)

            else:
                self.big_bg.fill(pygame.Color("#000000"))
                self.screen.blit(self.big_bg, (0, 0))

                if self.hero.rect.x < self.buddy.rect.x:
                    left = self.hero
                    right = self.buddy

                else:
                    left = self.buddy
                    right = self.hero

                self.update_small_background(self.first_small_bg, left, 0)

                self.update_small_background(self.second_small_bg, right,
                                             (cwin.WIN_WIDTH + 20) / 2)

            self.info.fill(pygame.Color("#000000"))
            msg = self.inf_font.render('LIFES: ' + str(self.hero.lifes),
                                       1, (255, 255, 255))
            self.info.blit(msg, (cwin.WIN_WIDTH - 2 * ce.WIDTH, 2))
            msg = self.inf_font.render('SCORE: ' + str(self.hero.scores),
                                       1, (255, 255, 255))
            self.info.blit(msg, (cwin.WIN_WIDTH / 2 - ce.WIDTH, 2))
            self.screen.blit(self.info, (0, 0))

            pygame.display.update()

        else:
            self.first_launch = False
            self.screen = pygame.display.set_mode(cwin.DISPLAY)
            pygame.display.set_caption("Bomberman")

    def update_big_background(self, target):
        self.big_camera.update(target)
        self.big_bg.fill(pygame.Color(cmain.BACKGROUND_COLOR))

        for e in self.entities:
            self.big_bg.blit(e.image, self.big_camera.apply(e))

        self.screen.blit(self.big_bg, (0, 0))

    def update_small_background(self, bg, target, place):
        self.small_camera.update(target)
        bg.fill(pygame.Color(cmain.BACKGROUND_COLOR))

        for e in self.entities:
            bg.blit(e.image, self.small_camera.apply(e))

        self.screen.blit(bg, (place, 0))

    def monsters_update(self):
        for baloon in self.baloon_monsters:
            baloon.update(self.platforms)
            if baloon.dead:
                self.remove_sprite(baloon)
                self.baloon_monsters.remove(baloon)
                self.hero.scores += 100

        for shadow in self.shadow_monsters:
            shadow.update(self.left, self.right,
                          self.up, self.down,
                          self.platforms)
            if shadow.dead:
                self.remove_sprite(shadow)
                self.shadow_monsters.remove(shadow)
                self.hero.scores += 100

        for chaser in self.chaser_monsters:
            chaser.update(self.hero.rect.x, self.hero.rect.y, self.platforms)
            if chaser.dead:
                self.remove_sprite(chaser)
                self.chaser_monsters.remove(chaser)
                self.hero.scores += 200

    def bombs_update(self):
        if self.hero.buddy_exist and self.buddy_bomb_exist:
            bomb_queue_length = self.hero.max_count_of_bombs + 1
        else:
            bomb_queue_length = self.hero.max_count_of_bombs

        if self.space and len(self.queue_of_bombs) < bomb_queue_length:
            bomb = Bomb(self.hero.rect.x, self.hero.rect.y,
                        self.hero.strength_of_bombs)
            self.queue_of_bombs.append(bomb)
            self.add_sprite(bomb)
            self.space = False

        if(self.hero.buddy_exist and self.buddy_bomb
           and not self.buddy_bomb_exist):
            bomb = BuddyBomb(self.buddy.rect.x, self.buddy.rect.y)
            self.queue_of_bombs.append(bomb)
            self.add_sprite(bomb)
            self.buddy_bomb_exist = True

        if not self.is_remote:
            for bomb in self.queue_of_bombs:
                bomb.update(self.platforms)
                if bomb.is_blowed:
                    if isinstance(bomb, BuddyBomb):
                        self.buddy_bomb_exist = False
                    self.remove_sprite(bomb)
                    self.bombs_pops += 1
                    explosion = Explosion(bomb.rect.x, bomb.rect.y,
                                          self.platforms, False,
                                          self.entities, bomb.strength)
                    self.queue_of_explosions.append(explosion)
                    self.add_sprite(explosion)

            while self.bombs_pops != 0:
                self.queue_of_bombs.popleft()
                self.bombs_pops -= 1

        elif self.boom:
            for bomb in self.queue_of_bombs:
                self.remove_sprite(bomb)
                self.bombs_pops += 1
                explosion = Explosion(bomb.rect.x, bomb.rect.y,
                                      self.platforms, False,
                                      self.entities, bomb.strength)
                self.queue_of_explosions.append(explosion)
                self.add_sprite(explosion)

            while self.bombs_pops != 0:
                self.queue_of_bombs.popleft()
                self.bombs_pops -= 1

    def explosions_update(self):
        for explosion in self.queue_of_explosions:
            explosion.update(self.platforms, self.entities)
            if explosion.is_ended:
                self.remove_sprite(explosion)
                self.explosions_pops += 1

        while self.explosions_pops != 0:
            self.queue_of_explosions.popleft()
            self.explosions_pops -= 1

        if not self.is_boost_hider_broken or not self.is_exit_hider_broken:
            self.is_exit_hider_broken = self.is_boost_hider_broken = True
            for p in self.platforms:
                if p == self.boost_hider:
                    self.is_boost_hider_broken = False
                if p == self.exit_hider:
                    self.is_exit_hider_broken = False

    def hiders_update(self):
        if not self.is_boost_hider_broken or not self.is_exit_hider_broken:
            self.is_exit_hider_broken = self.is_boost_hider_broken = True
            for p in self.platforms:
                if p == self.boost_hider:
                    self.is_boost_hider_broken = False
                if p == self.exit_hider:
                    self.is_exit_hider_broken = False

        if self.is_boost_hider_broken:
            self.entities.remove(self.boost_hider)
            self.add_sprite(self.boost)

        if self.is_exit_hider_broken:
            self.entities.remove(self.exit_hider)
            self.add_sprite(self.exit)

        if self.hero.is_boost_picked:
            self.remove_sprite(self.boost)

    def get_events(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pause_menu = PauseMenu(self)
                    pause_menu.menu()
                    if pause_menu.to_main:
                        self.hero.is_game_over = True
                if e.key == pygame.K_UP:
                    self.up = True
                if e.key == pygame.K_DOWN:
                    self.down = True
                if e.key == pygame.K_LEFT:
                    self.left = True
                if e.key == pygame.K_RIGHT:
                    self.right = True
                if e.key == pygame.K_SPACE:
                    self.space = True
                if e.key == pygame.K_m:
                    self.boom = True
                if e.key == pygame.K_h:
                    if not self.hero.buddy_exist and self.hero.lifes > 1:
                        self.spawn_buddy()
                    elif self.hero.buddy_exist:
                        if(sqrt((self.hero.rect.x - self.buddy.rect.x) ** 2
                                + (self.hero.rect.y - self.buddy.rect.y) ** 2)
                                < 1.5 * ce.WIDTH):
                            self.buddy.deleting = True
                            self.buddy.time_of_deleting = time.time()

                if self.hero.buddy_exist:
                    if e.key == pygame.K_w:
                        self.buddy_up = True
                    if e.key == pygame.K_s:
                        self.buddy_down = True
                    if e.key == pygame.K_a:
                        self.buddy_left = True
                    if e.key == pygame.K_d:
                        self.buddy_right = True
                    if e.key == pygame.K_v:
                        self.buddy_bomb = True

                if len(self.buttons_queue) == 3:
                    self.buttons_queue.popleft()
                self.buttons_queue.append(e.key)

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.up = False
                if e.key == pygame.K_DOWN:
                    self.down = False
                if e.key == pygame.K_RIGHT:
                    self.right = False
                if e.key == pygame.K_LEFT:
                    self.left = False
                if e.key == pygame.K_SPACE:
                    self.space = False
                if e.key == pygame.K_m:
                    self.boom = False

                if self.hero.buddy_exist:
                    if e.key == pygame.K_w:
                        self.buddy_up = False
                    if e.key == pygame.K_s:
                        self.buddy_down = False
                    if e.key == pygame.K_a:
                        self.buddy_left = False
                    if e.key == pygame.K_d:
                        self.buddy_right = False
                    if e.key == pygame.K_v:
                        self.buddy_bomb = False

    def spawn_buddy(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                potential_spawn_point = Block(self.hero.rect.x + i * ce.WIDTH,
                                              self.hero.rect.y + j * ce.WIDTH)
                is_avaliable = True
                for p in self.platforms:
                    if pygame.sprite.collide_rect(potential_spawn_point, p):
                        is_avaliable = False
                        break
                if is_avaliable:
                    self.buddy = Buddy(self.hero.rect.x + i * ce.WIDTH,
                                       self.hero.rect.y + j * ce.WIDTH)
                    self.add_sprite(self.buddy)
                    self.buddy_left = self.buddy_right = False
                    self.buddy_up = self.buddy_down = False
                    self.buddy_bomb = self.buddy_bomb_exist = False
                    self.hero.buddy_exist = True
                    self.hero.lifes -= 1
                    self.buddy.spawning = True
                    self.buddy.time_of_spawning = time.time()
                    break
            if self.hero.buddy_exist:
                break

    def delete_buddy(self):
        if not self.buddy.died:
            self.hero.lifes += 1
        self.remove_sprite(self.buddy)
        self.hero.buddy_exist = False

    def check_cheats(self):
        if self.buttons_queue == cmain.GOD:
            self.hero.god_cheat = True

        elif self.buttons_queue == cmain.FLY:
            self.hero.fly_cheat = True

        elif self.buttons_queue == cmain.BOM:
            self.hero.strength_of_bombs = 8
            self.hero.max_count_of_bombs = 6
            self.hero.remote_bombs_boost = True

    def make_save(self):
        if self.hero.buddy_exist:
            lifes = self.hero.lifes + 1
        else:
            lifes = self.hero.lifes
        save_log = '{} {} {} {} {} {} {} {} {}'.format(
            self.hero.level,
            lifes,
            self.hero.scores,
            self.hero.speed,
            self.hero.fly_cheat,
            self.hero.god_cheat,
            self.hero.strength_of_bombs,
            self.hero.max_count_of_bombs,
            self.hero.remote_bombs_boost)

        save_log = save_log.replace('False', '0')
        save_log = save_log.replace('True', '1')

        self.last_save_time = time.ctime().replace(':', '-')

        file = open('saves/Bomberman {}.txt'.format(self.last_save_time), 'w')
        file.write(save_log)
        file.close()

    def add_sprite(self, sprite):
        self.entities.add(sprite)
        self.platforms.append(sprite)

    def remove_sprite(self, sprite):
        self.entities.remove(sprite)
        self.platforms.remove(sprite)

    def clear_level(self):
        self.platforms.clear()
        for entity in self.entities:
            if not isinstance(entity, Hero):
                self.entities.remove(entity)
        self.baloon_monsters.clear()
        self.chaser_monsters.clear()
        self.shadow_monsters.clear()
        self.queue_of_bombs.clear()
        self.queue_of_explosions.clear()
        self.bombs_pops = self.explosions_pops = 0
        self.hero.is_boost_picked = False
        self.hero.is_game_won = False
        self.hero.buddy_exist = False
        self.is_boost_hider_broken = False
        self.is_exit_hider_broken = False

    def draw_message(self, text):
        self.big_bg.fill(pygame.Color("#000000"))
        self.info.fill(pygame.Color("#000000"))
        self.screen.blit(self.info, (0, 0))
        self.screen.blit(self.big_bg, (0, cwin.INFO_PANEL_HEIGHT))
        msg = self.message_font.render(text, 1, (255, 255, 255))
        self.screen.blit(msg,
                         (cwin.WIN_WIDTH / 2
                          - 3 * ce.WIDTH, cwin.WIN_HEIGHT / 2))
        pygame.display.update()
        time.sleep(2)


def main():
    game = Game()
    game.init_main_menu()
    level_generator = LevelGenerator(game)
    game.start()

    while True:
        game.clear_level()
        level_generator.get_level()
        game.draw_message('LEVEL ' + str(game.hero.level))
        game.play()

        if game.hero.is_game_over:
            game.draw_message('GAME OVER')
            game.init_main_menu()
            game.start()
            continue

        if game.hero.reload:
            game.hero.rect.x = game.hero.rect.y = game.hero.startX
            game.hero.reload = False
            continue

        if game.hero.is_game_won:
            game.hero.rect.x = game.hero.rect.y = game.hero.startX
            game.hero.level += 1


if __name__ == "__main__":
    main()
