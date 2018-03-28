"""
GUI / Window displaying the state
"""

from matplotlib import pyplot as plt
import numpy as np

class DisplayState(object):
    """Class to display the state

    This class uses the mathplotlib to open a window
    and displays the current state.
    """

    def __init__(self):
        plt.ion()
        plt.show()

    def render(self, state):
        plt.imshow(state, interpolation='none')
        plt.draw()
        plt.pause(0.001)
