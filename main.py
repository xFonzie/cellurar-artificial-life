from environment.environment import Environment
from environment.config import *
import arcade

def main():
    """ Main function - starting point to the program """
    window = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1 / 30)
    window.center_window()
    arcade.run()

if __name__ == "__main__":
    main()