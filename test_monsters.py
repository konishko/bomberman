import unittest
import main
import monsters
import bomb
from config_entity import WIDTH
from config_monsters import MOVE_SPEED


class TestMonsters(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()

    def test_collide_with_bomb(self):
        monster = monsters.Monster(WIDTH, WIDTH)
        my_bomb = bomb.Bomb(2 * WIDTH, WIDTH, 1)
        self.game.platforms.append(monster)
        self.game.platforms.append(my_bomb)
        monster.rect.x += 1
        monster.collide(1, 0, self.game.platforms)
        self.assertEqual(WIDTH, monster.rect.x)

    def test_collide_with_explosion(self):
        monster = monsters.Monster(WIDTH, WIDTH)
        explosion = bomb.Explosion(2 * WIDTH, WIDTH, self.game.platforms,
                                   False, self.game.entities, 1)
        self.game.platforms.append(monster)
        self.game.platforms.append(explosion)
        monster.rect.x += 1
        monster.collide(1, 0, self.game.platforms)
        self.assertTrue(monster.dying)

    def test_can_baloon_walk(self):
        baloon = monsters.Baloon(2 * WIDTH, 2 * WIDTH)
        baloon.update(self.game.platforms)
        init_pos = (2 * WIDTH, 2 * WIDTH)
        end_pos = (baloon.rect.x, baloon.rect.y)
        self.assertNotEqual(init_pos, end_pos)

    def test_can_shadow_copy_hero(self):
        shadow = monsters.Shadow(WIDTH, WIDTH)
        shadow.update(False, True, False, True, self.game.platforms)
        target_pos = (WIDTH + MOVE_SPEED, WIDTH + MOVE_SPEED)
        end_pos = (shadow.rect.x, shadow.rect.y)
        self.assertEqual(target_pos, end_pos)

    def test_can_chaser_chase_hero(self):
        chaser = monsters.Chaser(2 * WIDTH, 2 * WIDTH)
        chaser.update(self.game.hero.rect.x, self.game.hero.rect.y,
                      self.game.platforms)
        target_pos = (2 * WIDTH - MOVE_SPEED, 2 * WIDTH - MOVE_SPEED)
        end_pos = (chaser.rect.x, chaser.rect.y)
        self.assertEqual(target_pos, end_pos)


if __name__ == '__main__':
    unittest.main()
