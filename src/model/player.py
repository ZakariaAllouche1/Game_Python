class Player:

    def __init__(self, name):
        self.name = name
        self.units = {}
        self.selected_unit = None
        self.selected_attack = None

    def select_unit(self):
        if self.units is not None:
            for unit in self.units.values():
                if unit.is_selected:
                    self.selected_unit = unit

    def __str__(self):
        return f"Player -- [Name: {self.name} | Units: {self.units}]"