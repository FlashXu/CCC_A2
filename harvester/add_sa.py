import time
import ujson
from shapely.geometry import shape, point
from shapely import speedups
import couchdb
import utils


def get_zone(geo, zones):
    for z, s in zones.items():
        if s.contains(point.Point(geo)):
            return z
    return 'und'


def load_zones(file='SA2'):
    raw = ujson.load(open(f'../aurin/{file}.json'))
    return {zone['properties']['feature_code']: shape(
        zone['geometry']) for zone in raw['features']}


def add_zone(doc, zones):
    geo = doc['geo']
    doc['zone'] = get_zone(doc['geo'], zones)
    return doc


def main(chunk_size=500):

    db = utils.db(url='172.26.131.114:5984')
    # db = utils.db(url='45.88.195.224:9001')

    zones = load_zones()
    while True:
        try:
            rows = db.view('process/SA', include_docs=True,
                           reduce=False, limit=200, skip=400)
            print(f'Get {len(rows)} data...')
            docs = [add_zone(row.doc, zones) for row in rows]
            if not docs:
                time.sleep(20)
            result = db.update(docs)
            print(f'{sum([r[0] for r in result])}/{len(docs)} updated.')
        except:
            time.sleep(5)


if __name__ == "__main__":
    main()
