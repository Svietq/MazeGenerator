import random
import time
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


HORIZONTAL_WALL = '-'
VERTICAL_WALL = '|'
NO_WALL = ' '
random.seed(time.time())


class Cell:
    def __init__(self):
        self.top = HORIZONTAL_WALL
        self.bottom = HORIZONTAL_WALL
        self.left = VERTICAL_WALL
        self.right = VERTICAL_WALL
        self.is_visited = False

    def remove_wall(self, direction):
        if direction == Direction.UP:
            self.bottom = NO_WALL
        elif direction == Direction.DOWN:
            self.top = NO_WALL
        elif direction == Direction.LEFT:
            self.right = NO_WALL
        elif direction == Direction.RIGHT:
            self.left = NO_WALL


class Maze:
    def __init__(self, size, filename):
        self.BOARD_SIZE = size
        self.board = [[Cell() for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]
        self.filename = filename

    def save_to_file(self):
        file = open(self.filename, "w+")
        cell_width = 3
        y = 0
        for column in self.board:
            x = 0
            for cell in column:
                self.gotoxy(file, x, y)
                file.write('.' + cell.top + '.\n')
                self.gotoxy(file, x, y+1)
                file.write(cell.left + NO_WALL + cell.right + '\n')
                self.gotoxy(file, x, y+2)
                file.write('.' + cell.bottom + '.' + '\n')
                x += cell_width - 1
            y += cell_width - 1
        file.close()

    def gotoxy(self, file, x, y):
        file.seek(y * (self.BOARD_SIZE * 4) ** 2 + x)

    def remove_walls(self, x=0, y=0, direction=Direction.UP):
        if x < 0 or x >= self.BOARD_SIZE or y < 0 or y >= self.BOARD_SIZE:
            return
        if self.board[y][x].is_visited:
            return

        self.board[y][x].is_visited = True
        self.board[y][x].remove_wall(direction)
        possible_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        new_direction = random.choice(possible_directions)

        for index in range(4):
            if new_direction == Direction.UP:
                self.remove_walls(x, y-1, Direction.UP)
                new_direction = Direction.RIGHT
            elif new_direction == Direction.DOWN:
                self.remove_walls(x, y+1, Direction.DOWN)
                new_direction = Direction.LEFT
            elif new_direction == Direction.LEFT:
                self.remove_walls(x-1, y, Direction.LEFT)
                new_direction = Direction.UP
            elif new_direction == Direction.RIGHT:
                self.remove_walls(x+1, y, Direction.RIGHT)
                new_direction = Direction.DOWN

    def synchronize_cells(self):
        for y, column in enumerate(self.board):
            for x, cell in enumerate(column):
                if cell.top == NO_WALL and y > 0:
                    self.board[y-1][x].bottom = NO_WALL
                if cell.bottom == NO_WALL and y < self.BOARD_SIZE - 1:
                    self.board[y+1][x].top = NO_WALL
                if cell.left == NO_WALL and x > 0:
                    self.board[y][x-1].right = NO_WALL
                if cell.right == NO_WALL and x < self.BOARD_SIZE - 1:
                    self.board[y][x+1].left = NO_WALL

    def generate(self):
        self.remove_walls()
        self.synchronize_cells()
        self.save_to_file()


maze = Maze(10, "maze.txt")
maze.generate()