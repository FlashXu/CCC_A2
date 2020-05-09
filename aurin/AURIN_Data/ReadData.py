import json
import csv

f1 = open("./AURIN_Data/SA3_2016_Melb_Income.json", 'r', encoding='UTF-8')
f2 = open("./AURIN_Data/SA3_2016_Sydn_Income.json", 'r', encoding='UTF-8')
f3 = open("./AURIN_Data/SA3_2017_Melb_Population.json", 'r', encoding='UTF-8')
f4 = open("./AURIN_Data/SA3_2017_Sydn_Population.json", 'r', encoding='UTF-8')

features1 = json.load(f1)['features']
features2 = json.load(f2)['features']
features3 = json.load(f3)['features']
features4 = json.load(f4)['features']

data = {}

for i in range(len(features1)):
    instance = features1[i]['properties']
    sa3code = instance['sa3_code16']
    sa3name = instance['sa3_name16']
    income = instance['est_p_inc_avg_tot_inc_excl_gov_pnsn_aud']
    if sa3code not in data.keys():
        data[sa3code] = {}
        data[sa3code]['sa3name'] = sa3name
        data[sa3code]['sa3code'] = sa3code

    data[sa3code]['income'] = income


for i in range(len(features2)):
    instance = features2[i]['properties']
    sa3code = instance['sa3_code16']
    sa3name = instance['sa3_name16']
    income = instance['est_p_inc_avg_tot_inc_excl_gov_pnsn_aud']
    if sa3code not in data.keys():
        data[sa3code] = {}
        data[sa3code]['sa3name'] = sa3name
        data[sa3code]['sa3code'] = sa3code

    data[sa3code]['income'] = income

for i in range(len(features3)):
    instance = features3[i]['properties']
    sa3code = instance['sa3_code16']
    sa3name = instance['sa3_name16']
    total_num = instance['persons_total']
    teen_num = instance['persons_age_0_4']+instance['persons_age_5_9']+instance['persons_age_10_14']\
               +instance['persons_age_15_19']+instance['persons_age_20_24']+instance['persons_age_25_29']
    middle_num = instance['persons_age_30_34']+instance['persons_age_35_39']\
               +instance['persons_age_40_44']+instance['persons_age_45_49']\
                 +instance['persons_age_50_54']+instance['persons_age_55_59']
    old_num = instance['persons_age_60_64']+instance['persons_age_65_69']\
               +instance['persons_age_70_74']+instance['persons_age_75_79']\
                 +instance['persons_age_80_84']+instance['persons_age_85_plus']

    if sa3code not in data.keys():
        data[sa3code] = {}
        data[sa3code]['sa3name'] = sa3name
        data[sa3code]['sa3code'] = sa3code

    data[sa3code]['total_num'] = total_num
    data[sa3code]['teen_num'] = teen_num
    data[sa3code]['middle_num'] = middle_num
    data[sa3code]['old_num'] = old_num

for i in range(len(features4)):
    instance = features4[i]['properties']
    sa3code = instance['sa3_code16']
    sa3name = instance['sa3_name16']
    total_num = instance['persons_total']
    teen_num = instance['persons_age_0_4']+instance['persons_age_5_9']+instance['persons_age_10_14']\
               +instance['persons_age_15_19']+instance['persons_age_20_24']+instance['persons_age_25_29']
    middle_num = instance['persons_age_30_34']+instance['persons_age_35_39']\
               +instance['persons_age_40_44']+instance['persons_age_45_49']\
                 +instance['persons_age_50_54']+instance['persons_age_55_59']
    old_num = instance['persons_age_60_64']+instance['persons_age_65_69']\
               +instance['persons_age_70_74']+instance['persons_age_75_79']\
                 +instance['persons_age_80_84']+instance['persons_age_85_plus']

    if sa3code not in data.keys():
        data[sa3code] = {}
        data[sa3code]['sa3name'] = sa3name
        data[sa3code]['sa3code'] = sa3code

    data[sa3code]['total_num'] = total_num
    data[sa3code]['teen_num'] = teen_num
    data[sa3code]['middle_num'] = middle_num
    data[sa3code]['old_num'] = old_num


print(data)
with open('AURIN_data.json','w',encoding='utf-8') as f:
  f.write(json.dumps(data))

c = open('AURIN_data.csv', "w", newline='')
writer = csv.writer(c)
line_list = []
line_list.append("SA3Code")
line_list.append("SA3Name")
line_list.append("Income")
line_list.append("TotalNum")
line_list.append("TeenNum")
line_list.append("MiddleNum")
line_list.append("OldNum")
writer.writerow(line_list)

for k,v in data.items():
    print(v)
    line_list = []
    line_list.append(v["sa3code"])
    line_list.append(v["sa3name"])
    try:
        line_list.append(v["income"])
    except:
        line_list.append(" ")
    line_list.append(v["total_num"])
    line_list.append(v["teen_num"])
    line_list.append(v["middle_num"])
    line_list.append(v["old_num"])
    writer.writerow(line_list)
c.close()