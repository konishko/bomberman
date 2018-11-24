import unittest
import pygame
import main


class TestKeyboard(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_catching_of_pressed_buttons(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_UP,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_DOWN,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_LEFT,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_RIGHT,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_SPACE,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_m,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_h,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_w,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_s,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_a,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_d,
                                             type=pygame.KEYDOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             key=pygame.K_v,
                                             type=pygame.KEYDOWN))

        self.game.get_events()

        self.assertTrue(self.game.up)
        self.assertTrue(self.game.down)
        self.assertTrue(self.game.left)
        self.assertTrue(self.game.right)
        self.assertTrue(self.game.space)
        self.assertTrue(self.game.boom)
        self.assertTrue(self.game.hero.buddy_exist)
        self.assertTrue(self.game.buddy_up)
        self.assertTrue(self.game.buddy_down)
        self.assertTrue(self.game.buddy_left)
        self.assertTrue(self.game.buddy_right)
        self.assertTrue(self.game.buddy_bomb)

    def test_catching_of_unpressed_buttons(self):
        self.game.up = self.game.down = True
        self.game.left = self.game.right = True
        self.game.space = self.game.boom = True
        self.game.buddy_up = self.game.buddy_down = True
        self.game.buddy_left = self.game.buddy_right = True
        self.game.buddy_bomb = self.game.hero.buddy_exist = True

        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_UP,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_DOWN,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_LEFT,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_RIGHT,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_SPACE,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_m,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_w,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_s,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_a,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_d,
                                             type=pygame.KEYUP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP,
                                             key=pygame.K_v,
                                             type=pygame.KEYUP))

        self.game.get_events()

        self.assertFalse(self.game.up)
        self.assertFalse(self.game.down)
        self.assertFalse(self.game.left)
        self.assertFalse(self.game.right)
        self.assertFalse(self.game.space)
        self.assertFalse(self.game.boom)
        self.assertFalse(self.game.buddy_up)
        self.assertFalse(self.game.buddy_down)
        self.assertFalse(self.game.buddy_left)
        self.assertFalse(self.game.buddy_right)
        self.assertFalse(self.game.buddy_bomb)


if __name__ == '__main__':
    unittest.main()
