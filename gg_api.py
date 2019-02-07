'''Version 0.2'''

import json
import nltk
import re
from heapq import nlargest
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords



OFFICIAL_AWARDS = ['cecil b. demille award', 
                    'best motion picture - drama',
                    'best performance by an actress in a motion picture - drama',
                    'best performance by an actor in a motion picture - drama',
                    'best motion picture - comedy or musical', 
                    'best performance by an actress in a motion picture - comedy or musical',
                    'best performance by an actor in a motion picture - comedy or musical',
                    'best animated feature film',
                    'best foreign language film',
                    'best performance by an actress in a supporting role in a motion picture',
                    'best performance by an actor in a supporting role in a motion picture',
                    'best director - motion picture',
                    'best screenplay - motion picture',
                    'best original score - motion picture',
                    'best original song - motion picture',
                    'best television series - drama',
                    'best performance by an actress in a television series - drama',
                    'best performance by an actor in a television series - drama',
                    'best television series - comedy or musical',
                    'best performance by an actress in a television series - comedy or musical',
                    'best performance by an actor in a television series - comedy or musical',
                    'best mini-series or motion picture made for television',
                    'best performance by an actress in a mini-series or motion picture made for television',
                    'best performance by an actor in a mini-series or motion picture made for television',
                    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


# Finds either a single host or 2 hosts (cohosts) in a list of strings
def get_hosts(tweets):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    corpus = tweets

    hostMentions = {}



    for tweet in corpus:
        if 'monologue' in tweet:
            word = ""
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in hostMentions:
                    hostMentions[match] = 1
                else:
                    num = hostMentions.get(match)
                    num = num + 1
                    update = {match : num}
                    hostMentions.update(update)
    hosts = nlargest(2, hostMentions, key=hostMentions.get)
    #print (hostMentions)
    freq1 = hostMentions.get(hosts[0])
    freq2 = hostMentions.get(hosts[1])
    
    if freq2 / (freq1 + freq2) > .3:
        return hosts
    else:
        return [hosts[0]]

def get_awards(tweets):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(tweets):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = {}

        
        

    return nominees

def get_winner(tweets):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    '''
    personName = {}
    corpus = tweets
    real_awards = OFFICIAL_AWARDS
    tknzr = RegexpTokenizer(r'\w+')
    for award in real_awards:
        for tweet in corpus:
            award_parse = tknzr.tokenize(award)
            if len(set(award_parse).intersection(set(tweet))) >= 3:
                #print("here")
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
        awardWinner = nlargest(5, personName, key=personName.get)
        print (award + " won by ")
        print (awardWinner)
        
    winners = {}
    winnersUnique = []
    corpus = tweets
    

    real_awards = OFFICIAL_AWARDS
    tknzr = RegexpTokenizer(r'\w+')
    for award in real_awards:
        award_parse = tknzr.tokenize(award)
        award_parse[:] = [x for x in award_parse if x not in award_stopwords]
        print (award_parse)
        keys = len(award_parse)
        for tweet in filteredTweets:
            if len(set(award_parse).intersection(set(tweet))) == keys - 1:
                tweet[:] = [x for x in tweet if x not in award_words]
                print(tweet)
    '''
    ##Going to try individually for awards, hard to generalize
    winners = {}
    
    
    condenseAwards = ['cecil demille award',
                        'best motion picture drama',
                        'best performace actress drama',
                        'best performace actor drama',
                        'best motion picture comedy musical',
                        'actress comedy musical performance',
                        'actor comedy musical performace',
                        'animated feature film',
                        'foreign language film',
                        'supporting actress best',
                        'best supporting actor',
                        'best director',
                        'best screenplay',
                        'best score',
                        'best original song',
                        'best TV series',
                        'actress TV series',
                        'actor TV series',
                        'TV series comedy musical',
                        'actress TV mucial comedy',
                        'actor TV musical comedy',
                        'TV mini series picture',
                        'actress mini picture TV',
                        'actor mini picture TV',
                        'actress supporting TV series',
                        'actor supporting TV series']

    personName = {}
    corpus = tweets
    real_awards = OFFICIAL_AWARDS
    tknzr = RegexpTokenizer(r'\w+')
    award_words = ['cecil', 'TV', 'Cecil', 'award', 'Award', 'Movie', 'movie', 'best', 'motion picture', 'drama', 'performance', 'actress', 'actor', 'comedy', 'feature', 'film', 'foreign', 'language', 'musical', 'animated', 'supporting', 'role', 'director', 'screenplay', 'original', 'score', 'song', 'television', 'series', 'mini-series', 'miniseries', 'Best', 'Motion', 'picture', 'motion', 'Picture', 'Drama', 'Performance', 'Actress', 'Actor', 'Comedy', 'Feature', 'Film', 'Foreign', 'Language', 'Musical', 'Animated', 'Supporting', 'Role', 'Director', 'Screenplay', 'Original', 'Score', 'Song', 'Television', 'Series', 'Mini-series', 'Miniseries']
    nominee = ['nominee', 'nominees', 'Nominees', 'Nominee']
    filteredTweets = []
    filteredTweetsTV = []
    TVtweets = ['TV']
    debug = ['best', 'performance', 'actor', 'drama']
    award_stopwords = ['by', 'an', 'in', 'a', 'or', 'made', 'for', 'best']
    for tweet in corpus:
        if len(set(award_words).intersection(set(tweet))) >= 2:
            #Not using this part yet
            if len(set(nominee).intersection(set(tweet))) >= 0:
                index = 0
                try:
                    index = 0 #tweet.index('for')
                except:
                    index = 0
                if index > 0:
                    tweet = tweet[0:index]
                #print (tweet)
                filteredTweets.append(tweet)
                if len(set(TVtweets).intersection(set(tweet))) >= 1:
                    filteredTweetsTV.append(tweet)


                    

    peopleAwards = ['director', 'actor', 'actress', 'cecil', 'Director', 'Actor', 'Actress', 'Cecil']
    TvAwards = ['TV']
    ignore = ['Nshowbiz', 'Best', 'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    #award_words.extend(ignore)
    for award in condenseAwards:
        personName = {}
        award_parse = award.split(' ')
        key = len(award_parse)
        if len(set(peopleAwards).intersection(set(award_parse))) >= 1:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'actor' in award_parse and 'actor' not in tweet:
                    continue
                if 'actress' in award_parse and 'actress' not in tweet:
                    continue
                if 'supporting' in award_parse and 'supporting' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #print(award_parse)
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = "best performace actor drama"
                    for w in tweet:
                        tweetText += w + " "
                    #print (tweetText)
                    if award == '':
                        print (tweetText)


                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)
            awardWinner = nlargest(1, personName, key=personName.get)
            print (award + " won by ")
            print (awardWinner)
        else:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'score' in award_parse and 'score' not in tweet:
                    continue
                if 'screenplay' in award_parse and 'screenplay' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #print(award_parse)
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = ""
                    for w in tweet:
                        tweetText += w + " "
                    #print (tweetText)


                    regex_match = re.findall("[A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)

                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)
            awardWinner = nlargest(1, personName, key=personName.get)
            print (award + " won by ")
            print (awardWinner)

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
    
    parse = parsing('gg2013.json')
    #print (get_hosts(parse))
    get_winner(parse)
    #get_nominees(parse)
    

    return


def parsing(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    #If you want to remove stop words, do so inside the function call
    #stop_words = stopwords.words('english')
    stop_words =['The', 'Variety', 'This', 'Globe', 'RT', 'CNNshowbiz', 'http', 'Golden', 'Globes', 'GoldenGlobes', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt' ]
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
## Don't need this, changed implementation to only use other parsing method
'''
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
    '''

if __name__ == '__main__':
    main()
