import ujson
from pprint import pprint


def dump(f):
    raw = ujson.load(open(f))
    sa = {zone['properties']['feature_code']: zone['properties']
          ['feature_name'] for zone in raw['features']}
    return sa


sa = {}
for f in ['SA4', 'SA3', 'SA2']:
    sa.update(dump(f'../aurin/{f}.json'))

with open('SA.json', 'w') as fp:
    ujson.dump(sorted(sa.items()), fp)
