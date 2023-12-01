import random
from typing import Optional

import othello
from gameplay import Simulation
import evaluation

class AlphaBetaAI(othello.AI):
    """
    An AI agent for playing Othello that uses a minimax algorithm with alpha-beta pruning to determine the best move.

    Attributes:
        play_as (othello.Player): The player that the AI is controlling, either BLACK or WHITE.
        depth (int): The depth limit for the minimax search tree.
        evaluation_function (function): A function from the evaluation module used to evaluate the utility of a game state.
    """
    
    def __init__(self, play_as: othello.Player, search_depth: int = 2, eval_func=evaluation.heuristic_eval_comprehensive) -> None:
        """
        Initializes an AlphaBetaAI instance with a specified player, search depth, and evaluation function.

        Args:
            play_as: The player that the AI will play as.
            search_depth: The maximum depth of the search tree.
            eval_func: The evaluation function to use for scoring the board.
        """
        super().__init__()
        self.play_as = play_as
        self.depth = search_depth
        self.evaluation_function = lambda state: eval_func(state, self.play_as)

    def play(self, state: othello.State) -> Optional[othello.Action]:
        """
        Plays a move by using the minimax algorithm with alpha-beta pruning.

        Args:
            state: The current state of the Othello board.

        Returns:
            The action (move) that the AI decides to take. If there are no legal actions, returns None.
        """
        legal_actions = list(state.get_legal_actions(self.play_as))
        if not legal_actions:
            return None
        
        # Internal function to perform minimax search
        else:
            def minimax(currentGameState, depth, player):
                if currentGameState.is_terminal():
                    return self.evaluation_function(currentGameState)
                legal_actions = list(currentGameState.get_legal_actions(player))

                scores = []
                if player != self.play_as:
                    if depth == self.depth:
                        if len(legal_actions) == 0:
                            return self.evaluation_function(currentGameState)
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores.append(self.evaluation_function(currentGameState))
                        return min(scores)
                    else:
                        if len(legal_actions) == 0:
                            return minimax(currentGameState, depth + 1, player.adversary)
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores.append(minimax(childGameState, depth + 1, player.adversary))
                        return min(scores)
                else:
                    if len(legal_actions) == 0:
                        return minimax(currentGameState, depth, player.adversary)
                    for action in legal_actions:
                        childGameState = currentGameState.perform_action(player, action)
                        scores.append(minimax(childGameState, depth, player.adversary))
                    return max(scores)    

            scores = []
            # Choose one of the best actions
            for action in legal_actions:
                childgameState = state.perform_action(self.play_as, action)
                scores.append(minimax(childgameState, 1, self.play_as.adversary))
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            # Pick randomly among the best
            chosenIndex = random.choice(bestIndices) 
            
            return legal_actions[chosenIndex]

def run_alphabeta_ais() -> None:
    """
    Sets up and runs a game of Othello between two AI players using alpha-beta pruning.
    """
    referee = Simulation(AlphaBetaAI(othello.Player.BLACK),
                         AlphaBetaAI(othello.Player.WHITE))
    referee.run()

if __name__ == '__main__':
    run_alphabeta_ais()
