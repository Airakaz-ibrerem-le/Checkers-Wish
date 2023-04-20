from move import Move
from checker import Checker, Team
from board import Board
from graph import Graph, State

class AI:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.graph = Graph(0, State.MAX)
    
    def predict(self, max_depth = 10) -> tuple[Checker, Move]:
        def dfs(graph: Graph, move: Move, depth = 0) -> tuple[Move, int]:
            checker = self.board.get_piece(move.prev_row, move.prev_col)
            self.board.move_checker(checker, move)
            moves = self.board.get_all_legit_move(checker.team)
            if len(moves) == 0 or depth == max_depth:
                graph.value = self.board.heuristic_function()
                self.board.undo()
                return (move, graph.value)

            score_list : list[tuple[Move, int]] = []

            for iter in moves:
                m, score = dfs(graph.addChildren(), iter, depth + 1)
                score_list.append((m, score))

            self.board.undo()
            if self.board.current_team == Team.BLUE: # Maximize the score
                m, score = max(score_list, key= lambda x: x[1])
                graph.value = score
                return (m, score)
            else: # Minimize
                m, score = min(score_list, key= lambda x: x[1])
                graph.value = score
                return (m, score)


        self.graph = Graph(0, State.MAX)
        moves = self.board.get_all_legit_move(Team.BLUE)
        decision : list[tuple[Move, int]] = []

        # Evaluating initial options
        for _move in moves:
            m, score = dfs(self.graph.addChildren(), _move)
            decision.append((m, score))

        move, score = max(decision, key= lambda x: x[1])
        self.graph.value = score
        return self.board.get_piece(move.prev_row, move.prev_col), move
