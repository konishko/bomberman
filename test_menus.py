import unittest
import main
import menues
import pygame
import os
from config_window import DIR


class TestMenus(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_main_menu_buttons(self):
        main_menu = menues.MainMenu(self.game)
        event = pygame.event.Event(pygame.KEYDOWN,
                                   key=pygame.K_DOWN,
                                   type=pygame.KEYDOWN)
        pygame.event.post(event)
        main_menu.is_ended = True
        main_menu.menu()
        self.assertEqual(main_menu.picked_button, 1)

    def test_pause_menu_buttons(self):
        pause_menu = menues.PauseMenu(self.game)
        event = pygame.event.Event(pygame.KEYDOWN,
                                   key=pygame.K_DOWN,
                                   type=pygame.KEYDOWN)
        pygame.event.post(event)
        pause_menu.is_ended = True
        pause_menu.menu()
        self.assertEqual(pause_menu.picked_button, 1)

    @unittest.skipIf(len([name for name in os.listdir('{}/saves'.format(DIR))
                     if os.path.isfile(os.path.join(
                        '{}/saves'.format(DIR), name))]) < 2,
                     'Not enough of files to work correctly')
    def test_load_menu_buttons(self):
        load_menu = menues.LoadMenu(self.game)
        event = pygame.event.Event(pygame.KEYDOWN,
                                   key=pygame.K_DOWN,
                                   type=pygame.KEYDOWN)
        pygame.event.post(event)
        load_menu.is_ended = True
        load_menu.menu()
        self.assertEqual(load_menu.picked_button, 1)


if __name__ == '__main__':
    unittest.main()
