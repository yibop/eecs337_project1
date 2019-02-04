'''Version 0.2'''

import json
import nltk
import re
from heapq import nlargest
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


# Finds either a single host or 2 hosts (cohosts) in a list of strings
def get_hosts(tweets):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    corpus = tweets

    hostMentions = {}

    for tweet in corpus:
        if "open" in tweet:

            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweet)

            for match in regex_match:
                if not match in hostMentions:
                    hostMentions[match] = 1
                else:
                    num = hostMentions.get(match)
                    num = num + 1
                    update = {match : num}
                    hostMentions.update(update)
    hosts = nlargest(2, hostMentions, key=hostMentions.get)

    freq1 = hostMentions.get(hosts[0])
    freq2 = hostMentions.get(hosts[1])

    if freq2 / (freq1 + freq2) > .4:
        return hosts
    else:
        return [hosts[0]]

def get_awards(tweets):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(tweets):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    winners = {}
    personName = {}
    corpus = tweets


    for award in OFFICIAL_AWARDS:
        winners[award] = ""

    award_words = ['best', 'motion picture', 'winner', 'drama', 'performance', 'actress', 'actor', 'comedy', 'feature', 'film', 'foreign', 'language', 'musical', 'animated', 'supporting', 'role', 'director', 'screenplay', 'original', 'score', 'song', 'television', 'series', 'mini-series', 'miniseries', 'Best', 'Motion', 'picture', 'motion', 'Picture', 'Winner', 'Drama', 'Performance', 'Actress', 'Actor', 'Comedy', 'Feature', 'Film', 'Foreign', 'Language', 'Musical', 'Animated', 'Supporting', 'Role', 'Director', 'Screenplay', 'Original', 'Score', 'Song', 'Television', 'Series', 'Mini-series', 'Miniseries']

    for tweet in corpus:
        if len(set(award_words).intersection(set(tweet))) >= 2:
            for word in tweet:
                if word in award_words:
                    tweet[:] = [x for x in tweet if x not in award_words]
            tweetText = ""
            for w in tweet:
                tweetText += w + " "

            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

            for match in regex_match:
                if not match in personName:
                    personName[match] = 1
                else:
                    num = personName.get(match)
                    num = num + 1
                    update = {match : num}
                    personName.update(update)
    hosts = nlargest(24, personName, key=personName.get)

    print (hosts)

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print ("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    
    
    #print ((hostParse('gg2013.json')))
    get_winner(parsing('gg2013.json'))

    return


def parsing(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    #stop_words = stopwords.words('english')
    stop_words =['RT', 'http', 'Golden', 'Globes', 'GoldenGlobes', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt' ]
    #stop_words.extend(track)
    tknzr = RegexpTokenizer(r'\w+')

    word_list = []
    
    for tweet in data:
        text = tweet['text']  
        words = tknzr.tokenize(text)
        tweetText = []
        for w in words:
            if w not in stop_words:
                tweetText.append(w)
        word_list.append(tweetText)
    return word_list


## Need to parse without using stop words for finding the Host (still need the GG specific words)
def hostParse(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    
    track=['Golden', 'Globes', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt' ]
    
    tknzr = RegexpTokenizer(r'\w+')

    word_list = []
    
    for tweet in data:
        text = tweet['text']  
        words = tknzr.tokenize(text)
        tweetText = ""
        for w in words:
            if w not in track:
                tweetText += w + " "
        word_list.append(tweetText)
    return word_list

if __name__ == '__main__':
    main()
