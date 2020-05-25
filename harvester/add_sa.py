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
    raw = ujson.load(open(f'{file}.json'))
    return {zone['properties']['feature_code']: shape(
        zone['geometry']) for zone in raw['features']}


def add_zone(doc, zones):
    geo = doc['geo']
    doc['zone'] = get_zone(doc['geo'], zones)
    return doc


def main(chunk_size=500):

    db = utils.db()

    zones = load_zones()
    while True:
        try:
            rows = db.view('geo/by_zone',
                           include_docs=True, reduce=False, limit=chunk_size)[None]
            print(f'Get {len(rows)} data...')
            docs = [add_zone(row.doc, zones) for row in rows]
            if docs:
                result = db.update(docs)
                print(f'{sum([r[0] for r in result])}/{len(docs)} updated.')
                time.sleep(0.5)
            else:
                time.sleep(20)
        except:
            time.sleep(5)


if __name__ == "__main__":
    main()