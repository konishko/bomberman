import unittest
import main
import levelgenerator
import os


class TestUtility(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_clearing(self):
        self.lvlgnrtr = levelgenerator.LevelGenerator(self.game)
        self.lvlgnrtr.get_level()
        self.game.clear_level()

        self.assertEqual(len(self.game.platforms), 0)
        self.assertEqual(len(self.game.entities), 1)
        self.assertEqual(len(self.game.baloon_monsters), 0)
        self.assertEqual(len(self.game.shadow_monsters), 0)
        self.assertEqual(len(self.game.chaser_monsters), 0)
        self.assertEqual(len(self.game.queue_of_bombs), 0)
        self.assertEqual(len(self.game.queue_of_explosions), 0)
        self.assertEqual(self.game.bombs_pops, 0)
        self.assertEqual(self.game.explosions_pops, 0)
        self.assertFalse(self.game.hero.is_boost_picked)
        self.assertFalse(self.game.hero.is_game_won)
        self.assertFalse(self.game.hero.buddy_exist)
        self.assertFalse(self.game.is_boost_hider_broken)
        self.assertFalse(self.game.is_exit_hider_broken)

    def test_correct_saves(self):
        self.game.make_save()
        fs = open('saves/Bomberman {}.txt'.format(
                                          self.game.last_save_time), 'r')
        result = fs.read()
        fs.close()
        self.assertEqual(result, '1 3 0 5 0 0 1 1 0')
        os.remove('saves/Bomberman {}.txt'.format(self.game.last_save_time))


if __name__ == '__main__':
    unittest.main()
