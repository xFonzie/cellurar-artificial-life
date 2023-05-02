"""
Description of the Organism class
"""

from typing import Optional
# from arcade import Texture
import arcade
# pylint: disable=import-error
from config import (
    CELL_HEIGHT,
    CELL_MARGIN,
    CELL_WIDTH,
    ORGANISM_ENERGY,
    MUTATION_RATE,
    COLUMN_COUNT,
    ROW_COUNT,
    REPRODUCTION_ENERGY,
)
from brain import Brain


class Organism(arcade.SpriteSolidColor):
    """
    Organism is a single entity that tries to survive in te environment.
    """
    brain = ...

    def __init__(self, x: int, y: int, parent: Optional["Organism"] = None):
        """
        Standard constructor for the Organism class

        Parameters:
            x: x coordinate of the organism
            y: y coordinate of the organism
            parent: a parent of the organism
        """
        self.brain = Brain(genome=parent.brain.mutate(MUTATION_RATE) if parent else None)
        super().__init__(CELL_WIDTH, CELL_HEIGHT, self.brain.genome_color())
        self.energy = ORGANISM_ENERGY
        self.age = 0
        self.alive = True

        self.center_x = x * (CELL_WIDTH + CELL_MARGIN) + CELL_WIDTH // 2 + CELL_MARGIN
        self.center_y = y * (CELL_HEIGHT + CELL_MARGIN) + CELL_HEIGHT // 2 + CELL_MARGIN

        self.pos = x, y  # TODO если ты уже поменял центр координат, зачем обновлять pos?

    def kill(self):
        self.alive = False

    # pylint: disable=invalid-name
    def move_to(self, x, y):
        """
        The organism moves to another cell
        """
        if x < 0 or x >= COLUMN_COUNT or y < 0 or y >= ROW_COUNT:
            return

        self.pos = x, y

        self.center_x = x * (CELL_WIDTH + CELL_MARGIN) + CELL_WIDTH // 2 + CELL_MARGIN
        self.center_y = y * (CELL_HEIGHT + CELL_MARGIN) + CELL_HEIGHT // 2 + CELL_MARGIN

    def reproduce(self):
        """
        The organism makes a child
        """
        if self.energy < REPRODUCTION_ENERGY:
            return None
        child = Organism(*self.pos)  # TODO судя точно не надо родителя?
        child.energy = self.energy / 2
        self.energy = self.energy / 2
        return child

    # TODO update() с другими аргументами переписывается
    def org_update(self, observation: list) -> Optional["Organism"]:
        """
        The organism makes a step

        Returns:
            A child if it's created, otherwise None
        """
        self.age += 1
        self.energy -= 1
        if self.energy <= 0:
            self.kill()

        state = (
            list(observation[:8]) +  # TODO раньше было observation[:9], что я не учел?
            [self.brain.difference(org.brain) if org else 0 for org in observation[9: 17]] +
            [observation[17], self.energy]
        )

        action = self.brain.get_action(state)

        match action:
            case 0:
                self.move_to(self.pos[0], self.pos[1] + 1)
            case 1:
                self.move_to(self.pos[0], self.pos[1] - 1)
            case 2:
                self.move_to(self.pos[0] - 1, self.pos[1])
            case 3:
                self.move_to(self.pos[0] + 1, self.pos[1])
            case 4:
                self.energy += observation[4]
                print("ate")
            case 5:
                for i in range(9, 17):
                    if observation[i] is not None:
                        self.energy += observation[i].energy
                        observation[i].kill()
            case 6:
                child = self.reproduce()
                if child is not None:
                    return child
        return None