class Move:
    def __init__(self, prev_row, prev_col, row, col, team, checkers = None, state = False) -> None:
        self.row = row
        self.col = col
        self.prev_row = prev_row
        self.prev_col = prev_col
        self.team = team
        self.state = state
        if checkers is None:
            checkers = []
        self.checkers = checkers
    
    def is_eating(self) -> bool:
        return len(self.checkers) != 0
    
    def __repr__(self) -> str:
        return f"Move from: row = {self.prev_row} | col = {self.prev_col} to : row = {self.row} | col = {self.col} ({self.team})"