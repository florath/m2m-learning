"""
Abstract Base Class for Games that can be played with m2m-learning
"""
from abc import ABC


class BaseGame(ABC):
    """Defines common interface for all games"""

    def __init__(self, name):
        self.__name = name

    def shape(self):
        """Returns the shape status

        It looks that 84 x 84 x 1 is some kind of standard shape
        for this kind of task.
        """
        return (84, 84, 1)

    
