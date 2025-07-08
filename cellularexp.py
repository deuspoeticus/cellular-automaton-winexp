# cellular automaton on windows explorer
# by deuspoeticus
#
# made for genuary 2025 #7: "Use software that is not intended to create art or images."

from PIL import Image
import os

grid_size = 25
cell_size = 512 
generations = 1
live_color = (0, 0, 0)
dead_color = (255, 255, 255)

def create_initial_grid(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i in range(grid_size):
        for j in range(grid_size):
            color = live_color if (i + j) % 9 == 0 else dead_color
            img = Image.new('RGB', (cell_size, cell_size), color)
            img.save(f"{folder}/cell_{i}_{j}.png")

def get_cell_color(folder, x, y):
    try:
        img = Image.open(f"{folder}/cell_{x}_{y}.png")
        return img.getpixel((0, 0))
    except FileNotFoundError:
        return dead_color

def count_live_neighbors(folder, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    live_neighbors = 0
    for dx, dy in directions:
        neighbor_color = get_cell_color(folder, x + dx, y + dy)
        if neighbor_color == live_color:
            live_neighbors += 1
    return live_neighbors

# symmetry rule
def apply_rules(folder, next_folder):
    if not os.path.exists(next_folder):
        os.makedirs(next_folder)
    for i in range(grid_size):
        for j in range(grid_size):
            current_color = get_cell_color(folder, i, j)
            live_neighbors = count_live_neighbors(folder, i, j)
            if live_neighbors % 2 == 1:  # odd
                new_color = live_color if current_color == dead_color else dead_color
            else:  # even
                new_color = current_color
            new_img = Image.new('RGB', (cell_size, cell_size), new_color)
            new_img.save(f"{folder}/cell_{i}_{j}.png")

current_folder = "generation_0"
create_initial_grid(current_folder)
for gen in range(1, generations + 1):
    next_folder = f"generation_{gen}"
    apply_rules(current_folder, next_folder)
    current_folder = next_folder
