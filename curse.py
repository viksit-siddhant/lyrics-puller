from curses import wrapper
import curses
import curses.ascii
from genius import get_search,parse_lyrics
import sys

def main(stdscr):
    stdscr.clear()
    curses.curs_set(False)
    y,x = stdscr.getmaxyx()
    typing = True
    selecting = False
    display = False
    search_term = ""
    selection = 0
    top_line = 0
    song_list = []
    song_urls = []
    lyrics = ""
    if len(sys.argv) > 1:
        for word in sys.argv[1:]:
            search_term += word
            search_term += " "
        typing = False
        selecting = True
        song_list,song_urls=get_search(search_term)
        stdscr.addstr(0,0,song_list[0],curses.A_STANDOUT)
        selection = 0
        for i in range(1,len(song_list)):
            stdscr.addstr(i,0,song_list[i])

    while True:
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 16:
            break
        elif typing:
            if ch == curses.KEY_BACKSPACE:
                if len(search_term) > 0:
                    search_term = search_term[:-1]
            elif ch == 10:
                stdscr.addstr(1,0,'Getting results...')
                typing = False
                selecting = True
                song_list,song_urls=get_search(search_term)
                stdscr.addstr(0,0,song_list[0],curses.A_STANDOUT)
                for i in range(1,len(song_list)):
                    stdscr.addstr(i,0,song_list[i])
                continue

            else:
                search_term += chr(ch)
            stdscr.addstr(0,0," "*x)
            stdscr.addstr(0,0,search_term)
        elif selecting:
            if ch == ord('w') and selection > 0:
                selection -= 1
            elif ch == ord('s') and selection < len(song_list)-1:
                selection += 1
            elif ch == ord('g'):
                for i in range(len(song_list)):
                    stdscr.addstr(i,0," "*x)
                stdscr.addstr(0,0,search_term)
                typing = True
                selection = 0
                selecting = False
                continue
            elif ch == 10:
                selecting = False
                display = True
                lyrics = parse_lyrics(song_urls[selection]).split('\n') 
                for i in range(0,y-1):
                    stdscr.addstr(i,0," "*x)
                    if i >= len(lyrics):
                        break
                    stdscr.addstr(i,0,lyrics[i])
                selection = 0
                continue

            for i in range(len(song_list)):
                song = song_list[i]
                if len(song) > x-3:
                    song = song[:x-2] + '...'
                if i == selection:
                    stdscr.addstr(i,0,song,curses.A_STANDOUT)
                else:
                    stdscr.addstr(i,0,song)

        elif display:
            if ch == ord('g'):
                for i in range(y-1):
                    stdscr.addstr(i,0," "*x)
                stdscr.addstr(0,0,search_term)
                typing = True
                search_term = ""
                display = False
                top_line = 0
                continue

            elif ch == ord('f'):
                for i in range(y-1):
                    stdscr.addstr(i,0," "*x)
                display = False
                selecting = True
                top_line = 0
                stdscr.addstr(0,0,song_list[0],curses.A_STANDOUT)
                for i in range(1,len(song_list)):

                    stdscr.addstr(i,0,song_list[i])
                continue

            elif ch == ord('s'):
                top_line += 1

            elif ch == ord('w') and top_line > 0:
                top_line -= 1

            for i in range(top_line,top_line+y-1):
                stdscr.addstr(i-top_line,0," "*x)
                if i >= len(lyrics):
                    break
                stdscr.addstr(i-top_line,0,lyrics[i])

wrapper(main)
