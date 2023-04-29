import arcade
from Environment.config import *
import random

def create_grids():
    """
    Create a 2D and 1D grid of sprites. We use the 1D SpriteList for drawing,
    and the 2D list for accessing via grid. Both lists point to the same set of
    sprites.
    """
    # One dimensional list of all sprites in the two-dimensional sprite list
    grid_sprites_one_dim = arcade.SpriteList()

    # This will be a two-dimensional grid of sprites to mirror the two
    # dimensional grid of numbers. This points to the SAME sprites that are
    # in grid_sprite_list, just in a 2d manner.
    grid_sprites_two_dim = []

    # Create a list of sprites to represent each grid location
    for row in range(ROW_COUNT):
        grid_sprites_two_dim.append([])

        for column in range(COLUMN_COUNT):

            # Make the sprite as a soft circle
            sprite = arcade.SpriteSolidColor(CELL_WIDTH, CELL_HEIGHT, ALIVE_COLOR)

            # Position the sprite
            x = column * (CELL_WIDTH + CELL_MARGIN) + (CELL_WIDTH / 2 + CELL_MARGIN)
            y = row * (CELL_HEIGHT + CELL_MARGIN) + (CELL_HEIGHT / 2 + CELL_MARGIN)
            sprite.center_x = x
            sprite.center_y = y

            # Add the sprite to both lists
            grid_sprites_one_dim.append(sprite)
            grid_sprites_two_dim[row].append(sprite)

    return grid_sprites_one_dim, grid_sprites_two_dim


def randomize_grid(grid: arcade.SpriteList):
    """ Randomize the grid to alive/dead """
    for cell in grid:
        pick = random.randrange(2)
        if pick:
            cell.alpha = ALPHA_ON
        else:
            cell.alpha = ALPHA_OFF



class Environment(arcade.Window):
    """
    Main application class
    """

    def __init__(self, width: int = 800, height: int = 600, title: str | None = 'Arcade Window', 
                 fullscreen: bool = False, resizable: bool = False, update_rate: float | None = 1 / 60):
        
        super().__init__(width, height, title, fullscreen, resizable, update_rate)
        
        self.background_color = BACKGROUND_COLOR

        # We need two layers. One holds the current state of our grid, the other
        # holds the next frame's state. We flip back and forth between the two.
        grid_sprites_one_dim1, grid_sprites_two_dim1 = create_grids()
        grid_sprites_one_dim2, grid_sprites_two_dim2 = create_grids()

        self.layers_grid_sprites_one_dim = [grid_sprites_one_dim1, grid_sprites_one_dim2]
        self.layers_grid_sprites_two_dim = [grid_sprites_two_dim1, grid_sprites_two_dim2]

        self.cur_layer = 0
        self.paused = False
        self.step = False
        self.i = 0
        randomize_grid(self.layers_grid_sprites_one_dim[0])

    def on_draw(self):
        """ Render the screen. """
        # Clear all pixels in the window
        self.clear()
        self.layers_grid_sprites_one_dim[0].draw()

    def on_update(self, delta_time: float):
        """ Update the grid """
        pass
    
    def on_key_press(self, symbol: int, modifiers: int):
        # restart on 'r'
        if symbol == arcade.key.R:
            randomize_grid(self.layers_grid_sprites_one_dim[0])
            print('Restarting')
        # pause on 'spacebar'
        elif symbol == arcade.key.SPACE:
            self.paused = not self.paused
        # next frame on 'n'
        elif symbol == arcade.key.N:
            print(self.i)
            self.step = True




    