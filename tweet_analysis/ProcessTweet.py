import DataAnalysis as da
import json
from nltk.sentiment import SentimentIntensityAnalyzer
vader_analyzer = SentimentIntensityAnalyzer()
Aurin_data = open("AURIN_data.json", encoding='utf-8')
sacode = json.load(Aurin_data).keys()

f = open("twitter.json", encoding='utf-8')
line = f.readline()
count = 0
results = []

for row in f:
    line = f.readline()
    str_data = line
    str_data = str_data[:-2]
    try:
        lang = json.loads(str_data)['doc']['lang']
    except:
        continue
    if lang != "en":
        continue
    id = json.loads(str_data)['id']
    text = json.loads(str_data)['doc']['text']
    sentiment = vader_analyzer.polarity_scores(text)
    # sentiment = da.liu_hu_lexicon(text)
    try:
        zone = json.loads(str_data)['doc']['zone'][:5]
        if zone not in sacode:
            continue
    except:
        continue
    instance ={}
    instance['id'] = id
    instance['text'] = text
    instance['zone'] = zone
    instance['sentiment'] = sentiment
    results.append(instance)
    count += 1
    print(count)

f.close()
with open("SentimentResults.json","w") as output:
    json.dump(results, output)




