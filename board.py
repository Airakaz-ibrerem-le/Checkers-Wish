import pygame
from move import Move
from queue import LifoQueue as Stack
from typing import Optional
from checker import Checker, Queen, Team
from constants import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE

class Board:
    def __init__(self, team = Team.RED) -> None:
        self.board: list[Checker] = []
        self.legit_move : list[Move] = []
        self.history : Stack[Move] =  Stack()
        self.current_team = team
        self.red_count = 12
        self.blue_count = 12
        self.red_queen = 0
        self.blue_queen = 0

    def draw_board(self, win) -> None:
        win.fill((255, 255, 255))
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for move in self.legit_move:
            pygame.draw.rect(win, (25, 205, 25), (move.col * SQUARE_SIZE, move.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for checker in self.board:
            checker.draw(win)

    def init_board(self) -> None:
        for row in range(3):
            for col in range(0, COLS, 2):
                if row % 2 == 0: # Row starts with blue
                    self.board.append(Checker(row, col, Team.BLUE))
                    self.board.append(Checker(ROWS - 1 - row, col + 1, Team.RED))
                else:
                    self.board.append(Checker(ROWS - 1 - row, col, Team.RED))
                    self.board.append(Checker(row, col + 1, Team.BLUE))

    def legit_moves(self, checker: Checker) -> None:
        self.legit_move = checker.legit_moves(self)
    
    def legit_click(self, rowClick, colClick) -> Optional[Move]:
        for move in self.legit_move:
            if move.row == rowClick and move.col == colClick:
                return move
        return None

    def heuristic_function(self) -> int:
        """
        Heuristic function evaluating the state of the board with respect
        to the AI side (blue team)

        Returns:
        int: Value of the board
        """
        return self.blue_count - self.red_count + int(self.blue_queen * 0.5 - self.red_queen * 0.5)
    
    def get_all_legit_move(self, team: Team) -> list[Move]:
        moves = []
        for checker in self.board:
            if checker.team != team:
                continue
            moves += checker.legit_moves(self) # ["a"] + ["b"] => ["a", "b"]
        return moves

    def undo(self) -> None:
        if self.history.empty():
            return
        self.legit_move.clear()
        move = self.history.get()
        checker = self.get_piece(move.row, move.col)
        checker.col = move.prev_col
        checker.row = move.prev_row

        if not move.state:
            if move.team == Team.RED:
                if move.row == 0:
                    self.board.append(Checker(checker.row, checker.col, checker.team))
                    self.board.remove(checker)
            else:
                if move.row == ROWS-1:
                    self.board.append(Checker(checker.row, checker.col, checker.team))
                    self.board.remove(checker)

        self.board += move.checkers
        self.current_team = move.team

        for c in move.checkers:
            if c.team == Team.BLUE:
                if isinstance(c, Queen):
                    self.blue_queen += 1
                self.blue_count += 1
            else:
                if isinstance(c, Queen):
                    self.red_queen += 1
                self.red_count += 1

    def move_checker(self, checker: Checker, move: Move) -> bool:
        self.history.put(move)
        self.legit_move.clear()
        for c in move.checkers:
            self.board.remove(c) # ["a", "b"].remove("a") => ["b"]
        queen = checker.move(move.row, move.col)
        if queen is not None:
            if checker.team == Team.BLUE:
                self.blue_queen += 1
            else:
                self.red_queen += 1
            self.board.remove(checker)
            self.board.append(queen)
            checker = queen
        if move.is_eating():
            # I know for a fact I am eating someone
            if move.checkers[0].team == Team.BLUE:
                if isinstance(move.checkers[0], Queen):
                    self.blue_queen -= 1
                self.blue_count -= 1
            else:
                if isinstance(move.checkers[0], Queen):
                    self.red_queen -= 1
                self.red_count -= 1
            for move in checker.legit_moves(self):
                if move.is_eating():
                    self.legit_move.append(move)
            if len(self.legit_move) == 0:
                self.current_team = (Team.BLUE if self.current_team == Team.RED else Team.RED)
                #move.change = True
                return False
            else:
                #move.change = False
                return True
        self.current_team = (Team.BLUE if self.current_team == Team.RED else Team.RED)
        #move.change = True
        return False

    def is_in_board(self, row, col) -> bool:
        return 0 <= row < ROWS and 0 <= col < COLS


    def get_pos(self, x, y) -> tuple[int, int]:
        return (x // (WIDTH//COLS), y // (HEIGHT // ROWS))

    def get_piece(self, row, col) -> Optional[Checker]:
        for checker in self.board:
            if checker.col == col and checker.row == row:
                return checker
    
    def __repr__(self) -> str:
        board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        for checker in self.board:
            if checker.team == Team.BLUE:
                board[checker.row][checker.col] = 'b'
            else:
                board[checker.row][checker.col] = 'r'
        
        res = f"Board: turn={self.current_team}:\n" + "-" * COLS * 4 + "\n"
        for row in board:
            res += (" | ".join(row)) + "\n"
            res += "-" * COLS * 4 + "\n"
        return res
