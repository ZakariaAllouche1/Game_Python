from src.settings import SingletonMeta

class SpriteConfig:
    """Classe Settings utilisant le pattern Singleton."""
    def __init__(self, idle, movement, attacks, defenses, effects, dead):
        self.idle = idle
        self.movement = movement
        self.attacks = attacks
        self.defenses = defenses
        self.effects = effects
        self.dead = dead

    def get_indexes(self, state):
        if state == 'idle':
            return self.idle
        elif state == 'movement':
            return self.movement
        elif state == 'attacks':
            return self.attacks
        elif state == 'defenses':
            return self.defenses
        elif state == 'dead':
            return self.dead

    def get_effects(self, type):
        if type in self.effects.keys():
            return self.effects[type]
        return None

# gray = SpriteConfig({'idle' : [8, 9]}, {'right': [16, 17, 18, 19, 20, 21],
#                                'jump': [13, 22, 14]}, {'Sword of destiny': [4, 5, 6, 7], 'Titania attack': [8, 9, 10, 11, 22, 14]},
#                     {'Fairy aura': [0, 1, 2, 3], 'Diamond shield': [6, 7]}, {'Titania attack': (5, 6),
#             'Sword of destiny': (5, 2)}, {'dead' : [15]})
# er = {'sprite' : {
#             'idle': [6, 7],
#             'Sword of destiny': [4, 5, 6, 7],
#             'Titania attack': [8, 9, 10, 11, 22, 14],
#             'Fairy aura': [0, 1, 2, 3],
#             'Diamond shield': [6, 7]
#         },
#         'effects' : {
#             'attaque_1': ('attaque_titania', 5, 6),
#             'attaque_2': ('sword_attack', 5, 2),
#         },
#         'movements' : {
#             'right': [16, 17, 18, 19, 20, 21],
#             'saut': [13, 22, 14],
#         },
#         'mort': [15]
#     }