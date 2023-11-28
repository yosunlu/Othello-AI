from typing import Optional

import othello
import time

class Simulation(othello.Referee):
    def cb_post_move(self, player: othello.Player,
                     action: Optional[othello.Action]) -> None:
        if action is None:
            print(f'{player} skips')
        else:
            print(f'{player} plays {action.repr}')

        for row in self.game.state.board.repr:
            print(row)

        print()

    def cb_game_end(self) -> None:
        if self.game.get_conclusion() is othello.DRAW:
            print('Draw!')
        else:
            print(f'{self.game.get_conclusion()} wins!')
            print(f'It wins {self.game.state.get_difference()} chess pieces.')
        print(f'It takes {self.n_step} steps.')
        print(f'Player.BLACK for {self.time_black} seconds.')
        print(f'Player.WHITE for {self.time_white} seconds.')