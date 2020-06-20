import random
import time
import sys
import signal

abort = False
def stop(sig, stack):
    global abort
    print("Got signal!")
    abort = True

signal.signal(signal.SIGINT, stop)

words = list()
nomsEquipes = list()

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

def constitution_equipes(joueurs, nbEquipes):
    global nomsEquipes
    time.sleep(1)
    print("\n..... TEAM CREATION .....")
    equipes = [[]] * nbEquipes
    i = 0
    while len(joueurs) > 0:
        j = random.choice(joueurs)
        equipes[i % nbEquipes] = equipes[i % nbEquipes] + [j]
        i += 1
        joueurs.remove(j)
    for i, e in enumerate(equipes):
        print("Team", i + 1, ':')
        for j in e:
            time.sleep(.5)
            print("\t", j)
    for eq in range(nbEquipes):
        nomsEquipes.append(input("Name of the team " + str(eq + 1) + " : ")) 
    return equipes

def chargementMots():
    global words
    print("..... LOADING THE WORDS TO GUESS .....")
    motsDejaJoues = list()
    for w in open("backup/picmemo.txt", 'r').readlines():
        motsDejaJoues.append(w.strip().lower())
        
    basic_words = list()
    for lvl in range(1, 6):
        for w in open("words/picwords" + str(lvl) + ".txt", 'r').readlines():
            m = w.strip().lower()
            if m not in motsDejaJoues:
                basic_words.append(m)
    words = list(set(basic_words))
    print(len(words), "new words to guess!")

def picking():
    global words
    words_loc = list()
    skip = 0
    ok = False
    input("PICK A WORD (press ENTER)")
    while not ok and skip < 3:
        if len(words) > 0:
            word = random.choice(words)
            words.remove(word)
            words_loc.append(word)
            print(word)
            decision = input("OK (press ENTER) or enter 'skip' (/!\\ " + str(2 - skip) + " skipping left)\n")
            if 'skip' in decision:
                skip += 1
            else:
                ok = True
        else:
            return None
    with open("backup/picmemo.txt", 'a') as f:
        for w in words_loc:
            f.write(w+'\n')
    if not ok:
        return False
    return word
    
def jeu(equipes, scoreLimite=10):
    global nomsEquipes
    print("\n..... LAUNCHING THE GAME .....")
    time.sleep(1)
    chargementMots()
    fin = False
    scores = [0] * len(equipes)
    i = 0
    while not fin:
        print("//////  SCORES  \\\\\\\\\\\\")
        for s, t in enumerate(scores):
              print("TEAM", nomsEquipes[s], ":", t, "points")
        j = i % len(equipes)
        print("\n", nomsEquipes[j], " => YOUR TURN!")
        team = equipes[j]
        print(team[0], "is the drawer!")
        equipes[j] = team[1:] + [team[0]]
        word = picking()
        if word == False:
            i += 1
            j = i % len(equipes)
            scores[j] += 1
            if scores[j] >= scoreLimite:
                verif_ecart = True
                for u in range(1, len(equipes)):
                    if not (scores[j] - 1 > scores[(j + u) % len(equipes)]):
                        verif_ecart = False
                if verif_ecart:
                    fin = True
                    print("END OF THE GAME!!!")
                    print(nomsEquipes[j], "are the best, CONGRATS!!!")
        elif word == None:
            fin = True
            print("So sorry, end of the game, sadly no more words to play with")
        else:
            print(chr(27) + "[2J")
            timer()
            print("The word to guess was:", word)
            suite = False
            while not suite:
                victoire = input("Good guess? (enter y or n) ")
                if 'y' in victoire:
                    suite = True
                    scores[j] += 1
                    i = i + 1
                elif 'n' in victoire:
                    i = i + 1
                    suite = True
            if scores[j] >= scoreLimite:
                verif_ecart = True
                for u in range(1, len(equipes)):
                    if not (scores[j] - 1 > scores[(j + u) % len(equipes)]):
                        verif_ecart = False
                if verif_ecart:
                    fin = True
                    print("END OF THE GAME!!!")
                    print(nomsEquipes[j], "are the best, CONGRATS!!!")
    
joueurs = ["Sofi", "Lucas", "Sara", "David"]
nbEquipes = 2

equipes = constitution_equipes(joueurs, nbEquipes)

jeu(equipes)
