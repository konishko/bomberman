import unittest
import main
import bomb
from config_entity import WIDTH


class TestBomb(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_can_bomb_explode(self):
        my_bomb = bomb.Bomb(WIDTH, WIDTH, 1)
        my_bomb.time_of_planting = 0
        my_bomb.update(self.game.platforms)
        self.assertTrue(my_bomb.is_blowed)

    def test_can_bomb_make_explosion(self):
        my_bomb = bomb.Bomb(WIDTH, WIDTH, 1)
        my_bomb.is_blowed = True
        self.game.add_sprite(my_bomb)
        self.game.queue_of_bombs.append(my_bomb)
        self.game.bombs_update()
        self.assertTrue(len(self.game.queue_of_explosions) == 1)

    def test_can_hero_place_bomb(self):
        self.game.space = True
        self.game.bombs_update()
        self.assertTrue(len(self.game.queue_of_bombs) == 1)


if __name__ == '__main__':
    unittest.main()
