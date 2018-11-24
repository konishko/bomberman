import unittest
import main
import monsters
import boosts
import bomb
import blocks
from config_entity import WIDTH


class TestHero(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_collide_with_wall(self):
        wall = blocks.Platform(2 * WIDTH, WIDTH)
        self.game.platforms.append(wall)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertEqual(WIDTH, self.game.hero.rect.x)

    def test_collide_with_monster(self):
        monster = monsters.Monster(2 * WIDTH, WIDTH)
        self.game.platforms.append(monster)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertTrue(self.game.hero.dying)

    def test_collide_with_explosion(self):
        explosion = bomb.Explosion(2 * WIDTH, WIDTH, self.game.platforms,
                                   False, self.game.entities, 1)
        self.game.platforms.append(explosion)
        self.game.hero.update(False, False, False, False, self.game.platforms)
        self.assertTrue(self.game.hero.dying)

    def test_can_hero_die(self):
        self.game.hero.dying = True
        self.game.hero.time_of_death = 0
        self.game.hero.update(False, False, False, False, self.game.platforms)
        self.assertTrue(self.game.hero.reload)

    def test_earning_scores(self):
        baloon = monsters.Baloon(0, 0)
        self.game.add_sprite(baloon)
        self.game.baloon_monsters.append(baloon)
        shadow = monsters.Shadow(0, 0)
        self.game.add_sprite(shadow)
        self.game.shadow_monsters.append(shadow)
        chaser = monsters.Chaser(0, 0)
        self.game.add_sprite(chaser)
        self.game.chaser_monsters.append(chaser)

        baloon.dead = True
        shadow.dead = True
        chaser.dead = True

        self.game.monsters_update()
        self.assertEqual(400, self.game.hero.scores)

    def test_many_bombs_boost(self):
        boost = boosts.Many_Bombs_Boost(2 * WIDTH, WIDTH)
        self.game.platforms.append(boost)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertEqual(self.game.hero.max_count_of_bombs, 2)

    def test_remote_bombs_boost(self):
        boost = boosts.Remote_Bombs_Boost(2 * WIDTH, WIDTH)
        self.game.platforms.append(boost)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertTrue(self.game.hero.remote_bombs_boost)

    def test_strength_up(self):
        boost = boosts.Strength_Up(2 * WIDTH, WIDTH)
        self.game.platforms.append(boost)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertEqual(self.game.hero.strength_of_bombs, 2)

    def test_additional_life(self):
        boost = boosts.Additional_Life(2 * WIDTH, WIDTH)
        self.game.platforms.append(boost)
        self.game.hero.update(False, True, False, False, self.game.platforms)
        self.assertEqual(self.game.hero.lifes, 4)


if __name__ == '__main__':
    unittest.main()
