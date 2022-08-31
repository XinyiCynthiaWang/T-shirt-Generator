import nltk
from nltk import WhitespaceTokenizer
import random
from nltk.corpus import wordnet
from time import time


color = ["white", "yellow"]
on_color = ["on_red", "on_magenta", "on_blue", "on_grey"]

def generate_slogan(topic):
    def tags(tag):
        if tag in {"NNP","NNS","NN","NNPS"}:
            POS_tag = 'noun'
        elif tag in {'VB','VBD','VBG','VBN','VBP','VBZ'}:
            POS_tag = 'verb'
        elif tag in {'RB','RBR','RBS','WRB', 'RP'}:
            POS_tag = 'adverb'
        elif tag in {'PRP','PRP$'}:
            POS_tag = 'pronoun'
        elif tag in {'JJ','JJR','JJS'}:
            POS_tag = 'adjective'
        elif tag == 'IN':
            POS_tag = 'preposition'
        elif tag == 'WDT':
            POS_tag = 'determiner'
        elif tag in {'WP','WP$'}:
            POS_tag = 'pronoun'
        elif tag == 'UH':
            POS_tag = 'interjection'
        elif tag == 'POS':
            POS_tag = 'possesive ending'
        elif tag == 'SYM':
            POS_tag = 'symbol'
        elif tag == 'EX':
            POS_tag = 'existential there'
        elif tag == 'DT':
            POS_tag = 'determiner'
        elif tag == 'MD':
            POS_tag = 'modal'
        elif tag == 'LS':
            POS_tag = 'list item marker'
        elif tag == 'FW':
            POS_tag = 'foreign word'
        elif tag == 'CC':
            POS_tag = 'coordinating conjunction '
        elif tag == 'CD':
            POS_tag = 'cardinal number'
        elif tag == 'TO':
            POS_tag = 'to'
        elif tag == '.':
            POS_tag = 'line ending'
        elif tag == ',':
            POS_tag = 'comma'
        else:
            POS_tag = tag
        return POS_tag

    def POS_tagger(words):
        taggedwordlist = nltk.pos_tag(words)

        taglist = [pos for word,pos in taggedwordlist]
        POS_tags = []

        for item in taggedwordlist:
            postag = tags(item[1])
            POS_tags.append([item[0], postag])

        return POS_tags

    def givemeone(postag, allthewords):
        filtered = []
        for wordgroup in allthewords:
            if wordgroup[1] == postag:
                filtered.append(wordgroup[0])
        return random.choice(filtered)

    def alltags(allthewords):
        return [t[1] for t in allthewords]

    def doslogan1():
        transcript = open('static/vocabulary/transcription.txt').read()
        words = WhitespaceTokenizer().tokenize(transcript)
        tagged = POS_tagger(words)

        tags = alltags(tagged)

        newlist = []
        structure1 = ['verb', 'noun', 'determiner', 'verb', 'determiner', random.choice(syns)]
        for index, item in enumerate(structure1):
            if item in tags:
                one = givemeone(item, tagged)
                newlist.append(one)
            else:
                newlist.append(item)
        return (' '.join(newlist))


    def doslogan2():
        transcript = open('static/vocabulary/transcription.txt').read()
        words = WhitespaceTokenizer().tokenize(transcript)
        tagged = POS_tagger(words)

        tags = alltags(tagged)

        newlist = []
        structure1 = ['verb', 'preposition', 'determiner', random.choice(syns)]
        for index, item in enumerate(structure1):
            if item in tags:
                one = givemeone(item, tagged)
                newlist.append(one)
            else:
                newlist.append(item)

        return (' '.join(newlist))


    def doslogan3():
        transcript = open('static/vocabulary/transcription.txt').read()
        words = WhitespaceTokenizer().tokenize(transcript)
        tagged = POS_tagger(words)

        tags = alltags(tagged)

        newlist = []
        structure1 = ['adjective', 'determiner', random.choice(syns)]
        for index, item in enumerate(structure1):
            if item in tags:
                one = givemeone(item, tagged)
                newlist.append(one)
            else:
                newlist.append(item)

        return (' '.join(newlist))



    def doslogan4():
        transcript = open('static/vocabulary/transcription.txt').read()
        words = WhitespaceTokenizer().tokenize(transcript)
        tagged = POS_tagger(words)

        tags = alltags(tagged)

        newlist = []
        structure1 = [random.choice(syns), 'determiner', 'noun']
        for index, item in enumerate(structure1):
            if item in tags:
                one = givemeone(item, tagged)
                newlist.append(one)
            else:
                newlist.append(item)

        return (' '.join(newlist))



    def doslogan5():
        transcript = open('static/vocabulary/transcription.txt').read()
        words = WhitespaceTokenizer().tokenize(transcript)
        tagged = POS_tagger(words)

        tags = alltags(tagged)

        newlist = []
        structure1 = [random.choice(syns), 'preposition', 'noun']
        for index, item in enumerate(structure1):
            if item in tags:
                one = givemeone(item, tagged)
                newlist.append(one)
            else:
                newlist.append(item)

        return (' '.join(newlist))

    result_slogans = []
    if topic == None:
        syns = []
        syns.append('noun')
        for _ in range(0,5):
            result_slogans.append(doslogan1())
            result_slogans.append(doslogan2())
            result_slogans.append(doslogan3()) 
            result_slogans.append(doslogan4()) 
            result_slogans.append(doslogan5())
    elif topic != None:
        syns = []
        for syn in wordnet.synsets(topic):
        
            for lemma in syn.lemmas():
        
                syns.append(lemma.name())
        for _ in range(0,5):
            result_slogans.append(doslogan1())
            result_slogans.append(doslogan2()) 
            result_slogans.append(doslogan3()) 
            result_slogans.append(doslogan4()) 
            result_slogans.append(doslogan5())
    
    return result_slogans


start_time = time()
generate_slogan('Sky')
passed_time = time() - start_time
print(f"Tagline Generation Running Time: {passed_time}")