import pygame as pg
import numpy as np
import random as rand
import const as CONST


class Terrain:

    def __init__(self, height, width, size):
        self.size = size
        self.width = width
        self.height = height
        self.grid = [[CONST.FREE for _ in range(width)] for _ in range(height)]
        for y in {0, height - 1}:
            for x in range(width):
                self.grid[y][x] = CONST.WALL
        for x in {0, width - 1}:
            for y in range(height):
                self.grid[y][x] = CONST.WALL
        self.target = [0, 0]

    def set_target(self, pos):
        self.grid[pos[0]][pos[1]] = CONST.TARGET
        self.target = [pos[0], pos[1]]

    def set_target_manually(self, mouse_pos):
        pos = [mouse_pos[1] // self.size, mouse_pos[0] // self.size]
        self.set_target(pos)


    def rand_target(self):

        rand_target = lambda interval: rand.randint(1, interval - 2)

        y = rand_target(self.height)
        x = rand_target(self.width)
        while self.grid[y][x] != CONST.FREE:
            y = rand_target(self.height)
            x = rand_target(self.width)
        self.grid[y][x] = CONST.TARGET
        self.target = [y, x]

    def clear(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == CONST.QUE_PATH\
                        or self.grid[y][x] == CONST.PATH:
                    self.grid[y][x] = CONST.FREE

    def get_target(self):
        return self.target

    def is_target_stolen(self):
        return self.grid[self.target[0]][self.target[1]] == CONST.PAWN

    def add_blocks(self, beg, vec):
        for y in range(vec[0]):
            for x in range(vec[1]):
                self.grid[beg[0] + y][beg[1] + x] = CONST.WALL

    def add_block_manually(self, mouse_pos):
        pos = [mouse_pos[1] // self.size, mouse_pos[0] // self.size]
        self.grid[pos[0]][pos[1]] = CONST.WALL

    def draw(self, win):

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == CONST.TARGET:
                    marker = (40, 250, 20)
                elif self.grid[y][x] == CONST.PAWN:
                    marker = (250, 70, 20)
                elif self.grid[y][x] == CONST.QUE_PATH:
                    marker = (250, 250, 20)
                elif self.grid[y][x] == CONST.WALL:
                    marker = (90, 90, 90)
                elif self.grid[y][x] == CONST.PATH:
                    marker = (0, 200, 205)
                elif self.grid[y][x] == CONST.DEATH_WAY:
                    marker = (20, 20, 20)
                else:
                    marker = (50, 250, 255)
                pg.draw.rect(win, marker, pg.Rect(np.multiply([x, y], self.size), [self.size, self.size]))
                pg.draw.rect(win, (0, 0, 0), pg.Rect(np.multiply([x, y], self.size), [self.size, self.size]), 2)
