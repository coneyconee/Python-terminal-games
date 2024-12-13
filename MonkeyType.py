#libraries
import sys, tty, os, termios, time, threading

#to trunc random sentence if it gets too long ie over one line
def truncterminal(string):
    w = os.get_terminal_size().columns
    
    if len(string) > w:
        return string[:w - 3] + '...'
    return string

#ANSI const for colouring text
RED = '\033[31m'
GREEN = '\033[32m'
GREY = '\033[90m'
RESET = '\033[0m'

#variables for stopwatch()
elapsed = 0
timerstatus = False

#dependencies for randomsentence()
from random import choice
from nltk.corpus import words
realwordlst = tuple(words.words())

#wpm calculator
def wpm(sen,time):
    words = str(sen).split(' ')
    return (len(words)/time) * 60

#generates a random sentence of length chosen by user
def randomsentence(bomb):
    tmplst = []
    for i in range(bomb):
        tmplst.append(choice(realwordlst))
    return (truncterminal(' '.join(tmplst)).lower())

#threaded stopwatch to run in background
def stopwatch():
    global elapsed, timerstatus
    starttime = time.perf_counter()
    while timerstatus:
        elapsed = time.perf_counter() - starttime
        time.sleep(0.01)

#uses sys to get keyboard inputs in real-time
def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: 'space',
                9: 'tab',
                27: 'esc',
                65: 'up',
                66: 'down',
                67: 'right',
                68: 'left',
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

#essentially printing but overwriting the same line
def replaceln(printee):
    print('\r', end='')
    print(' ' * 80, end='')
    print('\r', printee, end='', flush=True)

#legacy colouring letters using external colorama library replaced by colourltrvanilla()
'''#using the colorama library to colour letters according to their status
def colourltr(ltr, status):
    if status == 'red':
        return colorama.Fore.RED + str(ltr) + colorama.Style.RESET_ALL
    elif status == 'green':
        return colorama.Fore.GREEN + str(ltr) + colorama.Style.RESET_ALL
    elif status == 'grey':
        return colorama.Fore.LIGHTBLACK_EX + str(ltr) + colorama.Style.RESET_ALL'''

#colour letters without external libaries
def colourltrvanilla(ltr,status):
    global RED,GREEN,GREY,RESET

    if status == 'red':
        return f'{RED}{str(ltr)}{RESET}'
    elif status == 'green':
        return f'{GREEN}{str(ltr)}{RESET}'
    elif status == 'grey':
        return f'{GREY}{str(ltr)}{RESET}'

#comparing the static list (target) and flexible list (user-typed) to check for differences, then calling colourltr() to mark the letters based on the differences
def comparelsts(src, flex):
    comparisonlst = []
    for i in range(len(src)):
        if i < len(flex):
            if src[i] == flex[i]:
                comparisonlst.append(colourltrvanilla(src[i], 'green'))
            else:
                if flex[i] == ' ':
                    comparisonlst.append(colourltrvanilla(src[i], 'red'))
                else:
                    comparisonlst.append(colourltrvanilla(flex[i], 'red'))
        else:
            comparisonlst.append(colourltrvanilla(src[i], 'grey'))
    return ''.join(comparisonlst)

#uses comparelsts() and adds the keyboard input with getkey()
def wordmaker(src):
    srclst = list(src)
    flexlst = []

    result = comparelsts(srclst, flexlst)
    replaceln(result)
    
    while True:
        k = getkey()

        if k == 'backspace' and flexlst:
            flexlst.pop()
        elif k == 'space':
            flexlst.append(' ')
        elif k == 'return':
            break
        elif k == 'esc':
            break
        elif k in {'tab', 'up', 'down', 'left', 'right'}:
            pass
        elif len(k) == 1:
            flexlst.append(k)

        result = comparelsts(srclst, flexlst)
        replaceln(result)

        if ''.join(flexlst) == src:
            break

#adds timer and ui
def game(sentence):
    global timerstatus, elapsed

    elapsed = 0
    timerstatus = True
    stopwatchthread = threading.Thread(target=stopwatch, daemon=True)
    stopwatchthread.start()

    wordmaker(sentence)

    timerstatus = False
    print('\n')
    print(f'{elapsed} seconds')
    print(f'avg wpm: {wpm(sentence,elapsed)}')
    print('\n')

#main
tmp = input('how many words? (N to kill): ')
if tmp == 'N':
    print('program killed')
else:
    print('\n')
    sen = randomsentence(int(tmp))
    game(sen)