import pygame
from game import Game


class GameWindow:
    """Графический интерфейс."""

    def __init__(self):
        # Окно
        self.screen = pygame.display.set_mode((600, 800))
        pygame.display.set_caption("Крестики-нолики")

        # Шрифты
        self.font_big = pygame.font.Font(None, 72)
        self.font_mid = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)

        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game()

        # Счетчик побед
        self.score = {'X': 0, 'O': 0, 'draws': 0}

        self.error_msg = ""
        self.error_time = 0

    def run(self):
        while self.running:
            # События
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            # Очистка ошибки
            if self.error_msg and pygame.time.get_ticks() > self.error_time + 2000:
                self.error_msg = ""

            # Отрисовка
            self.draw()
            self.clock.tick(60)

    def handle_click(self, pos):
        x, y = pos

        # Кнопка "Новая игра"
        if 70 <= x <= 230 and 20 <= y <= 70:
            self.game.reset_game()
            return

        # Кнопка "Сброс счета"
        if 250 <= x <= 410 and 20 <= y <= 70:
            self.score = {'X': 0, 'O': 0, 'draws': 0}
            self.game.reset_game()
            return

        # Кнопка "Выход"
        if 430 <= x <= 530 and 20 <= y <= 70:
            self.running = False
            return

        # Клик по полю
        col = x // 200
        row = (y - 160) // 200

        if 0 <= row < 3 and 0 <= col < 3:
            try:
                if not self.game.make_move(row, col):
                    self.error_msg = "Клетка занята!"
                    self.error_time = pygame.time.get_ticks()
                else:
                    # Обновить счет при завершении игры
                    status = self.game.get_game_status()
                    if status['game_over']:
                        if status['is_draw']:
                            self.score['draws'] += 1
                        else:
                            self.score[status['winner']] += 1
            except Exception as e:
                self.error_msg = str(e)[:40]
                self.error_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill((255, 255, 255))  # Белый фон

        # Кнопка "Новая игра"
        pygame.draw.rect(self.screen, (173, 216, 230), (70, 20, 160, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (70, 20, 160, 50), 2)
        btn_text = self.font_small.render("Новая игра", True, (0, 0, 0))
        self.screen.blit(btn_text, btn_text.get_rect(center=(150, 45)))

        # Кнопка "Сброс счета"
        pygame.draw.rect(self.screen, (255, 200, 200), (250, 20, 160, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (250, 20, 160, 50), 2)
        reset_text = self.font_small.render("Сброс счета", True, (0, 0, 0))
        self.screen.blit(reset_text, reset_text.get_rect(center=(330, 45)))

        # Кнопка "Выход"
        pygame.draw.rect(self.screen, (220, 220, 220), (430, 20, 100, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (430, 20, 100, 50), 2)
        exit_text = self.font_small.render("Выход", True, (0, 0, 0))
        self.screen.blit(exit_text, exit_text.get_rect(center=(480, 45)))

        # Счетчик побед
        score_text = f"X: {self.score['X']}  |  O: {self.score['O']}  |  Ничья: {self.score['draws']}"
        score_surface = self.font_small.render(score_text, True, (50, 50, 50))
        self.screen.blit(score_surface, score_surface.get_rect(center=(300, 90)))

        # Статус
        status = self.game.get_game_status()
        if status['game_over']:
            text = "Ничья!" if status['is_draw'] else f"Игрок {status['winner']} победил!"
            color = (100, 100, 100) if status['is_draw'] else (0, 180, 0)
        else:
            text = f"Ход игрока: {status['current_player']}"
            color = (0, 0, 0)

        status_text = self.font_mid.render(text, True, color)
        self.screen.blit(status_text, status_text.get_rect(center=(300, 130)))

        # Сетка
        grid_top = 160
        for i in range(1, 3):
            # Горизонтальные линии
            pygame.draw.line(self.screen, (0, 0, 0),
                           (0, grid_top + i * 200), (600, grid_top + i * 200), 2)
            # Вертикальные линии
            pygame.draw.line(self.screen, (0, 0, 0),
                           (i * 200, grid_top), (i * 200, grid_top + 600), 2)

        # Граница сетки
        pygame.draw.rect(self.screen, (0, 0, 0), (0, grid_top, 600, 600), 3)

        # X и O
        board = self.game.get_board_state()
        for row in range(3):
            for col in range(3):
                if board[row][col] != '':
                    symbol = board[row][col]
                    color = (220, 50, 50) if symbol == 'X' else (50, 120, 255)
                    x = col * 200 + 100
                    y = grid_top + row * 200 + 100
                    text = self.font_big.render(symbol, True, color)
                    self.screen.blit(text, text.get_rect(center=(x, y)))

        # Подсказка
        hint_text = "R - новая игра  |  ESC - выход"
        hint_surface = self.font_tiny.render(hint_text, True, (120, 120, 120))
        self.screen.blit(hint_surface, hint_surface.get_rect(center=(300, 775)))

        # Ошибка
        if self.error_msg:
            err_text = self.font_small.render(self.error_msg, True, (200, 0, 0))
            self.screen.blit(err_text, err_text.get_rect(center=(300, 740)))

        pygame.display.flip()
