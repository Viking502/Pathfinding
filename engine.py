import random as rand
import pygame as pg
from terrain import Terrain
from pathfinder import Pathfinder


def main():

    pg.init()

    resolution = (1200, 900)
    window = pg.display.set_mode(resolution, pg.DOUBLEBUF | pg.RESIZABLE)
    pg.display.set_caption("pathfinder")

    map = Terrain(16, 22, 50)
    # format (y, x)
    map.set_target([1, 14])
    for _ in range(5):
        x = rand.randint(2, 20)
        y = rand.randint(2, 14)
        dx = rand.randint(1, max(10 - x, 2))
        dy = rand.randint(1, max(10 - y, 2))
        map.add_blocks([y, x], [dy, dx])

    #map.add_blocks([4, 11], [1, 7])
    #map.add_blocks([4, 13], [3, 1])
    #map.add_blocks([4, 15], [3, 1])

    pawn = Pathfinder([14, 14], map.grid)

    clock = pg.time.Clock()
    run_flag = True

    while run_flag:
        clock.tick(20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_flag = False

        if map.is_target_stolen():
            map.rand_target()
            map.clear()

        window.fill((120, 120, 120))
        map.draw(window)
        pg.display.update()

        pawn.make_move(map.grid, window, map)


if __name__ == '__main__':
    main()
