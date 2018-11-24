import unittest
import main
import pygame


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_big_camera(self):
        camera = main.Camera(main.big_camera_configure,
                             self.game.total_level_width,
                             self.game.total_level_height)
        camera.update(self.game.hero)
        self.assertEqual(camera.state, pygame.Rect(0, 0, 2480, 960))

    def test_small_camera(self):
        camera = main.Camera(main.small_camera_configure,
                             self.game.total_level_width,
                             self.game.total_level_height)
        camera.update(self.game.hero)
        self.assertEqual(camera.state, pygame.Rect(0, 0, 2480, 960))


if __name__ == '__main__':
    unittest.main()
