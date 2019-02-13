'''Version 0.2'''

import json
import nltk
import re
import itertools
from heapq import nlargest
#nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from difflib import SequenceMatcher




OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 
                        'best motion picture - drama', 
                        'best performance by an actress in a motion picture - drama', 
                        'best performance by an actor in a motion picture - drama', 
                        'best motion picture - comedy or musical', 
                        'best performance by an actress in a motion picture - comedy or musical', 
                        'best performance by an actor in a motion picture - comedy or musical', 
                        'best animated feature film', 'best foreign language film', 
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
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 
                        'best motion picture - musical or comedy', 
                        'best performance by an actress in a motion picture - drama', 
                        'best performance by an actor in a motion picture - drama', 
                        'best performance by an actress in a motion picture - musical or comedy', 
                        'best performance by an actor in a motion picture - musical or comedy', 
                        'best performance by an actress in a supporting role in any motion picture', 
                        'best performance by an actor in a supporting role in any motion picture', 
                        'best director - motion picture', 
                        'best screenplay - motion picture', 
                        'best motion picture - animated', 
                        'best motion picture - foreign language', 
                        'best original score - motion picture', 
                        'best original song - motion picture', 
                        'best television series - drama', 
                        'best television series - musical or comedy', 
                        'best television limited series or motion picture made for television', 
                        'best performance by an actress in a limited series or a motion picture made for television', 
                        'best performance by an actor in a limited series or a motion picture made for television', 
                        'best performance by an actress in a television series - drama', 
                        'best performance by an actor in a television series - drama', 
                        'best performance by an actress in a television series - musical or comedy',
                        'best performance by an actor in a television series - musical or comedy', 
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
                        'cecil b. demille award']


# Finds either a single host or 2 hosts (cohosts) in a list of strings
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    string = 'gg' + str(year) + '.json'
    parse = parsing(string)

    corpus = parse

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

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    end_words = ['Drama', 'Musical', 'Film', 'Television', 'Motion Picture']
    key_words = end_words + ['performance', 'comedy', 'series', 'role', 'Performance', 'Comedy', 'Series', 'Role']

    # Parsing 

    string = 'gg' + str(year) + '.json'
    
    try:
        with open(string) as data_file:
            data = json.load(data_file)
    except:
        pass

    #stop_words = stopwords.words('english')
    stop_words =['The', 'Variety', 'This', 'Globe', 'RT', 'CNNshowbiz', 'http', 'Golden', 'Globes', 'GoldenGlobes', 'Goldenglobes', 'Goldenglobe', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt', '2013', '2015' ]

    tknzr = RegexpTokenizer(r'\w+')

    word_list = []
    word_dic = {}
    
    for tweet in data:
        text = tweet['text']
        id = tweet['id']

        '''  
        words = tknzr.tokenize(text)
        for w in words:
            if w in stop_words:
                words.remove(w)
        word_list.append(words)
        '''

        word_list.append((text,id))

    corpus = word_list

    # End of Parsing

    prev_ID = 1
    temp_awards = {}
    count = 0
    for tweet in corpus:
        for endWord in end_words:
            # Extract the segment between 'Best' and one of the end_words
            match = re.search(r'(?<=\sBest).*(?='+ endWord +')', tweet[0], re.IGNORECASE)
            if match:
                award = 'Best'+ match.group(0) + endWord

                # Remove duplicate segments from the same teweet
                if prev_ID == tweet[1]:
                    continue
                prev_ID = tweet[1]

                # Remove stopwords from the segment
                words = tknzr.tokenize(award)
                for w in words:
                    if w in stop_words:
                        award = award.replace(w, '')
        
                if (len(words) >= 4) :
                    if endWord not in temp_awards:
                        temp_awards[endWord] = [award]
                    else:
                        temp_awards[endWord].append(award)
                        #print(award)
                    count = count + 1


    '''
    #k = 0
    #for k in temp_awards:
    k = 'Motion Picture'
    sim_dic = {}
    i = 0
    while i < len(temp_awards[k]):
        tweet1 = temp_awards[k][i]
        j = i + 1
        print (i)
        while j < len(temp_awards[k]):
            tweet2 = temp_awards[k][j]
            sim = SequenceMatcher(None, tweet1, tweet2).ratio()
            #print (i)
            #print (sim)
            if sim > 0.85:   
                if tweet1 in sim_dic:
                    sim_dic[tweet1] = sim_dic[tweet1]+ 1
                else:
                    sim_dic[tweet1] = 1

                if tweet2 in sim_dic:
                    sim_dic[tweet2] = sim_dic[tweet2]+ 1
                else:
                    sim_dic[tweet2] = 1
            if tweet1 in sim_dic:
                sim_dic[tweet1][1] = sim_dic[tweet1][1] + 1
                sim_dic[tweet1][0] = (sim_dic[tweet1][0] + sim) / sim_dic[tweet1][1]
            else:
                temp_tup = [sim,1]
                sim_dic[tweet1] = temp_tup

            if tweet2 in sim_dic:
                sim_dic[tweet2][1] = sim_dic[tweet2][1] + 1
                sim_dic[tweet2][0] = (sim_dic[tweet2][0] + sim) / sim_dic[tweet2][1]
            else:
                temp_tup = [sim,1]
                sim_dic[tweet2] = temp_tup
            j = j + 1
        i = i + 1 

        '''
    
    result = []
    for k in temp_awards:
        dic = {}
        p = 0
        while p < len(temp_awards[k]):
            tweet = temp_awards[k][p]
            if tweet in dic:
                dic[tweet] = dic[tweet] + 1
            else:
                dic[tweet] = 1
            p = p+1

        dic_list= sorted(dic.items(), key=lambda x:x[1], reverse = True)
        #stackoverflow.com/questions/16772071/sort-dic-by-value-python

        # dic_list is acutally a list of tuple!!!!!
        dic_list = dic_list[:15]
        #print (dic)
        #print ('\n\n')

        award_list = []
        
        for item in dic_list:
            award_list.append(item[0])
        
        
        #print (award_list)

        remove_list = []

        i = 0
        for tweet1 in award_list:
            j = i + 1

            while j < len(award_list):
                tweet2 = award_list[j]
                sim = SequenceMatcher(None, tweet1, tweet2).ratio()

                if sim > 0.85 and (('actor' not in tweet1 and 'actor' not in tweet2) or ('actress' not in tweet2 and 'actress' not in tweet1)):
                    if (dic[tweet1] > dic[tweet2]):
                        #award_list.remove(tweet2)
                        remove_list.append(tweet2)
                    else:
                        #award_list.remove(tweet1)
                        remove_list.append(tweet1)

                j = j + 1
            i = i + 1
        
        remove_list = set(remove_list)
        for tweet in award_list:
            if tweet in remove_list:
                award_list.remove(tweet)
        
        
        #print (award_list)
        #print ('\n\n')
        result.append(award_list)
    
    result[0] = result[0][:6]
    result[1] = result[1][:6]
    result[2] = result[2][:5]
    result[3] = result[3][:6]
    result[4] = result[4][:2]

    awards = []
    for i in result:
        for j in i:
            print (j.lower())
            awards.append(j.lower())

    #print (sorted(sim_dic.items(), key=lambda x:x[1], reverse = True))
    #print (count)
    #awards = sorted(sim_dic, key = sim_dic.get, reverse = True)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = {}

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse
    
    if year == 2013 or year == 2015:
        real_awards = OFFICIAL_AWARDS_1315
    else:
        real_awards = OFFICIAL_AWARDS_1819

    # Use correct year tho
    for award in real_awards:
        nominees[award] = ['sample']

    return nominees
        

def get_winner(year):
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
    
    #Need to make new condensed awards list
    
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

    award_stopList = ['drama', '-', 'by', 'an', 'a', 'in', 'made', 'for', 'role', 'or', 'b.', 'series,', 'performance', 'best']

    personName = {}
    
    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse
    if year == 2013 or year == 2015:
        real_awards = OFFICIAL_AWARDS_1315
    else:
        real_awards = OFFICIAL_AWARDS_1819
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
    ignore = ['Supporting', 'Actress', 'Actor', 'Series', 'Nshowbiz', 'Best', 'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    #award_words.extend(ignore)
    count = 0
    for award in real_awards:
        personName = {}
        award_parse = award.split(' ')
        for stop in award_stopList:
            while stop in award_parse:
                award_parse.remove(stop)
        if 'television' in award_parse:
            award_parse.remove('television')
            award_parse.append('TV')
        if 'mini-series' in award_parse:
            award_parse.remove('mini-series')
            award_parse.append('series')
        if len(award_parse) >=5:
            while 'motion' in award_parse:
                award_parse.remove('motion')
            while 'picture' in award_parse:
                award_parse.remove('picture')

        #print (award_parse)
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
                if 'supporting' not in award_parse and 'supporting' in tweet:
                    continue
                if 'director' in award_parse and 'director' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #print(award_parse)
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = ""
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
            print (awardWinner)
            print (real_awards[count])
            winners[real_awards[count]] = awardWinner[0]
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
                                num = num + 1.1
                                update = {match : num}
                                personName.update(update)
            awardWinner = nlargest(1, personName, key=personName.get)
            print (awardWinner)
            print (real_awards[count])
            try:
                winners[real_awards[count]] = awardWinner[0]
            except:
                winners[real_awards[count]] = ""
        count = count + 1

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = {}

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse
    
    if year == 2013 or year == 2015:
        real_awards = OFFICIAL_AWARDS_1315
    else:
        real_awards = OFFICIAL_AWARDS_1819

    # Use correct year tho
    for award in real_awards:
        presenters[award] = ['sample']

    return presenters


def get_bestDressed(year):
    '''Best Dressed is list of a strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse

    bestDressed = {}
    
    keys = ['best', 'dressed', 'Best', 'Dressed', 'Red', 'Carpet', 'red', 'carpet', 'amazing', 'Amazing', 'dress', 'Dress', 'stunning', 'Stunning']

    for tweet in corpus:
        if len(set(tweet).intersection(set(keys))) >= 4:
            #print (tweet)
            word = ""
            tweet[:] = [x for x in tweet if x not in keys]
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in bestDressed:
                    bestDressed[match] = 1
                else:
                    num = bestDressed.get(match)
                    num = num + 1
                    update = {match : num}
                    bestDressed.update(update)
    person = nlargest(1, bestDressed, key=bestDressed.get)
    #print (bestDressed)
    
    return person

def get_worstDressed(year):
    '''Best Dressed is list of a strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    
    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse

    worstDressed = {}
    
    keys = ['ugly', 'dress']

    for tweet in corpus:
        if len(set(tweet).intersection(set(keys))) >= 2:
            #print (tweet)
            word = ""
            tweet[:] = [x for x in tweet if x not in keys]
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in worstDressed:
                    worstDressed[match] = 1
                else:
                    num = worstDressed.get(match)
                    num = num + 1
                    update = {match : num}
                    worstDressed.update(update)
    person = nlargest(1, worstDressed, key=worstDressed.get)
    #print (worstDressed)
    
    return person



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
    

    
    #get_winner(2015)
    print (get_worstDressed(2013))
    print (get_bestDressed(2013))

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
