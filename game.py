class Game:
    """Логика игры"""

    def __init__(self):
        """Инициализация"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        """Делает ход. Возвращает True если успешно, False если клетка занята."""
        # Проверка координат
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise ValueError(f"Координаты должны быть 0-2, получено ({row}, {col})")

        # Проверка завершения
        if self.game_over:
            raise RuntimeError("Игра уже завершена")

        # Проверка занятости
        if self.board[row][col] != '':
            return False

        # Совершить ход
        self.board[row][col] = self.current_player

        # Проверить результат
        if self._check_winner():
            self.winner = self.current_player
            self.game_over = True
        elif self._check_draw():
            self.game_over = True
        else:
            self._switch_player()

        return True

    def _check_winner(self):
        """Проверка победы текущего игрока"""
        player = self.current_player
        board = self.board

        # Проверка строк
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] == player:
                return True

        # Проверка столбцов
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] == player:
                return True

        # Главная диагональ
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True

        # Побочная диагональ
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True

        return False

    def _check_draw(self):
        """Проверка ничьей"""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True

    def _switch_player(self):
        """Переключение игрока"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_game(self):
        """Сброс игры в начальное состояние"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def get_board_state(self):
        """Возвращает копию доски"""
        return [row[:] for row in self.board]

    def get_game_status(self):
        """Возвращает словарь со статусом игры"""
        return {
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'is_draw': self.game_over and self.winner is None
        }
