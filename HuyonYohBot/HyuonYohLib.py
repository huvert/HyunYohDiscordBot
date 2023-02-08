import requests
import json
import os
from random import randint


def fetchRandomQuote():
    '''Fetch an random inspirational quote from API! Doc: https://zenquotes.io/api'''
    return requests.get('https://zenquotes.io/api/random').json()[0]["q"].upper()


def fetchTodaysQuote():
    '''Fetch an todays inspirational quote from API! Doc: https://zenquotes.io/api'''
    return requests.get('https://zenquotes.io/api/today').json()[0]["q"].upper()
    

def getVocabulary():
    '''Return dataobject from JSON file'''
    path = os.getcwd()
    file = open(f'{path}\HuyonYohBot\HyuonYohVocabulary.json')
    vocabulary = json.load(file)
    file.close()
    return vocabulary


def doubleLetters(word):
    '''Check for double letters (Dobbelkonsonant)'''
    for i in range (len(word)-1):
        if word[i] == word[i+1]:
            return f"{word[:i]}{word[i+1:]}"
    return word


def rapeWordEnding(word):
    '''Misspronounce words like HAPPENING --> HAPPENINGING'''
    if word[-3:] == "ING":
        return f"{word[:-3]}INING"
    return word


def hyunYohify(quote):
    '''Returns a quote in Hyuon Yoh style'''
    vocabulary = getVocabulary()
    for i, word in enumerate(quote):
        try:
            print(f'Word: {word}')
            sign = 0
            if word[-1] in ['.', ',' , ';', ':', '!', '?']:
                sign = word[-1]     #Store last index to sign
                word = word[:-1]    #Remove last index

            if word in vocabulary:
                if len(vocabulary[word]) == 1:
                    word = vocabulary[word][0]
                else:
                    r = randint(1, len(vocabulary[word])) # 1 .. end
                    word = vocabulary[word][r-1]

            elif word[-1] == 'S':
                word = word[:-1] #Strip S away
                sign = 'S'       #Store the S for later
                if word in vocabulary:
                    if len(vocabulary[word]) == 1:
                        word = vocabulary[word][0]
                    else:
                        r = randint(1, len(vocabulary[word])) # 1 .. end
                        word = vocabulary[word][r-1]

            else: 
                if randint(0,100) > 20:   #chance to misspell words like BECOMING --> BECOMINING
                    word = rapeWordEnding(word)

                if randint(0,100) > 20:   #chance to misspell doubel letters
                    word = doubleLetters(word)

                if randint(0,100) > 20:   #change to misspell "TH"
                    if "TH" in word:
                        if randint(0,100) > 50:
                            word = word.replace("TH", "T") #WORT --> WORT
                        else:
                            word = word.replace("TH", "HT") #WORT --> WORHT
                
                if randint(0,100) > 20:   #Chance to misspell EA
                    if "EA" in word:
                        if randint(0,100) > 50:
                            word = word.replace("EA", "E") #DREAMS --> DREMS
                        else:
                            word = word.replace("EA", "AE") #DREAMS --> DRAEMS

                if randint(0,100) > 20:   #Chance to misspell OU 
                    if "OU" in word:
                        if randint(0,100) > 50:
                            word = word.replace("OU", "O") #AROUND --> AROND
                        else:
                            word = word.replace("OU", "UO") #AROUND --> ARUOND

                if randint(0,100) > 20:   #Chance to misspell CH
                    if "CH" in word:
                        if randint(0,100) > 50:
                            word = word.replace("CH", "SH") #AROUND --> AROND


            if sign != 0:
                word = f"{word}{sign}" #Add sign back to word
            
            quote[i] = word     #Write word back to quote
        except:
            print("[HYUNYOIFY] error at line 106")
    quote = ' '.join(quote)
    return quote


def getHyonYohQuote(type = "random"):
    '''Gets a HyuonYohified quote'''
    if type == "random":
        quote = fetchRandomQuote()
    elif type == "today":
        quote = fetchTodaysQuote()
    else:
        quote = fetchTodaysQuote()
    #quote = "HAPPENING HAPPENING BECOMING BECOMING BECOMING HAPPENING"
    quote = quote.replace("'","") #Hyon Yoh doesnt use '
    quote = list(quote.split(" "))
    return hyunYohify(quote)


def getHyonYohSource():
    '''Fetch a random source from JSON file'''
    path = os.getcwd()
    file = open(f'{path}\HuyonYohBot\HyuonYohSources.json')
    source = json.load(file)["SOURCES"]
    file.close()
    r = randint(0,len(source)-1)
    return source[r]


def getHyuonYohMessage(type = "random"):
    quote = getHyonYohQuote(type = "random")
    source = getHyonYohSource()
    return f"{quote}\n\n~{source}"


if __name__ == "__main__":
    #quote = "How you think is as important as whats you think.".upper()
    quote = getHyonYohQuote()
    #print(quote)
    source = getHyonYohSource()
    #print(source)
    hyuonYohPost = f"{quote}\n\n~{source}"
    print(hyuonYohPost)
    
