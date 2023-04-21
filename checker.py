import pygame
from move import Move
from typing import Optional
from constants import COLS, SQUARE_SIZE, CHECKER_SIZE, ROWS
from enum import Enum

class Team(Enum):
    RED = 1
    BLUE = 2


class Checker:
    def __init__(self, row, col, team: Team) -> None:
        self.row = row
        self.col = col
        self.team = team

    def move(self, row, col):
        self.row = row
        self.col = col
        if self.team == Team.BLUE and self.row == ROWS - 1:
            return Queen(self.row, self.col, self.team)
        elif self.team == Team.RED and self.row == 0:
            return Queen(self.row, self.col, self.team)

    def draw(self, win) -> None:
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        color = None
        if self.team == Team.BLUE:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.circle(win, color, (x, y), CHECKER_SIZE // 2)

    def legit_moves(self, board) -> list[Move]:
        moves = []
        if self.team == Team.BLUE:
            if self.col != 0:
                collision = board.get_piece(self.row + 1, self.col - 1)
                if collision == None:
                    moves.append(Move(self.row, self.col, self.row + 1, self.col - 1, board.current_team))
                elif board.get_piece(self.row + 2, self.col - 2) == None and board.is_in_board(self.row + 2, self.col - 2) and self.team != collision.team: # We have to check if we can eat that piece
                    moves.append(Move(self.row, self.col, self.row + 2, self.col - 2, board.current_team, [collision]))
            if self.col != COLS - 1:
                collision = board.get_piece(self.row + 1, self.col + 1)
                if collision == None:
                    moves.append(Move(self.row, self.col, self.row + 1, self.col + 1, board.current_team))
                elif board.get_piece(self.row + 2, self.col + 2) == None and board.is_in_board(self.row + 2, self.col + 2) and self.team != collision.team: # We have to check if we can eat that piece
                    moves.append(Move(self.row, self.col, self.row + 2, self.col + 2, board.current_team, [collision]))
        else:
            if self.col != 0:
                collision = board.get_piece(self.row - 1, self.col - 1)
                if collision == None:
                    moves.append(Move(self.row, self.col, self.row - 1, self.col - 1, board.current_team))
                elif board.get_piece(self.row - 2, self.col - 2) == None and board.is_in_board(self.row - 2, self.col - 2) and self.team != collision.team: # We have to check if we can eat that piece
                    moves.append(Move(self.row, self.col, self.row - 2, self.col - 2, board.current_team, [collision]))
            if self.col != COLS - 1:
                collision = board.get_piece(self.row - 1, self.col + 1)
                if collision == None:
                    moves.append(Move(self.row, self.col, self.row - 1, self.col + 1, board.current_team))
                elif board.get_piece(self.row - 2, self.col + 2) == None and board.is_in_board(self.row - 2, self.col + 2) and self.team != collision.team: # We have to check if we can eat that piece
                    moves.append(Move(self.row, self.col, self.row - 2, self.col + 2, board.current_team, [collision]))
        return moves
    
    def __eq__(self, checker) -> bool:
        return checker != None and self.col == checker.col and self.row == checker.row

    def __repr__(self) -> str:
        return f"Checker : row = {self.row} | col = {self.col} | team = {self.team}"

class Queen(Checker):
    def __init__(self, row, col, team: Team) -> None:
        super().__init__(row, col, team)

    def draw(self, win) -> None:
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        color = None
        if self.team == Team.BLUE:
            color1 = (0, 0, 255)
            color2 = (0, 200, 255)
        else:
            color1 = (255, 0, 0)
            color2 = (255, 200, 0)
        pygame.draw.circle(win, color1, (x, y), CHECKER_SIZE // 2)
        pygame.draw.circle(win, color2, (x, y), CHECKER_SIZE // 3)
        

    def legit_moves(self, board) -> None:
        # While in board:
        #   Check en diagonal
        moves = []
        collision1 = board.get_piece(self.row + 1, self.col - 1)
        collision2 = board.get_piece(self.row - 1, self.col - 1)
        collision3 = board.get_piece(self.row + 1, self.col + 1)
        collision4 = board.get_piece(self.row - 1, self.col + 1)
        if board.is_in_board(self.row + 1, self.col - 1):
            if collision1 == None:
                moves.append(Move(self.row, self.col, self.row + 1, self.col - 1, board.current_team, state = True))
            elif board.get_piece(self.row + 2, self.col - 2) == None and board.is_in_board(self.row + 2, self.col - 2) and self.team != collision1.team: # We have to check if we can eat that piece
                moves.append(Move(self.row, self.col,self.row + 2, self.col - 2, board.current_team, [collision1], True))
        if board.is_in_board(self.row - 1, self.col - 1):
            if collision2 == None:
                moves.append(Move(self.row, self.col, self.row - 1, self.col - 1, board.current_team, state = True))
            elif board.get_piece(self.row - 2, self.col - 2) == None and board.is_in_board(self.row - 2, self.col - 2) and self.team != collision2.team: # We have to check if we can eat that piece
                moves.append(Move(self.row, self.col,self.row - 2, self.col - 2, board.current_team, [collision2], True))    
        if board.is_in_board(self.row + 1, self.col + 1):
            if collision3 == None:
                moves.append(Move(self.row, self.col,self.row + 1, self.col + 1, board.current_team, state = True))
            elif board.get_piece(self.row + 2, self.col + 2) == None and board.is_in_board(self.row + 2, self.col + 2) and self.team != collision3.team: # We have to check if we can eat that piece
                moves.append(Move(self.row, self.col,self.row + 2, self.col + 2, board.current_team, [collision3], True))
        if board.is_in_board(self.row - 1, self.col + 1):
            if collision4 == None:
                moves.append(Move(self.row, self.col,self.row - 1, self.col + 1, board.current_team, state = True))
            elif board.get_piece(self.row - 2, self.col + 2) == None and board.is_in_board(self.row - 2, self.col + 2) and self.team != collision4.team: # We have to check if we can eat that piece
                moves.append(Move(self.row, self.col,self.row - 2, self.col + 2, board.current_team, [collision4], True))                 
        return moves