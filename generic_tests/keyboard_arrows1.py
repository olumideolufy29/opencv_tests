import curses
stdscr = curses.initscr()
#curses.cbreak()
stdscr.keypad(1)

#stdscr.addstr(0,10,"Hit 'q' to quit")
#stdscr.refresh()
x,y = 0,0
key = ''
while key != ord('q'):
    key = stdscr.getch()
    #stdscr.addch(20,25,key)
    stdscr.refresh()
    if key == curses.KEY_UP: 
        y = y + 1
    if key == curses.KEY_DOWN:
        y = y -1
    if key == curses.KEY_LEFT:
        x = x -1
    if key == curses.KEY_RIGHT: 
        x = x +1
    print x, y

curses.endwin()
