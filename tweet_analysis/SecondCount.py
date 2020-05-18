import json
import csv
f = open("SentimentResults.json", encoding='utf-8')
data = json.load(f)
f.close()
results = {}
count = 0

for i in range(len(data)):
    line = data[i]
    line_list = []
    zone = line['zone']
    if zone not in results.keys():
        results[zone] = {'pos': 0, 'neu': 0, 'neg': 0}
    score = line['sentiment']['compound']
    if score > 0.2:
        results[zone]['pos'] += 1
    elif score < 0:
        results[zone]['neg'] += 1
    else:
        results[zone]['neu'] += 1
    count += 1
    print(count)

c = open('Sentiments.csv', "w", newline='')
writer = csv.writer(c)
line_list = []
line_list.append("SA3Code")
line_list.append("PosNum")
line_list.append("NeuNum")
line_list.append("NegNum")
writer.writerow(line_list)
for k, v in results.items():
    line_list = []
    line_list.append(k)
    line_list.append(v['pos'])
    line_list.append(v['neu'])
    line_list.append(v['neg'])
    writer.writerow(line_list)
c.close()

with open("SecondCount.json", 'w') as f1:
    json.dump(results, f1)

f = open("AURIN_data.json", encoding='utf-8')
data = json.load(f)
f.close()

c = open('WholeData.csv', "w", newline='')
writer = csv.writer(c)
line_list = []
line_list.append("SA3Code")
line_list.append("SA3Name")
line_list.append("Income")
line_list.append("TotalNum")
line_list.append("TeenNum")
line_list.append("MiddleNum")
line_list.append("OldNum")
line_list.append("TweetNum")
line_list.append("PosNum")
line_list.append("NeuNum")
line_list.append("NegNum")
writer.writerow(line_list)

for k,v in data.items():
    line_list = []
    sa3code = v["sa3code"]
    line_list.append(v["sa3code"])
    line_list.append(v["sa3name"])
    try:
        line_list.append(v["income"])
    except:
        line_list.append(0)
    line_list.append(v["total_num"])
    line_list.append(v["teen_num"])
    line_list.append(v["middle_num"])
    line_list.append(v["old_num"])
    if sa3code in results.keys():
        tweets = results[sa3code]
        line_list.append(tweets['pos'] + tweets['neu'] + tweets['neg'])
        line_list.append(tweets['pos'])
        line_list.append(tweets['neu'])
        line_list.append(tweets['neg'])
    else:
        line_list.append(0)
        line_list.append(0)
        line_list.append(0)
        line_list.append(0)
    writer.writerow(line_list)
c.close()



