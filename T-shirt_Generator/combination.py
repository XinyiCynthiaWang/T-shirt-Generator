import pandas as pd
import generator
import property
import numpy as np
import random


features_df = pd.DataFrame(index = np.arange(25), columns = ['sentiment', 'Word_count', 'Black', 'Colorful', 'White', 'Animal', 'AnimalnPerson', 'Nonrealistic', 'Person', 'text'])

def combination(tshirt):
    generateContent(tshirt)
    generateSlogan(tshirt)
    generateColour(tshirt)
    return features_df

def generateContent(tshirt):
    if tshirt.isRealistic:
        features_df['Animal'] = np.random.choice([0, 1], features_df.shape[0])
        for index in range (features_df.shape[0]):
            if features_df['Animal'][index] == 1:
                features_df.set_value(index, 'Person', 0)
                features_df.set_value(index, 'AnimalnPerson', 0)
            elif features_df['Animal'][index] == 0:
                features_df.set_value(index, 'Person', random.choice([0, 1]))
                features_df.set_value(index, 'AnimalnPerson', 1 - features_df['Person'][index])
        features_df['Nonrealistic'] = 0
    else:
        features_df['Animal'] = 0
        features_df['Person'] = 0  
        features_df['AnimalnPerson'] = 0
        features_df['Nonrealistic'] = 1 

def generateSlogan(tshirt):
    if tshirt.hasSlogan:
        if tshirt.sloganTopic:
            slogan_list = generator.generate_slogan(tshirt.sloganTopic)
            word_count = []
            sentiment = []
            for slogan in slogan_list:
                word_count.append(len(slogan.split()))
                sentiment.append(property.sentiment_analysis(slogan))
            features_df['Word_count'] = word_count
            features_df['sentiment'] = sentiment
            features_df['text'] = slogan_list
        else:
            for index in range (features_df.shape[0]):
                if features_df['Animal'][index] == 1:
                    slogan = random.choice(generator.generate_slogan('Animal'))
                    word_count = len(slogan.split())
                    sentiment = property.sentiment_analysis(slogan)
                    features_df.set_value(index, 'Word_count', word_count)
                    features_df.set_value(index, 'sentiment', sentiment)
                    features_df.set_value(index, 'text', slogan)

                elif features_df['Person'][index] == 1:
                    slogan = random.choice(generator.generate_slogan('Friend'))
                    word_count = len(slogan.split())
                    sentiment = property.sentiment_analysis(slogan)
                    features_df.set_value(index, 'Word_count', word_count)
                    features_df.set_value(index, 'sentiment', sentiment)
                    features_df.set_value(index, 'text', slogan)

                else:
                    slogan = random.choice(generator.generate_slogan(None))
                    word_count = len(slogan.split())
                    sentiment = property.sentiment_analysis(slogan)
                    features_df.set_value(index, 'Word_count', word_count)
                    features_df.set_value(index, 'sentiment', sentiment)
                    features_df.set_value(index, 'text', slogan)
    else:
        features_df['Word_count'] = 0
        features_df['sentiment'] = 0
        features_df['text'] = ['' for i in range (25)]
    
def generateColour(tshirt): 
    if tshirt.isColourful:
        features_df['Colorful'] = 1
        features_df['Black'] = 0
        features_df['White'] = 0
    else:
        features_df['Black'] = np.random.choice([0, 1], features_df.shape[0])
        features_df['White'] = 1 - features_df['Black']
        features_df['Colorful'] = 0