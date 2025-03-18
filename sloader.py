from grid import Grid
from cells import Cell

def get_save_string(grid: Grid):
    string = ""
    cell: Cell
    for pos, cell in grid.placed_cells.items():
        string += f"{pos[0]},{pos[1]},{cell.type},{cell.direction}~"
    return string[:len(string) - 1]

def load_from_string(string: str):
    grid = Grid()
    Grid.placed_cells = {}
    cells = string.split("~")
    for cell in cells:
        properties = cell.split(",")
        grid.add_cell(
            int(properties[0]), int(properties[1]), properties[2], properties[3]
        )
    return grid