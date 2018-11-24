import unittest
import main
import levelgenerator


class TestLevelGenerator(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.level_generator = levelgenerator.LevelGenerator(self.game)
        self.game.start()

    def test_booster_choose(self):
        self.level_generator.choose_booster()
        self.assertTrue(0 <= self.level_generator.booster <= 3)

    def test_make_exit_hider(self):
        self.level_generator.make_exit_hider()
        exit_hider_exist = False
        for p in self.game.platforms:
            if p == self.game.exit_hider:
                exit_hider_exist = True
        self.assertTrue(exit_hider_exist)

    def test_make_boost_hider(self):
        self.level_generator.choose_booster()
        self.level_generator.make_booster_hider()
        boost_hider_exist = False
        for p in self.game.platforms:
            if p == self.game.boost_hider:
                boost_hider_exist = True
        self.assertTrue(boost_hider_exist)

    def test_make_hard_platforms(self):
        self.level_generator.make_hard_platforms()
        self.assertEqual(len(self.game.platforms), 152)

    def test_make_monsters(self):
        self.level_generator.make_monsters()
        self.assertEqual(len(self.game.baloon_monsters)
                         + len(self.game.shadow_monsters)
                         + len(self.game.chaser_monsters), 4)

    def test_make_monsters_high_level(self):
        self.game.hero.level = 100
        self.level_generator.make_monsters()
        self.assertEqual(len(self.game.baloon_monsters)
                         + len(self.game.shadow_monsters)
                         + len(self.game.chaser_monsters), 14)

    def test_make_simple_platforms(self):
        self.level_generator.make_simple_platforms()
        self.assertEqual(len(self.game.platforms), 59)


if __name__ == '__main__':
    unittest.main()
