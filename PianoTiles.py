#libraries
import curses
import random
import threading
import time

#global consts
LANES = 4
TILECHAR = '█'
EMPTYCHAR = ' '
SCREENH = 20
TILEW = 5
TILEH = 1

#global states of tiles
gamefin = False
tiles = []

#global vars
pts = 0
elapsed = 0
timerstatus = False

def stopwatch():
    global elapsed, timerstatus
    starttime = time.perf_counter()
    while timerstatus:
        elapsed = time.perf_counter() - starttime
        time.sleep(0.01)

#generates one state of tiles in booleans with 1 true and 3 falses
def tilegenerator():
    row = [EMPTYCHAR] * LANES
    randlane = random.randint(0, LANES - 1)
    row[randlane] = TILECHAR
    return row

#cascades the existing states and adds one more
def cascader(stdscr,speed):
    global tiles, gamefin

    while not gamefin:
        stdscr.clear()

        newstate = tilegenerator()
        tiles.insert(0, newstate)

        if len(tiles) > SCREENH:
            if TILECHAR in tiles[-1]:
                gamefin = True
            tiles.pop()

        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                stdscr.addstr(y, x * TILEW, tile * TILEW)

        stdscr.refresh()
        time.sleep(speed)

#checks if any of the tiles have reached the end and ends the game
def thresholdchecker():
    global gamefin

    if len(tiles) > SCREENH and TILECHAR in tiles[-1]:
        gamefin = True

#this might only work for macos
#uses curses library to get cursor info
#disappears tiles if they are clicked or ends game if user clicks a not tile
def clickcheck(stdscr):
    global tiles, gamefin, pts

    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    while not gamefin:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, buttonstate = curses.getmouse()
            if buttonstate & curses.BUTTON1_CLICKED:
                lane = x // TILEW
                if y < len(tiles) and lane < LANES and tiles[y][lane] == TILECHAR:
                    tiles[y][lane] = EMPTYCHAR
                    pts += 1
                else:
                    gamefin = True

#main
def main(stdscr):
    global tiles, gamefin, timerstatus, speed

    curses.curs_set(0)
    tiles = []

    #threading for the cascader so it can work as a background process
    cascadethread = threading.Thread(target=cascader, args=(stdscr,speed,))
    cascadethread.daemon = True
    cascadethread.start()

    #another threading for the points system
    timerstatus = True
    stopwatchthread = threading.Thread(target=stopwatch, daemon=True)
    stopwatchthread.start()

    clickcheck(stdscr)

    #btw this doesnt need a control flow cos the clickcheck() already has a while loop inside
    timerstatus = False
    stdscr.clear()
    stdscr.addstr(SCREENH // 2, 10, f'Game over! you lasted {elapsed} seconds and scored {pts} points.')
    stdscr.refresh()
    stdscr.getch()

print('Speed? (0.5 for fast, 1 for medium, 2 for slow)')
speed = float(input())
curses.wrapper(main)