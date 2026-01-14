import pygame
from gui import GameWindow

def main():
    """Точка входа в игру Крестики-Нолики"""
    pygame.init()
    try:
        GameWindow().run()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
