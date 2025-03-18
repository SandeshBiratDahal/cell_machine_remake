from initializer import *
from grid import Grid
from sloader import get_save_string, load_from_string

def main():
    grid = Grid()
    gameloop = Gameloop()
    user = User()

    while True:
        gameloop.tick += 1
        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: gameloop.autoplay = not gameloop.autoplay
                elif event.key == pg.K_RETURN: grid.update_grid()
                elif event.key == pg.K_RIGHTBRACKET: user.cycle_cells(1)
                elif event.key == pg.K_LEFTBRACKET: user.cycle_cells(-1)

                elif event.key == pg.K_s:
                    print("Saved the current state!")
                    user.saved_grid = get_save_string(grid)
                elif event.key == pg.K_l:
                    print("Loaded the saved state!")
                    grid = load_from_string(user.saved_grid)

            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:
                    grid.add_cell(
                        mouse[0] // grid.cell_size, mouse[1] // grid.cell_size, user.get_current()
                    )
                elif event.button == 3:
                    loc = mouse[0] // grid.cell_size, mouse[1] // grid.cell_size
                    grid.get_cell(*loc).direction = cycle_direction(grid.get_cell(*loc).direction)

        scr.fill((0, 0, 0))
        if gameloop.autoplay and not gameloop.tick % 10: grid.update_grid()
        grid.render(scr)
        user.preview_placement(scr, mouse)
        clock.tick(60)
        pg.display.flip()

class User:
    def __init__(self):
        self.saved_grid = None
        self.cell_size = 50
        self.currently_holding = 0
        self.cells = [
            "regular", "mover", "duplicater", "rotater", "immovable", "slide", "destroyer", "fungal"
        ]
        self.cell_sprites = [
            pg.image.load(f"assets/{image}.png") for image in self.cells
        ]

        self.cell_sprites = [
            pg.transform.scale(sprite, (self.cell_size, self.cell_size)) for sprite in self.cell_sprites
        ]

        for sprite in self.cell_sprites: sprite.set_alpha(100)

    def cycle_cells(self, increment: int):
        self.currently_holding += increment
        if self.currently_holding >= len(self.cells): self.currently_holding = 0
        elif self.currently_holding < 0: self.currently_holding = len(self.cells) - 1
    
    def preview_placement(self, surf: pg.Surface, mouse: tuple):
        
        surf.blit(
            self.cell_sprites[self.currently_holding], (mouse[0] // self.cell_size * self.cell_size, mouse[1] // self.cell_size * self.cell_size)
        )
    
    def get_current(self): return self.cells[self.currently_holding]

class Gameloop:
    def __init__(self):
        self.tick = 0
        self.autoplay = False


def cycle_direction(direction: str):
    directions = "urdl"

    index = directions.index(direction)
    index += 1

    if index >= len(directions): index = 0
    return directions[index]

if __name__ == "__main__":
    main()