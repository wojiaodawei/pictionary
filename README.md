# Pictionary

~~ *This project was implemented in May 2020* ~~

*During the lockdown period, in the countryside, cut off from the Internet, I took 2 hours of my time to code this game in order to entertain my friends and I for several evenings.*

Execute in a terminal:
```
$ python3 pictionary.py
```

**Rules:**
* 581 words to guess
* 2 teams
* minimum 4 players
* the players are randomly and evenly assigned to a team
* first to 10 points wins (2 pts gap)
* 1 minute to make your teammates guess the word
* teams take turns playing a word

If the word is found before the time has elapsed, it is possible to stop the countdown and move on to the next guess, simply by using the keyboard shortcut *Ctrl+C*.

In order to play several games with only new words, the words already played are saved in a file *backup/picmemo.txt*. You can clean this file whenever you want. 


