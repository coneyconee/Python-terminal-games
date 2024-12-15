#nltk dependency for word bank, random for obviously pseudorandom choice
from nltk.corpus import words
from random import choice

realwordlst = set(words.words())

#ansi colour consts
GREEN = '\033[32m'
YELLOW = '\033[33m'
GREY = '\033[90m'
RESET = '\033[0m'

#colour letters without external libaries
def colourltrvanilla(ltr,status):
    global GREEN,YELLOW,GREY,RESET

    if status == 'green':
        return f'{GREEN}{str(ltr)}{RESET}'
    elif status == 'yellow':
        return f'{YELLOW}{str(ltr)}{RESET}'
    elif status == 'grey':
        return f'{GREY}{str(ltr)}{RESET}'

#word validation using nltk words
def validateword(word):
    if len(word) != 5:
        print(word,'is not a 5 letter word!')
        return False
    for char in word:
        try:
            int(char)
        except ValueError:
            if word in realwordlst:
                str(word).lower()
                return True
            else:
                print(word,'is not a registered word!')
                return False
        else:
            print(word,'has special characters!')
            return False

#random word of the day
print(f'\nWelcome to {colourltrvanilla('Wordle','green')}!\nYou have 6 tries to guess a 5 letter word.\n')

word = str(choice([word for word in realwordlst if len(word) == 5])).lower()

wordlst = []

for char in word:
    wordlst += char

#i dont want to comment this
def validateguess(guess):
    if guess in tried:
        print(guess,'has been tried already!')
        return False
    if len(guess) != 5:
        print(guess,'is not a 5 letter word!')
        return False
    for char in guess:
        try:
            int(char)
        except ValueError:
            if guess in realwordlst:
                return True
            else:
                print(guess,'is not a registered word!')
                return False
        else:
            print(guess,'has special characters!')
            return False

#same idea as the monkeytype; two lists that compare with iteration
def checkguess(guess):

    resultlst = []
    guesslst = []
    tmpguesslst = []

    for char in guess:
        guesslst +=char
    
    for i in range(len(guesslst)):
        if guesslst[i] in wordlst:
            if guesslst[i] == wordlst[i]:
                resultlst += ('🟩 ')
                tmpguesslst.append(colourltrvanilla(guesslst[i],'green'))
            else:
                resultlst  += ('🟨 ')
                tmpguesslst.append(colourltrvanilla(guesslst[i],'yellow'))
        else:
            resultlst += ('⬜️ ')
            tmpguesslst.append(colourltrvanilla(guesslst[i],'grey'))

    return (''.join(resultlst)), str(''.join(tmpguesslst))

i = 0

tried = []

#game
while True:

    if i == 6:
        print('the word was', word, '!')
        break

    guess = input('guess: ')

    guess.lower

    if guess == 'n':
        print('session ended')
        break

    if validateguess(guess) == False:
        continue


    if validateguess(guess) == True:
        tried.append(guess)
        result,textresult = checkguess(guess)
        print(textresult)

        if result == '🟩 🟩 🟩 🟩 🟩 ':
            break
        else:
            i = i + 1
            continue
