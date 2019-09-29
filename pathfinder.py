import math
import numpy as np
import random as rand
import const as CONST
import pygame as pg

import pprint
import time


class Pathfinder:
    path_que = []

    def __init__(self, pos, grid):
        self.pos = pos
        grid[pos[0]][pos[1]] = CONST.PAWN

        self.target = pos
        self.find_target(grid)

    def first_pick(self, grid):
        best_mv = self.pos
        best_dist = 999

        if grid[self.pos[0]][self.pos[1]] == CONST.TARGET \
                or grid[self.pos[0]][self.pos[1]] == CONST.WALL:
            return False

        for step in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
            mv_pos = np.add(self.pos, step)
            if grid[mv_pos[0]][mv_pos[1]] != CONST.WALL:
                curr_dist = self.heuristic(mv_pos, self.target)

                if curr_dist < best_dist \
                        or (curr_dist == best_dist and rand.randint(0, 1) == 1):
                    best_dist = curr_dist
                    best_mv = mv_pos
        self.path_que.append(best_mv)
        grid[best_mv[0]][best_mv[1]] = CONST.QUE_PATH
        return True

    def dijkstra(self, grid):

        cost = [[100 for _ in g] for g in grid]
        cost[self.pos[0]][self.pos[1]] = 0
        que = [self.pos]

        while len(que) > 0:
            curr_pos = que.pop()
            for step in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
                mv_pos = np.add(curr_pos, step)
                if not grid[mv_pos[0]][mv_pos[1]] & (CONST.WALL | CONST.QUE_PATH | CONST.DEATH_WAY):
                    if cost[curr_pos[0]][curr_pos[1]] + 1 < cost[mv_pos[0]][mv_pos[1]]:
                        cost[mv_pos[0]][mv_pos[1]] = cost[curr_pos[0]][curr_pos[1]] + 1
                        que.append(mv_pos)

        pointer = self.target
        self.path_que.append(list(pointer))
        while pointer[0] != self.pos[0] or pointer[1] != self.pos[1]:
            min_cost = 100
            best_move = pointer
            for step in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
                next_mv = np.add(pointer, step)
                if cost[next_mv[0]][next_mv[1]] < min_cost:
                    min_cost = cost[next_mv[0]][next_mv[1]]
                    best_move = next_mv
            pointer = best_move
            self.path_que.append(list(pointer))
            if grid[pointer[0]][pointer[1]] != CONST.PAWN:
                grid[pointer[0]][pointer[1]] = CONST.QUE_PATH
        return True

    def a_star(self, grid, win, map):
        if grid[self.pos[0]][self.pos[1]] & (CONST.WALL | CONST.TARGET):
            return False

        possible_ways = [{'path': [self.pos], 'cost': 0, 'heuristic': self.heuristic(self.pos, self.target)}]
        found_way_flag = False

        while not found_way_flag:

            best_way = possible_ways[0]
            for way in possible_ways:
                if way['cost'] + way['heuristic'] > best_way['cost'] + best_way['heuristic']:

                    #death_way_flag = True
                    #for step in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
                    #    mv_pos = np.add(way['path'][-1], step)

                    #    if not grid[mv_pos[0]][mv_pos[1]] & (CONST.WALL | CONST.QUE_PATH | CONST.DEATH_WAY):
                    #        death_way_flag = False
                    #if not death_way_flag:
                    if grid[way['path'][-1][0]][way['path'][-1][1]] != CONST.DEATH_WAY:
                        best_way = way

            new_way = best_way.copy()
            possible_ways.append(new_way)

            best_dist = 999
            exist_way_flag = False
            for step in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
                mv_pos = np.add(new_way['path'][-1], step)

                if not grid[mv_pos[0]][mv_pos[1]] & (CONST.WALL | CONST.QUE_PATH | CONST.DEATH_WAY):
                    curr_dist = self.heuristic(mv_pos, self.target)
                    if curr_dist < best_dist:
                        exist_way_flag = True
                        best_dist = curr_dist
                        best_mv = mv_pos
            if exist_way_flag:
                new_way['path'].append(best_mv)
                new_way['cost'] += 1
                new_way['heuristics'] = self.heuristic(best_mv, self.target)
                if self.heuristic(best_mv, self.target) == 0:
                    found_way_flag = True
                if grid[best_mv[0]][best_mv[1]] != CONST.TARGET:
                    grid[best_mv[0]][best_mv[1]] = CONST.QUE_PATH
            else:
                grid[new_way['path'][-1][0]][new_way['path'][-1][1]] = CONST.DEATH_WAY
                possible_ways.remove(new_way)
                # print(len(possible_ways))

            win.fill((120, 120, 120))
            map.draw(win)
            pg.display.update()

        self.path_que = new_way['path']
        self.path_que.reverse()
        return True

    def find_target(self, grid):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == CONST.TARGET:
                    self.target = [y, x]

    def set_target(self, pos):
        self.target = [pos[0], pos[1]]

    def make_move(self, grid, win, map):

        if len(self.path_que) == 0:
            if grid[self.target[0]][self.target[1]] != CONST.PAWN:
                # self.a_star(grid, win, map)
                self.dijkstra(grid)
            else:
                self.find_target(grid)
        else:
            old_pos = self.pos
            self.pos = self.path_que.pop()

            grid[old_pos[0]][old_pos[1]] = CONST.PATH
            grid[self.pos[0]][self.pos[1]] = CONST.PAWN
            time.sleep(0.1)

    @staticmethod
    def heuristic(start, end):

        distance = 0
        for dim in range(len(end)):
            distance += (end[dim] - start[dim]) ** 2

        return math.sqrt(distance)
