import random
import time

from m2mlearning.games.DisplayState import DisplayState
from m2mlearning.games.awjuliani.GridWorld import GridWorld

def main():
    game = GridWorld(board_size=[5,5])
    action_space_size = game.action_space_size()
    ds = DisplayState()

    for game_idx in range(10):
        print("*" * 100)
        print("New game")
        print("*" * 100)
        state = game.reset()
        ds.render(state)

        game_done = False
        while not game_done:
            action = random.randrange(action_space_size)
            print("New action [%d]" % action)
            state, reward, game_done, info = game.step(action)
            print("Reward [%s]" % reward)
            ds.render(state)

if __name__ == "__main__":
    main()
