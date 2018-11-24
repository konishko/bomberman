# Игра "Bomberman"
Версия 1.01

Автор: Смольянов Данил Леонидович

## Описание
Данное приложение является реализацией игры "Bomberman".


## Требования
* Python версии не ниже 3.4
* Pygame версии не ниже 1.9.3
* Pyganim версии не ниже 0.9.2


## Состав
* Графическая версия: `main.py`
* Файлы настроек: `config_entity.py`
                  `config_bomb.py`
                  `config_buddy.py`
                  `config_hero.py`
                  `config_monsters.py`
                  `config_window.py`
                  `config_main.py`
                  `config_level_generator.py`
* Модули: `monsters.py`
          `hero.py`
          `buddy.py`
          `menus.py`
          `bomb.py`
          `blocks.py`
          `boosts.py`
* Изображения: `images/`
* Шрифты: `fonts/`
* Сохранения: `saves/`
* Тесты: `tests_buddy.py`
         `tests_bomb.py`
         `tests_camera.py`
         `tests_explosion.py`
         `tests_generator.py`
         `tests_hero.py`
         `tests_keyboard.py`
         `tests_menus.py`
         `tests_monsters.py`
         `tests_utility.py`


## Графическая версия

Пример запуска: `./python main.py`


## Подробности реализации
Модули, отвечающие за логику игры, расположены в пакете Bomberman_mp.
В основе всего лежит класс `Game`, реализующий хранение игрового поля и его изменение.
Остальные модули хранят реализацию различных обьектов встречающихся в игре.
Есть возможности: 
*  сохранять прогресс
*  играть вдвоем по технологии Hotseat
*  улучшать персонажа
*  использовать чит-коды
*  ставить игру на паузу

На данные модули написаны тесты, их можно найти в `./`.
Покрытие по строкам составляет около 81%:

    Name                        Stmts   Miss  Cover
    -----------------------------------------------
    blocks.py                      20      0   100%
    bomb.py                       179     26    85%
    boosts.py                      28      2    93%
    buddy.py                      126     12    90%
    hero.py                       149     18    88%
    levelgenerator.py             117     10    91%
    main.py                       412    137    67%
    menues.py                     173    112    35%
    monsters.py                   179     21    88%  
