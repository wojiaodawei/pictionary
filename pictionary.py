import random
import time
import sys
import signal

words = list()
teamNames = list()

abort = False
def stop(sig, stack):
    global abort
    print("Got signal!")
    abort = True

signal.signal(signal.SIGINT, stop)

def timer(secs=60):
    global abort
    stopped = False
    input("READY? (press ENTER) ")
    abort = False
    for t in range(secs):
        sys.stdout.write('\r{:10}\t{:4}'.format("Timer:", t))
        sys.stdout.flush()
        time.sleep(1)
        if abort:
            abort = False
            stopped = True
            break
    if not stopped:
        sys.stdout.write('\r{:15}'.format("Time's up!",))
    sys.stdout.flush()


def create_players():
    time.sleep(1)
    print("\n..... WHO PLAYS? .....")
    players = list()
    ok = False
    while not ok:
        try:
            nbPlayers = int(input("Number of players: "))
            if nbPlayers >= 4:
                ok = True
            else:
                print("Minimum 4 players")
        except:
            print("Please enter a number")
    for i in range(nbPlayers):
        players.append(input("Name of Player " + str(i + 1) + ": ")) 
    return players

def create_teams(players, numberOfTeams=2):
    global teamNames
    time.sleep(1)
    print("\n..... TEAM CREATION .....")
    teams = [[]] * numberOfTeams
    i = 0
    while len(players) > 0:
        j = random.choice(players)
        teams[i % numberOfTeams] = teams[i % numberOfTeams] + [j]
        i += 1
        players.remove(j)
    for i, e in enumerate(teams):
        print("Team", i + 1, ':')
        for j in e:
            time.sleep(.5)
            print("\t", j)
    for eq in range(numberOfTeams):
        teamNames.append(input("Name of the team " + str(eq + 1) + ": ")) 
    return teams

def load_words():
    global words
    print("..... LOADING THE WORDS TO GUESS .....")
    wordsAlreadyPlayed = list()
    for w in open("backup/picmemo.txt", 'r').readlines():
        wordsAlreadyPlayed.append(w.strip().lower())
        
    basic_words = list()
    for lvl in range(1, 6):
        for w in open("words/picwords" + str(lvl) + ".txt", 'r').readlines():
            m = w.strip().lower()
            if m not in wordsAlreadyPlayed:
                basic_words.append(m)
    words = list(set(basic_words))
    print(len(words), "new words to guess!")

def picking():
    global words
    localWords = list()
    skip = 0
    ok = False
    input("PICK A WORD (press ENTER)")
    while not ok and skip < 3:
        if len(words) > 0:
            word = random.choice(words)
            words.remove(word)
            localWords.append(word)
            print(word)
            decision = input("OK (press ENTER) or enter 'skip' (/!\\ " + str(2 - skip) + " skipping left)\n")
            if 'skip' in decision:
                skip += 1
            else:
                ok = True
        else:
            return None
    with open("backup/picmemo.txt", 'a') as f:
        for w in localWords:
            f.write(w+'\n')
    if not ok:
        return False
    return word
    
def play(teams, scoreLimit=10):
    global teamNames
    print("\n..... LAUNCHING THE GAME .....")
    time.sleep(1)
    load_words()
    end = False
    scores = [0] * len(teams)
    i = 0
    while not end:
        print("//////  SCORES  \\\\\\\\\\\\")
        for s, t in enumerate(scores):
              print("TEAM", teamNames[s], ":", t, "points")
        j = i % len(teams)
        print("\n", teamNames[j], " => YOUR TURN!")
        team = teams[j]
        print(team[0], "is the drawer!")
        teams[j] = team[1:] + [team[0]]
        word = picking()
        if word == False:
            i += 1
            j = i % len(teams)
            scores[j] += 1
            if scores[j] >= scoreLimit:
                checkGap = True
                for u in range(1, len(teams)):
                    if not (scores[j] - 1 > scores[(j + u) % len(teams)]):
                        checkGap = False
                if checkGap:
                    end = True
                    print("END OF THE GAME!!!")
                    print(teamNames[j], "are the best, CONGRATS!!!")
        elif word == None:
            end = True
            print("So sorry, end of the game, sadly no more words to play with")
        else:
            print(chr(27) + "[2J")
            timer()
            print("The word to guess was:", word)
            next = False
            while not next:
                victory = input("Good guess? (enter y or n) ")
                if 'y' in victory:
                    next = True
                    scores[j] += 1
                    i = i + 1
                elif 'n' in victory:
                    i = i + 1
                    next = True
            if scores[j] >= scoreLimit:
                checkGap = True
                for u in range(1, len(teams)):
                    if not (scores[j] - 1 > scores[(j + u) % len(teams)]):
                        checkGap = False
                if checkGap:
                    end = True
                    print("END OF THE GAME!!!")
                    print(teamNames[j], "are the best, CONGRATS!!!")

if __name__ == "__main__":
    players = create_players()
    teams = create_teams(players)
    play(teams)
