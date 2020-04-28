import requests
import json
import tweepy
from datetime import datetime
import couchdb


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    def __getattr__(*args):
        val = dict.__getitem__(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def parse_line(line):
    try:
        line = str(line, encoding='utf-8').strip()
        if line.endswith(','):
            line = line[:-1]
        return DotDict(json.loads(line))
    except json.decoder.JSONDecodeError:
        pass


def stream(url, func=requests.get, stream=True):
    with func(url, stream=stream) as r:
        yield from filter(None, map(parse_line, r.iter_lines()))


def break_to_chunk(l, size=100):
    return [l[i:i + size] for i in range(0, len(l), size)]


# Variables that contains the user credentials to access Twitter API
class Credential:
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

    def api(self, wait_on_rate_limit=True, wait_on_rate_limit_notify=True):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        return tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit, wait_on_rate_limit_notify=wait_on_rate_limit_notify)


credential = [
    Credential('nyR8ejR7Z7LftoDYRoyusn2jg',
               'lLlxxKAOd3DyIGTLVgq1Mwy8hOnsGPCTroBhAIbgqB31Dbp0WT',
               '851934201506971648-TTEeRvC5pcTBu5GGl9LV1yqANvRMVu1',
               'tyZVYaNiPm2bMjjo4bkEuGwABUHoBITlrnWnDEENqKZSl'),

    Credential('n5FxlcSsxWpaVrLtdSiHTcWiG',
               'Tf2Xv6h5Z7bWcTUkhzaxmZfzVF8OeIkzbFi3tjO1wz6KkqRbls',
               '1250699207272304640-TAWwK8eToTmHNcAT79RZVIapIFYNla',
               '2PBtpTyUQvr1T3NtgbLHNI6QDdYPloaFvQhP8J49cIkG1'
               ),

    Credential('CZffhPdM8SIh8lBgOBgczz5uD',
               '6APpt2NW5Z9ieGJnEb5ySmZn4Zf6QF43Ygsgm02Pa3Mig3tbgd',
               '1252457706041913344-TEX4W3EnZAUQAAHyLsFijebDX0p5pB',
               'vK5CNioh1yNBR5kH5hFjGNvC27O8XI2aJFrMYEznW7OHD'
               ),

    Credential('U1lUxhPRqkgJnjcYxzR9l882D',
               'eWyY3NaI02ZmNXT3V4ITbPGGWvrGzUyb6Lr71ecfraw8VaYQ3i',
               '1118399076653944833-cpAmEuFX694kK4i7JSQy9DnRzsfZG9',
               'Wh3MzRqIwqXcymvRcticPRkewb06s8DuuRiHvEXEQDdjm'
               ),

    Credential('L0BR4kmzsxaM7IdPUHdQ37Hns',
               'MsugIw8Ltx114Kkqgfm66RRpj7Z8KWqV1NR4Eq4xFFhkRGEJ67',
               '1118399076653944833-DUN8hDJDHqGka3lw6a29JNUi21qyaP',
               'oXvl3HzDIvPJvLpr949pkD7nDxbxPsO9xoy1Lutl2P1Y7'
               ),

    Credential('esfbRz6gUhGyckd2t7K7BLQeW',
               'A7GyPaNmpJsKgXXgR2qIgNCRhPN1KCvb0qJ3YfImPqHNevhTwx',
               '2362162429-GYwJY4gknR5Gj6JHs9aSlP7hax8k3Z0fXK8PVwE',
               '4kWkv1Yqpst0o7V7QaYMiusFZppAyCtOXg06AJ693o1WZ'
               ),

    Credential('ALNwJ7Unkb2WURTSDqA9o7Aan',
               '1vibUNGiegOhQa9WV1FzNGJdFFCyAclnOCna13sFGO9DMPhEWa',
               '622442315-Mw1YibQ8XrkB0HvwNblH301Q5uSqV235yzR2P4An',
               'HNsNN5FYjjvWhK2VVVbnnKmttKePC0qp9JSbtgKYJxeGV'),

    Credential('9uWwELoYRA4loNboCqe4P7XZD',
               'ZhIOn2XPAnVtDjbh4iVrANG4gq7zTCJdJZAAlDpPmKAFpNz4gF',
               '2344719422-4a94VSU2kjHzgFp1Kap9uoAAvE5R2n9vb4H5Atz',
               'O5H5r7QyOTct7yFFlePITJGcuIJPBmgyDBunIYRVjYELq'
               ),
]


def db(name='tweet-stream', url='localhost:5984', username='admin', password='admin'):
    return couchdb.Server(f'http://{username}:{password}@{url}').__getitem__(name)


def bulk_parse_tweet(raw_tweets, blacklist=['googuns_lulz', 'object82']):
    return list(filter(None, map(lambda s: parse_tweet(s._json, blacklist), raw_tweets)))


def parse_tweet(raw_tweet, blacklist=['googuns_lulz', 'object82']):
    if not (raw_tweet['place'] and raw_tweet['place']['country_code'] == 'AU'):
        return

    data = {}
    data['_id'] = raw_tweet['id_str']
    data['date'] = datetime.strptime(
        raw_tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
    data['user'] = raw_tweet['user']['screen_name']
    data['lang'] = raw_tweet['lang']

    if data['user'] in blacklist:
        return

    def extract_hashtag(entity):
        return [h['text'] for h in entity['hashtags']]

    # extended tweet is un-truncated version of the tweet
    if 'extended_tweet' in raw_tweet:
        ext = raw_tweet['extended_tweet']
        data['text'] = ext['full_text']
        data['hashtags'] = extract_hashtag(ext['entities'])
    else:
        data['text'] = raw_tweet['text']
        data['hashtags'] = extract_hashtag(raw_tweet['entities'])

    # geo-location
    if raw_tweet['coordinates'] and 'coordinates' in raw_tweet['coordinates']:
        data['geo'] = raw_tweet['coordinates']['coordinates']
    elif raw_tweet['geo'] and 'coordinates' in raw_tweet['geo']:
        coordinate = raw_tweet['geo']['coordinates']
        if len(coordinate) == 2:
            data['geo'] = [coordinate[1], coordinate[0]]

    place = raw_tweet['place']
    place_key = ['place_type', 'full_name', 'bounding_box']
    data['place'] = {k: place[k] for k in place if k in place_key}

    return data


def bulk_parse_user(raw_users, level):
    return list(filter(None, map(lambda u: parse_user(u._json, level), raw_users)))


def parse_user(raw_user, level):
    user = {}
    user['_id'] = 'u_' + raw_user['id_str']
    user['type'] = 'user'
    user['name'] = raw_user['screen_name']
    user['level'] = level
    user['expanded'] = False
    user['searched'] = False
    for key in ['followers_count', 'friends_count', 'statuses_count']:
        user[key] = raw_user[key]

    activity = user['followers_count'] + user['friends_count']

    return None if activity < 400 or activity > 5000 else user


def batch_update_by_username(db, ids, **args):
    docs = [r.doc for r in db.view(
        'user_tree/by_name', keys=ids, include_docs=True)]
    for doc in docs:
        for k, v in args.items():
            doc[k] = v

    result = db.update(docs)
    for r in result:
        print(r)


def update_by_username(db, name, **args):
    doc = db.view('user_tree/by_name', key=name, include_docs=True).rows[0].doc
    for k, v in args.items():
        doc[k] = v
    db.save(doc)
