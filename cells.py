import pygame as pg

class Cell:
    auto_id = 0
    def __init__(self, x: int, y: int, type: str = "regular", size: int = 50, direction: str = "u"):
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.base_sprite = pg.image.load(f"assets/{type}.png").convert_alpha()
        self.base_sprite = pg.transform.scale(self.base_sprite, (self.size, self.size))
        self.sprites = {
            "u": self.base_sprite,
            "r": pg.transform.rotate(self.base_sprite, -90),
            "l": pg.transform.rotate(self.base_sprite, 90),
            "d": pg.transform.rotate(self.base_sprite, 180)
        }
        self.type = type
        self.id = Cell.auto_id
        Cell.auto_id += 1

    def render(self, surf: pg.Surface):
        surf.blit(
            self.sprites[self.direction], (self.x * self.size, self.y * self.size)
        )

class Mover(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "mover", direction=direction)

class Rotater(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "rotater", direction=direction)

class Immovable(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "immovable", direction=direction)

class Regular(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "regular", direction=direction)

class Duplicater(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "duplicater", direction=direction)

class Destroyer(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "destroyer", direction=direction)
    
class Slide(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "slide", direction=direction)

class Fungal(Cell):
    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x, y, "fungal", direction=direction)