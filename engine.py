import random as rand
import pygame as pg
from terrain import Terrain
from pathfinder import Pathfinder


def main():

    pg.init()

    resolution = (1200, 900)
    window = pg.display.set_mode(resolution, pg.DOUBLEBUF | pg.RESIZABLE)
    pg.display.set_caption("pathfinder")

    map = Terrain(8, 11, 100)
    # format (y, x)
    map.set_target([1, 6])
    pawn = Pathfinder([6, 6], map.grid)

    clock = pg.time.Clock()
    run_flag = True

    while run_flag:
        clock.tick(20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_flag = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    map.add_block_manually(pg.mouse.get_pos())
                if event.key == pg.K_e:
                    map.set_target_manually(pg.mouse.get_pos())
                if event.key == pg.K_q:
                    map.free_block_manually(pg.mouse.get_pos())

        window.fill((120, 120, 120))
        map.draw(window)
        pg.display.update()

        pawn.make_move(map.grid, window, map)


if __name__ == '__main__':
    main()
