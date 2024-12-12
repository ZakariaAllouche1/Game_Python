from src.model.attack import Attack
from src.model.defense import Defense
from src.model.unit import Unit
from src.view.sprites_config import SpriteConfig


class HeroFactory:

    @staticmethod
    def sprite_config(name):
        if name == 'Erza':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [14, 6, 7]},
                         {'Sword of destiny': [4, 5, 6, 7], 'Titania attack': [8, 9, 10, 11, 22, 14]},
                         {'Fairy aura': [0, 1, 2, 3], 'Diamond shield': [6, 7]},
                         {'Titania attack': (5, 6, True, 190), 'Diamond shield': (5, 5, False, 190), 'Fairy aura': (5, 4, False, 190),
                          'Sword of destiny': (5, 2, True, 120)}, {'dead': [15]})

        if name == 'Gray':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 6, 7]},
                                {'Frozen swords': [14, 4, 5, 6], 'Icy destruction': [8, 9, 10, 11, 22, 14]},
                                {'Ice shield': [7, 8, 9, 10], 'Absolute ice': [6, 7]},
                                {'Icy destruction': (5, 5, True, 190), 'Frozen swords': (5, 4, True, 190),
                                 'Absolute ice': (5, 2, False, 190)}, {'dead': [15]})

        if name == 'Natsu':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 6, 7]},
                                {"Fire dragon's iron fist": [14, 4, 5], "Fire dragon's roar": [8, 9, 10, 14]},
                                {'Protective flame': [0, 1, 2, 3], 'Flame envelope': [6, 7]},
                                {"Fire dragon's iron fist": (5, 3, True, 190), "Fire dragon's roar": (5, 2, True, 180),
                                 'Flame envelope': (5, 5, False, 190)}, {'dead': [15]})

        if name == 'Kansuke':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 13, 14]},
                                 {'Infinite light': [4, 5, 6, 7], 'Holy light': [8, 22, 9, 10]},
                                 {'Dissipative clarity': [0, 1, 2, 3], 'Protective ray': [0, 1, 2, 3]},
                                 {'Holy light': (5, 5, True, 190), 'Protective ray': (5, 4, False, 190),
                                  'Infinite light': (5, 6, True, 190), 'Dissipative clarity': (5, 6, False, 190)}, {'dead': [15]})

        if name == 'Gowther':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 14]},
                                 {'Darkness flare bomb': [8, 9, 10], 'Obscurity tentacles': [0, 1, 2, 3]},
                                 {'Shadow rune shield': [3, 4, 5], 'Demon aura': [0, 1, 2, 3]},
                                 {'Darkness flare bomb': (5, 5, True, 190), 'Shadow rune shield': (5, 6, False, 190),
                                  'Obscurity tentacles': (5, 5, True, 190), 'Demon aura': (5, 6, False, 190)}, {'dead': [15]})

        if name == 'Heisuke':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 14]},
                                   {'Thunderball': [14, 4, 5], 'Lightning saber': [8, 9, 10]},
                                   {'Regenerative lightning': [0, 1, 2, 3, 14], 'Lightning strike': [0, 1, 2, 3]},
                                   {'Thunderball': (5, 2, True, 190), 'Lightning saber': (5, 3, True, 190),
                                    'Regenerative lightning': (3, 1, False, 190), 'Lightning strike': (5, 6, False, 190)},
                                   {'dead': [15]})


    @staticmethod
    def erza(x, y, team):
        erza = Unit("Erza", x, y, 100, team, 10)

        erza.add_competence(Attack("Sword of destiny", 30, (2, 2, 0), 10, (4, 3, 0), None), "attack")
        erza.add_competence(Attack("Titania attack", 45, (3, 2, 0), 10, (5, 4, 0), None), "attack")

        erza.add_competence(Defense("Fairy aura", 20, (1, 1, 0), 10, (0, 0, 0)), "defense")
        erza.add_competence(Defense("Diamond shield", 35, (2, 1, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(erza.name)

        return erza, sprite_conf

    @staticmethod
    def gray(x, y, team):
        gray = Unit("Gray", x, y, 100, team, 10)

        gray.add_competence(Attack("Frozen swords", 20, (2, 2, 0), 10, (4, 3, 0), None), "attack")
        gray.add_competence(Attack("Icy destruction", 40, (3, 2, 0), 10, (5, 4, 0), None), "attack")

        gray.add_competence(Defense("Ice shield", 15, (1, 1, 0), 10, (0, 0, 0)), "defense")
        gray.add_competence(Defense("Absolute ice", 30, (2, 2, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(gray.name)

        return gray, sprite_conf
    
    @staticmethod
    def Natsu(x, y, team):
        Natsu = Unit("Natsu", x, y, 130, team, 10)

        Natsu.add_competence(Attack("Fire dragon's iron fist", 35, (3, 3, 0), 10, (4, 4, 0), None), "attack")
        Natsu.add_competence(Attack("Fire dragon's roar", 50, (5, 3, 0), 10, (5, 4, 0), None), "attack")

        Natsu.add_competence(Defense("Protective flame", 30, (1, 1, 0), 10, (0, 0, 0)), "defense")
        Natsu.add_competence(Defense("Flame envelope", 20, (2, 1, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(Natsu.name)

        return Natsu, sprite_conf
    
    @staticmethod
    def Kansuke(x, y, team):
        Kansuke = Unit("Kansuke", x, y, 110, team, 10)

        Kansuke.add_competence(Attack("Infinite ligh", 25, (4, 4, 0), 10, (4, 4, 0), None), "attack")
        Kansuke.add_competence(Attack("Holy light", 55, (3, 3, 0), 10, (3, 4, 0), None), "attack")

        Kansuke.add_competence(Defense("Dissipative clarity", 20, (1, 1, 0), 10, (0, 0, 0)), "defense")
        Kansuke.add_competence(Defense("Protective ray", 35, (2, 2, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(Kansuke.name)

        return Kansuke, sprite_conf
    
    @staticmethod
    def Gowther(x, y, team):
        Gowther = Unit("Gowther", x, y, 120, team, 10)

        Gowther.add_competence(Attack("Darkness flare bomb", 40, (3, 3, 0), 10, (5, 5, 0), None), "attack")
        Gowther.add_competence(Attack("Obscurity tentacles", 60, (2, 2, 0), 10, (2, 2, 0), None), "attack")

        Gowther.add_competence(Defense("Shadow rune shield", 35, (1, 1, 0), 10, (0, 0, 0)), "defense")
        Gowther.add_competence(Defense("Demon aura", 20, (2, 2, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(Gowther.name)

        return Gowther, sprite_conf
    
    @staticmethod
    def Heisuke(x, y, team):
        Heisuke = Unit("Heisuke", x, y, 140, team, 10)

        Heisuke.add_competence(Attack("Thunderball", 45, (4, 4, 0), 10, (5, 5, 0), None), "attack")
        Heisuke.add_competence(Attack("Lightning sabe", 50, (3, 3, 0), 10, (4, 4, 0), None), "attack")

        Heisuke.add_competence(Defense("Regenerative lightning", 15, (1, 1, 0), 10, (0, 0, 0)), "defense")
        Heisuke.add_competence(Defense("Lightning strike", 10, (2, 2, 0), 10, (0, 0, 0)), "defense")

        sprite_conf = HeroFactory.sprite_config(Heisuke.name)

        return Heisuke, sprite_conf