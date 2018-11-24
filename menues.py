#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config_window as cwin
import os


class Button:
    def __init__(self, x, y, name, number):
        self.x = x
        self.y = y
        self.number = number
        self.name = name


class MainMenu:
    def __init__(self, game):
        self.buttons = [Button(cwin.WIN_WIDTH / 2 - 200,
                               cwin.WIN_HEIGHT / 2, "NEW GAME", 0),
                        Button(cwin.WIN_WIDTH / 2 - 200,
                               cwin.WIN_HEIGHT / 2 + 100, "LOAD GAME", 1),
                        Button(cwin.WIN_WIDTH / 2 - 200,
                               cwin.WIN_HEIGHT / 2 + 200, "EXIT", 2)]
        self.game = game
        pygame.font.init()
        self.font = pygame.font.Font('%s/fonts/visitor1.ttf' % cwin.DIR, 70)
        self.bg = pygame.Surface((cwin.WIN_WIDTH, cwin.WIN_HEIGHT))
        self.bgpic = pygame.image.load('%s/images/mainmenu.png' % cwin.DIR)
        self.picked_button = 0
        self.is_ended = False

    def render(self, picked_button):
        if not self.game.first_launch:
            self.bg.blit(self.bgpic, [0, 0])
            for button in self.buttons:
                if picked_button == button.number:
                    msg = self.font.render("-> " + button.name,
                                           1, (255, 255, 255))
                    self.bg.blit(msg, (button.x, button.y))
                else:
                    msg = self.font.render(button.name, 1, (255, 255, 255))
                    self.bg.blit(msg, (button.x, button.y))

            self.game.screen.blit(self.bg, (0, 0))
            pygame.display.update()
        else:
            self.game.first_launch = False
            self.game.screen = pygame.display.set_mode(cwin.DISPLAY)
            pygame.display.set_caption("Bomberman")

    def menu(self):
        while True:
            if not self.game.testing:
                self.render(self.picked_button)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise SystemExit("QUIT")
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        if self.picked_button > 0:
                            self.picked_button -= 1

                    if e.key == pygame.K_DOWN:
                        if self.picked_button < len(self.buttons) - 1:
                            self.picked_button += 1

                    if e.key == pygame.K_RETURN:
                        if self.picked_button == 0:
                            self.is_ended = True
                        if self.picked_button == 1:
                            lm = LoadMenu(self.game)
                            lm.menu()
                            if lm.is_ended:
                                self.is_ended = True

                        if self.picked_button == 2:
                            raise SystemExit("QUIT")
            if self.is_ended:
                break


class PauseMenu:
    def __init__(self, game):
        self.buttons = [Button(cwin.WIN_WIDTH / 2 - 400, 200, "RESUME", 0),
                        Button(cwin.WIN_WIDTH / 2 - 400, 350, "SAVE GAME", 1),
                        Button(cwin.WIN_WIDTH / 2 - 400, 500,
                               "EXIT TO MAIN MENU", 2),
                        Button(cwin.WIN_WIDTH / 2 - 400, 650,
                               "EXIT TO DESKTOP", 3)]
        self.game = game
        pygame.font.init()
        self.is_ended = False
        self.to_main = False
        self.picked_button = 0
        self.font = pygame.font.Font('%s/fonts/visitor1.ttf' % cwin.DIR, 70)
        self.bg = pygame.Surface((cwin.WIN_WIDTH, cwin.WIN_HEIGHT))

    def render(self, picked_button):
        if not self.game.first_launch:
            self.bg.fill(pygame.Color("#000000"))
            msg = self.font.render("PAUSE MENU", 1, (255, 255, 255))
            self.bg.blit(msg, (200, 50))

            for button in self.buttons:
                if picked_button == button.number:
                    msg = self.font.render("-> " + button.name,
                                           1, (255, 255, 255))
                    self.bg.blit(msg, (button.x, button.y))
                else:
                    msg = self.font.render(button.name, 1, (255, 255, 255))
                    self.bg.blit(msg, (button.x, button.y))

            self.game.screen.blit(self.bg, (0, 0))
            pygame.display.update()

        else:
            self.game.first_launch = False
            self.game.screen = pygame.display.set_mode(cwin.DISPLAY)
            pygame.display.set_caption("Bomberman")

    def menu(self):
        while True:
            if not self.game.testing:
                self.render(self.picked_button)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise SystemExit("QUIT")
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        if self.picked_button > 0:
                            self.picked_button -= 1

                    if e.key == pygame.K_DOWN:
                        if self.picked_button < len(self.buttons) - 1:
                            self.picked_button += 1

                    if e.key == pygame.K_RETURN:
                        if self.picked_button == 0:
                            self.is_ended = True
                        if self.picked_button == 1:
                            self.game.make_save()
                        if self.picked_button == 2:
                            self.to_main = True
                        if self.picked_button == 3:
                            raise SystemExit("QUIT")

            if self.is_ended or self.to_main:
                break


class LoadMenu:
    def __init__(self, game):
        list_saves = os.listdir('saves')
        self.buttons = []
        for save in range(len(list_saves)):
            self.buttons.append(Button(100, (2 + save) * 100,
                                       list_saves[save], save))

        self.game = game

        pygame.font.init()
        self.font_small = pygame.font.Font('%s/fonts/visitor1.ttf'
                                           % cwin.DIR, 35)
        self.font_big = pygame.font.Font('%s/fonts/visitor1.ttf'
                                         % cwin.DIR, 70)

        self.bg = pygame.Surface((cwin.WIN_WIDTH, cwin.WIN_HEIGHT))

        self.is_ended = False
        self.to_main = False
        self.picked_button = 0

    def render(self, bg, picked_button):
        if not self.game.first_launch:
            self.bg.fill(pygame.Color("#000000"))
            msg = self.font_big.render("LOAD MENU", 1, (255, 255, 255))
            self.bg.blit(msg, (200, 50))

            begin_of_buttons = 0
            end_of_buttons = min(6, len(self.buttons))
            if picked_button > 3:
                begin_of_buttons = picked_button - 3
                end_of_buttons = min(picked_button + 3, len(self.buttons))

            for index in range(begin_of_buttons, end_of_buttons):
                button = self.buttons[index]
                if picked_button == button.number:
                    msg = self.font_small.render("-> " + button.name,
                                                 1, (255, 255, 255))
                    bg.blit(msg, (button.x, button.y - begin_of_buttons * 100))
                else:
                    msg = self.font_small.render(button.name,
                                                 1, (255, 255, 255))
                    bg.blit(msg, (button.x, button.y - begin_of_buttons * 100))

        else:
            self.game.first_launch = False
            self.game.screen = pygame.display.set_mode(cwin.DISPLAY)
            pygame.display.set_caption("Bomberman")

    def menu(self):
        while True:
            if not self.game.testing:
                self.render(self.bg, self.picked_button)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise SystemExit("QUIT")
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.to_main = True

                    if e.key == pygame.K_UP:
                        if self.picked_button > 0:
                            self.picked_button -= 1

                    if e.key == pygame.K_DOWN:
                        if self.picked_button < len(self.buttons) - 1:
                            self.picked_button += 1

                    if e.key == pygame.K_RETURN:
                        fs = open('saves/{}'.format(
                                             self.buttons[self.picked_button]
                                             .name), 'r')
                        self.game.save_data = fs.read()
                        fs.close()
                        self.is_ended = True

                    if e.key == pygame.K_DELETE:
                        button = self.buttons[self.picked_button]
                        self.buttons.remove(button)
                        os.remove('saves/{}'.format(button.name))

            if self.is_ended or self.to_main:
                break

            self.game.screen.blit(self.bg, (0, 0))
            pygame.display.update()
