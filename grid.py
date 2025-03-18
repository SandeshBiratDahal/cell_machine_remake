from cells import *
import copy

class Grid:
    placed_cells = {}
    def __init__(self, cell_size: int = 50):
        self.cell_size = cell_size
        self.movers = []
        self.duplicaters = []
        self.rotaters = []
        self.immovables = []
        self.regulars = []
        self.slides = []
        self.destroyers = []

    def add_cell(self, x: int, y: int, type: str, direction: str = "u"):
        currently_placed = None
        if type == "mover": 
            currently_placed = Mover(x, y, direction)
            self.movers.append(currently_placed)
        elif type == "rotater": 
            currently_placed = Rotater(x, y, direction)
            self.rotaters.append(currently_placed)
        elif type == "immovable": 
            currently_placed = Immovable(x, y, direction)
            self.immovables.append(currently_placed)
        elif type == "duplicater": 
            currently_placed = Duplicater(x, y, direction)
            self.duplicaters.append(currently_placed)
        elif type == "regular": 
            currently_placed = Regular(x, y, direction)
            self.regulars.append(currently_placed) 
        elif type == "slide": 
            currently_placed = Slide(x, y, direction)
            self.slides.append(currently_placed) 
        elif type == "destroyer":
            currently_placed = Destroyer(x, y, direction)
            self.destroyers.append(currently_placed)
        Grid.placed_cells[(x, y)] = currently_placed

    def render(self, surf: pg.Surface):
        mover: Mover
        rotater: Rotater
        immovable: Immovable
        duplicater: Duplicater
        regular: Regular
        slide: Slide
        destroyer: Destroyer
        for mover in self.movers: mover.render(surf)
        for rotater in self.rotaters: rotater.render(surf)
        for immovable in self.immovables: immovable.render(surf)
        for duplicater in self.duplicaters: duplicater.render(surf)
        for regular in self.regulars: regular.render(surf)
        for slide in self.slides: slide.render(surf)
        for destroyer in self.destroyers: destroyer.render(surf)

    def get_cell(self, x: int, y: int) -> Cell: return Grid.placed_cells.get((x, y))

    def update_grid(self):
        mover: Mover
        rotater: Rotater
        duplicater: Duplicater
        destroyer: Destroyer

        for destroyer in self.destroyers:
            match destroyer.direction:
                case "u":
                    current_cell = self.get_cell(destroyer.x, destroyer.y - 1)
                    if current_cell:
                        cell_id, cell_name = current_cell.id, current_cell.type
                        index = 0
                        while eval(f"self.{cell_name}s[{index}].id != {cell_id}"): index += 1
                        exec(f"self.{cell_name}s.pop({index})")
                        del Grid.placed_cells[(destroyer.x, destroyer.y - 1)]
                case "d":
                    current_cell = self.get_cell(destroyer.x, destroyer.y + 1)
                    if current_cell:
                        cell_id, cell_name = current_cell.id, current_cell.type
                        index = 0
                        while eval(f"self.{cell_name}s[{index}].id != {cell_id}"): index += 1
                        exec(f"self.{cell_name}s.pop({index})")
                        del Grid.placed_cells[(destroyer.x, destroyer.y + 1)]
                case "r":
                    current_cell = self.get_cell(destroyer.x + 1, destroyer.y)
                    if current_cell:
                        cell_id, cell_name = current_cell.id, current_cell.type
                        index = 0
                        while eval(f"self.{cell_name}s[{index}].id != {cell_id}"): index += 1
                        exec(f"self.{cell_name}s.pop({index})")
                        del Grid.placed_cells[(destroyer.x + 1, destroyer.y)]
                case "l":
                    current_cell = self.get_cell(destroyer.x - 1, destroyer.y)
                    if current_cell:
                        cell_id, cell_name = current_cell.id, current_cell.type
                        index = 0
                        while eval(f"self.{cell_name}s[{index}].id != {cell_id}"): index += 1
                        exec(f"self.{cell_name}s.pop({index})")
                        del Grid.placed_cells[(destroyer.x - 1, destroyer.y)]

        for mover in self.movers:
            movable = True
            number_of_blocks_ahead = 0
            match mover.direction:
                case "r":
                    while self.get_cell(mover.x + number_of_blocks_ahead + 1, mover.y): 
                        current_cell = self.get_cell(mover.x + number_of_blocks_ahead + 1, mover.y)
                        if current_cell.type == "immovable": movable = False
                        elif current_cell.type == "slide" and (current_cell.direction == "u" or current_cell.direction == "d"): movable = False
                        number_of_blocks_ahead += 1
                    if not movable: continue
                    for i in range(mover.x + number_of_blocks_ahead, mover.x, -1): 
                        current_cell = self.get_cell(i, mover.y)
                        current_cell.x += 1
                        Grid.placed_cells[(i, mover.y)] = None
                        Grid.placed_cells[(i + 1, mover.y)] = current_cell
                    Grid.placed_cells[(mover.x, mover.y)] = None
                    Grid.placed_cells[(mover.x + 1, mover.y)] = mover
                    mover.x += 1
                case "u":
                    while self.get_cell(mover.x, mover.y - number_of_blocks_ahead - 1): 
                        current_cell = self.get_cell(mover.x, mover.y - number_of_blocks_ahead - 1)
                        if current_cell.type == "immovable": movable = False
                        elif current_cell.type == "slide" and (current_cell.direction == "r" or current_cell.direction == "l"): movable = False
                        number_of_blocks_ahead += 1
                    if not movable: continue
                    for i in range(mover.y - number_of_blocks_ahead, mover.y): 
                        current_cell = self.get_cell(mover.x, i)
                        current_cell.y -= 1
                        Grid.placed_cells[(mover.x, i)] = None
                        Grid.placed_cells[(mover.x, i - 1)] = current_cell
                    Grid.placed_cells[(mover.x, mover.y)] = None
                    Grid.placed_cells[(mover.x, mover.y - 1)] = mover
                    mover.y -= 1
                case "l":
                    while self.get_cell(mover.x - number_of_blocks_ahead - 1, mover.y): 
                        current_cell = self.get_cell(mover.x - number_of_blocks_ahead - 1, mover.y)
                        if current_cell.type == "immovable": movable = False
                        elif current_cell.type == "slide" and (current_cell.direction == "u" or current_cell.direction == "d"): movable = False
                        number_of_blocks_ahead += 1
                    if not movable: continue
                    for i in range(mover.x - number_of_blocks_ahead, mover.x): 
                        current_cell = self.get_cell(i, mover.y)
                        current_cell.x -= 1
                        Grid.placed_cells[(i, mover.y)] = None
                        Grid.placed_cells[(i - 1, mover.y)] = current_cell
                    Grid.placed_cells[(mover.x, mover.y)] = None
                    Grid.placed_cells[(mover.x - 1, mover.y)] = mover
                    mover.x -= 1
                case "d":
                    while self.get_cell(mover.x, mover.y + number_of_blocks_ahead + 1): 
                        current_cell = self.get_cell(mover.x, mover.y + number_of_blocks_ahead + 1)
                        if current_cell.type == "immovable": movable = False
                        elif current_cell.type == "slide" and (current_cell.direction == "r" or current_cell.direction == "l"): movable = False
                        number_of_blocks_ahead += 1
                    if not movable: continue
                    for i in range(mover.y + number_of_blocks_ahead, mover.y, -1): 
                        current_cell = self.get_cell(mover.x, i)
                        current_cell.y += 1
                        Grid.placed_cells[(mover.x, i)] = None
                        Grid.placed_cells[(mover.x, i + 1)] = current_cell
                    Grid.placed_cells[(mover.x, mover.y)] = None
                    Grid.placed_cells[(mover.x, mover.y + 1)] = mover
                    mover.y += 1

        for duplicater in self.duplicaters:
            
            match duplicater.direction:
                case "u":
                    block_to_duplicate, location = self.get_cell(duplicater.x, duplicater.y + 1), (-100, -100)
                    if block_to_duplicate and not self.get_cell(duplicater.x, duplicater.y - 1): location = (duplicater.x, duplicater.y - 1)
                case "d":
                    block_to_duplicate, location = self.get_cell(duplicater.x, duplicater.y - 1), (-100, -100)
                    if block_to_duplicate and not self.get_cell(duplicater.x, duplicater.y + 1): location = (duplicater.x, duplicater.y + 1)
                case "r":
                    block_to_duplicate, location = self.get_cell(duplicater.x - 1, duplicater.y), (-100, -100)
                    if block_to_duplicate and not self.get_cell(duplicater.x + 1, duplicater.y): location = (duplicater.x + 1, duplicater.y)
                case "l":
                    block_to_duplicate, location = self.get_cell(duplicater.x + 1, duplicater.y + 1), (-100, -100)
                    if block_to_duplicate and not self.get_cell(duplicater.x - 1, duplicater.y): location = (duplicater.x - 1, duplicater.y)

            if location[0] != -100:
                new_copy_block = copy.copy(block_to_duplicate)
                new_copy_block.x, new_copy_block.y = location
                exec(
                    f"self.{block_to_duplicate.type}s.append(new_copy_block)"
                )
                Grid.placed_cells[location] = new_copy_block
                        
        for rotater in self.rotaters:
            neighbours = [
                self.get_cell(rotater.x - 1, rotater.y),
                self.get_cell(rotater.x + 1, rotater.y),
                self.get_cell(rotater.x, rotater.y - 1),
                self.get_cell(rotater.x, rotater.y + 1)
            ]
            for neighbour in neighbours: 
                if neighbour: neighbour.direction = rotater.direction