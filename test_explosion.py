import unittest
import main
import blocks
import bomb
import levelgenerator
from config_entity import WIDTH


class TestExplosion(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    @unittest.expectedFailure
    def test_appendages_break_walls(self):
        self.game.platforms.append(blocks.Platform(2 * WIDTH, WIDTH))
        self.game.platforms.append(blocks.Platform(WIDTH, 2 * WIDTH))
        self.game.platforms.append(blocks.Platform(3 * WIDTH, 2 * WIDTH))
        self.game.platforms.append(blocks.Platform(2 * WIDTH, 3 * WIDTH))
        explosion = bomb.Explosion(2 * WIDTH, 2 * WIDTH, self.game.platforms,
                                   False, self.game.entities, 1)
        self.game.platforms.append(explosion)
        self.assertEqual(len(explosion.appendages), 0)

    def test_are_boost_spawning(self):
        self.lvlgnrtr = levelgenerator.LevelGenerator(self.game)
        self.lvlgnrtr.choose_booster()
        self.lvlgnrtr.make_booster_hider()
        self.lvlgnrtr.make_exit_hider()
        self.game.platforms.clear()
        self.game.is_boost_hider_broken = True
        self.game.is_exit_hider_broken = True
        self.game.hiders_update()
        check_boost = check_exit = False
        for p in self.game.platforms:
            if p == self.game.boost:
                check_boost = True
            if p == self.game.exit:
                check_exit = True
        self.assertTrue(check_boost)
        self.assertTrue(check_exit)

    def test_can_explosion_be_ended(self):
        self.lvlgnrtr = levelgenerator.LevelGenerator(self.game)
        self.lvlgnrtr.choose_booster()
        self.lvlgnrtr.make_booster_hider()
        self.lvlgnrtr.make_exit_hider()
        explosion = bomb.Explosion(2 * WIDTH, 2 * WIDTH, self.game.platforms,
                                   False, self.game.entities, 1)
        self.game.queue_of_explosions.append(explosion)
        self.game.add_sprite(explosion)
        explosion.time_of_exploding = 0
        for appendage in explosion.appendages:
            appendage.time_of_exploding = 0
        self.game.explosions_update()
        check = True
        for p in self.game.platforms:
            if isinstance(p, bomb.Explosion):
                check = True
        self.assertTrue(check)


if __name__ == '__main__':
    unittest.main()
