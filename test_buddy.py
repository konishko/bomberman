import unittest
import main
import buddy
import blocks
import bomb
import monsters
from config_entity import WIDTH


class TestBuddy(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()
        self.game.start()
        self.game.hero.buddy_exist = True
        self.game.buddy = buddy.Buddy(WIDTH, WIDTH)

    def test_collide_with_wall(self):
        wall = blocks.Platform(2 * WIDTH, WIDTH)
        self.game.platforms.append(wall)
        self.game.buddy.update(False, True, False, False, self.game.platforms)
        self.assertEqual(WIDTH, self.game.buddy.rect.x)

    def test_collide_with_monster(self):
        monster = monsters.Monster(2 * WIDTH, WIDTH)
        self.game.platforms.append(monster)
        self.game.buddy.update(False, True, False, False, self.game.platforms)
        self.assertTrue(self.game.buddy.dying)

    def test_collide_with_explosion(self):
        explosion = bomb.Explosion(2 * WIDTH, WIDTH, self.game.platforms,
                                   False, self.game.entities, 1)
        self.game.platforms.append(explosion)
        self.game.buddy.update(False, False, False, False, self.game.platforms)
        self.assertTrue(self.game.buddy.dying)

    def test_can_buddy_die(self):
        self.game.buddy.dying = True
        self.game.buddy.time_of_death = 0
        self.game.buddy.update(False, False, False, False, self.game.platforms)
        self.assertTrue(self.game.buddy.died)

    def test_can_buddy_spawn(self):
        self.game.buddy.spawning = True
        self.game.buddy.time_of_spawning = 0
        self.game.buddy.update(False, False, False, False, self.game.platforms)
        self.assertFalse(self.game.buddy.spawning)

    def test_can_buddy_deleting(self):
        self.game.buddy.deleting = True
        self.game.buddy.time_of_deleting = 0
        self.game.buddy.update(False, False, False, False, self.game.platforms)
        self.assertTrue(self.game.buddy.deleted)

    def test_spawn_buddy(self):
        self.game.spawn_buddy()
        self.assertTrue(self.game.hero.buddy_exist)


if __name__ == '__main__':
    unittest.main()
