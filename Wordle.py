#nltk dependency for word bank, random for obviously pseudorandom choice
from nltk.corpus import words
from random import choice

realwordlst = set(words.words())

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

    for char in guess:
        guesslst +=char
    
    for i in range(len(guesslst)):
        if guesslst[i] in wordlst:
            if guesslst[i] == wordlst[i]:
                resultlst += ('🟩 ')
            else:
                resultlst  += ('🟨 ')
        else:
            resultlst += ('⬜️ ')

    return ''.join(resultlst)

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
        result = checkguess(guess)
        print(guess,result)

        if result == '🟩 🟩 🟩 🟩 🟩 ':
            break
        else:
            i = i + 1
            continue