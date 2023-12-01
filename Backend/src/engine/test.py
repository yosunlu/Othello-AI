import othello
from gameplay import Simulation
import evaluation
import unittest

from alpha_beta_ai import AlphaBetaAI
from mcts_ai import MCTSAI


class TestAlphaBetaAI(unittest.TestCase):
	def test_alpha_beta_ai(self):
		simulation = Simulation(AlphaBetaAI(othello.Player.BLACK),
							 AlphaBetaAI(othello.Player.WHITE))
		simulation.run()

class TestMCTSAI(unittest.TestCase):
	def test_mcts_ai(self):
		n_iters = 100

		simulation = Simulation(MCTSAI(othello.Player.BLACK, n_iters),
							 MCTSAI(othello.Player.WHITE, n_iters))
		simulation.run()
	
class TestAI(unittest.TestCase):
	def __init__(self, AI1_id=0, AI2_id=0, search_depth_1: int =2, search_depth_2: int =2, 
				 eval_func=evaluation.heuristic_eval_comprehensive) -> None:
		super().__init__()

		self.AI1_id = AI1_id
		self.AI2_id = AI2_id
		self.eval_func = eval_func
		self.search_depth_1 = search_depth_1
		self.search_depth_2 = search_depth_2

	def test_ai(self):
		AIs_1 = [AlphaBetaAI(othello.Player.BLACK, eval_func=self.eval_func), 
				MCTSAI(othello.Player.BLACK)]
		AIs_2 = [AlphaBetaAI(othello.Player.WHITE, eval_func=self.eval_func),
				MCTSAI(othello.Player.WHITE)]
		simulation = Simulation(AIs_1[self.AI1_id],
							 AIs_2[self.AI2_id])
		simulation.run()

if __name__ == '__main__':
	for i in range(2):
		for j in range(2):
			print('i =', i, '\tj =', j)
			TestAI(i, j).test_ai()
		print()

