import pygame
from checker import Team
from ai import AI
from board import Board
from constants import WIDTH, HEIGHT, FPS

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de dames")

def main():
    run = True
    clock = pygame.time.Clock()

    board = Board()
    ai = AI(board)
    board.init_board()

    selected_checker = None

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                board.undo()
                selected_checker = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = board.get_pos(*pos)
                if selected_checker != None:
                    move = board.legit_click(row, col)
                    if move is not None:
                        if not board.move_checker(selected_checker, move):
                            selected_checker = None
                    else:
                        checker = board.get_piece(row, col)
                        if checker is not None and board.current_team == checker.team:
                            selected_checker = checker
                            board.legit_moves(checker)
                        else:
                            board.legit_move.clear()
                else:
                    checker = board.get_piece(row, col)
                    if checker != None and board.current_team == checker.team:
                        board.legit_moves(checker)
                        selected_checker = checker
        if board.current_team == Team.BLUE:
            checker, move = ai.predict()
            board.move_checker(checker, move)
        board.draw_board(WIN)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()