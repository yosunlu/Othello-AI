from collections import defaultdict
from dataclasses import dataclass, field
from math import log, sqrt
import random
from typing import Optional

import othello
from gameplay import Simulation
import pdb


@dataclass(frozen=True)
class MCTSTreeData:
    """
    Data class that holds the win count and play count for a state in the MCTS.
    
    Attributes:
        win_count (float): Number of wins from the current state.
        play_count (int): Number of times the current state has been visited.
    
    Raises:
        ValueError: If win_count is less than 0, play_count is less than 0,
                    or win_count is greater than play_count.
    """
    win_count: float = field(default=0)
    play_count: int = field(default=0)

    def __post_init__(self) -> None:
        """Ensures that win_count and play_count are valid after initialization."""
        if self.win_count < 0:
            raise ValueError('invalid win_count')
        if self.play_count < 0:
            raise ValueError('invalid play_count')
        if self.win_count > self.play_count:
            raise ValueError('win_count > play_count')

    @property
    def win_rate(self) -> float:
        """Calculates and returns the win rate."""
        return 0 if self.play_count == 0 else self.win_count / self.play_count

    def register_win(self, delta_wc: float) -> 'MCTSTreeData':
        """Updates win_count and play_count after a game simulation."""
        return MCTSTreeData(self.win_count + delta_wc, self.play_count + 1)


class MCTSAI(othello.AI):
    """
    AI agent that uses Monte Carlo Tree Search to play Othello.
    
    Attributes:
        play_as (othello.Player): The player that the AI is representing.
        n_iters (int): Number of iterations to run MCTS for each move.
        c (float): Exploration parameter for the UCB algorithm.
    """
    def __init__(self, play_as: othello.Player, n_iters: int = 100,
                 c: float = sqrt(2)) -> None:
        """Initialize the MCTSAI with the player, number of iterations, and exploration parameter."""
        super().__init__()
        self.play_as = play_as
        self.n_iters = n_iters
        self.c = c
        self.mcts_tree: defaultdict[tuple[othello.Player, othello.State], MCTSTreeData] = defaultdict(MCTSTreeData)

    def play(self, state: othello.State) -> Optional[othello.Action]:
        """
        Simulates MCTS iterations and selects the best action to play.
        
        Args:
            state (othello.State): The current state of the Othello game.
            
        Returns:
            Optional[othello.Action]: The chosen action, or None if no legal actions are available.
        """
        
        # MCTS algorithm implementation
        for _ in range(self.n_iters):
            cur_state = state
            player = self.play_as.adversary
            visited = [(player, cur_state)]
            # Selection & Expansion.
            while cur_state.get_conclusion() is None:
                player = player.adversary
                legal_actions = list(cur_state.get_legal_actions(player))

                if legal_actions != []:
                    next_states = [cur_state.perform_action(
                        player, action) for action in legal_actions]
                    not_played_states \
                        = [s for s in next_states
                           if self.mcts_tree[player, s].play_count == 0]

                    if not_played_states == []:
                        log_n = log(sum(self.mcts_tree[player, s].play_count
                                        for s in next_states))

                        def ucb(s: othello.State) -> float:
                            wr = self.mcts_tree[player, s].win_rate
                            pc = self.mcts_tree[player, s].play_count
                            return wr + self.c * sqrt(log_n / pc)

                        cur_state = max(next_states, key=ucb)
                        visited.append((player, cur_state))
                    else:
                        # Removing type annotation causes error here.
                        cur_state: othello.State = random.choice(
                            not_played_states)
                        visited.append((player, cur_state))
                        break

            # Simulation.

            while (conclusion := cur_state.get_conclusion()) is None:
                player = player.adversary
                legal_actions = list(cur_state.get_legal_actions(player))

                if legal_actions != []:
                    next_states = [cur_state.perform_action(
                        player, action) for action in legal_actions]
                    cur_state = random.choice(next_states)

            # Backpropagation.

            for player, s in visited:
                if conclusion is othello.DRAW:
                    delta_wc = .5
                elif conclusion is player:
                    delta_wc = 1
                else:  # if conclusion is player.adversary
                    delta_wc = 0

                self.mcts_tree[player, s] \
                    = self.mcts_tree[player, s].register_win(delta_wc)

        legal_actions = list(state.get_legal_actions(self.play_as))

        if legal_actions == []:
            return None
        else:
            next_states = [state.perform_action(
                self.play_as, action) for action in legal_actions]
            chosen_action, _ \
                = max(zip(legal_actions, next_states),
                      key=lambda x: self.mcts_tree[self.play_as, x[1]].win_rate)
            return chosen_action


def run_mcts_ais() -> None:
    """
    Runs a game of Othello between two MCTS AI agents.
    """
    n_iters = 100
    referee = Simulation(MCTSAI(othello.Player.BLACK, n_iters),
                         MCTSAI(othello.Player.WHITE, n_iters))
    referee.run()

if __name__ == '__main__':
    run_mcts_ais()