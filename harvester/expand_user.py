import utils
from tweepy.error import TweepError
from concurrent.futures import ThreadPoolExecutor
import time


# add all existing user into search tree as level 0
def expand_by_username(api, names):
    parsed_user = utils.bulk_parse_user(
        api.lookup_users(screen_names=names), 0)
    if parsed_user:
        result = db.update(parsed_user)
        print(f'{sum([r[0] for r in result])} user uploaded')


def add_root(api):
    users = [r.key for r in db.view('90024/user', group=True)]
    with ThreadPoolExecutor(max_workers=15 * len(utils.credential)) as executor:
        for names in utils.break_to_chunk(users):
            executor.submit(expand_by_username, api, names)


def batch_update(ids, **args):
    docs = [r.doc for r in db.view(
        'user_tree/by_name', keys=ids, include_docs=True)]
    for doc in docs:
        for k, v in args.items():
            doc[k] = v

    result = db.update(docs)
    for r in result:
        print(r)


def update(name, **args):
    doc = db.view('user_tree/by_name', key=name, include_docs=True).rows[0].doc
    for k, v in args.items():
        doc[k] = v
    db.save(doc)


def expand(api, n, i):
    # get next user to expand, the purpose of while loop is handle race condition
    while True:
        user = db.view('user_tree/expand', limit=1, reduce=False,
                       startkey=[False], endkey=[False, {}], include_docs=True).rows[0].doc
        try:
            user['expanded'] = True
            db.save(user)
            break
        except:
            # Race condition... Skip to next available user.
            pass

    # start the expansion on followers and friends
    try:
        level = user['level'] + 1
        name = user['name']
        print(f'Expanding {name} to level {level} ...')
        follower_ids = api.followers_ids(screen_name=name, count=5000)
        friend_ids = api.friends_ids(screen_name=name, count=5000)
        ids = list(set(follower_ids) | set(friend_ids))
        for uid in utils.break_to_chunk(ids):
            parsed_user = utils.bulk_parse_user(
                api.lookup_users(user_ids=uid), level)
            if parsed_user:
                result = db.update(parsed_user)
                print(
                    f'Key {n}  Loop: {i}  Uploading {sum([r[0] for r in result])} level {level} user.')
    except TweepError:
        print(f'{name} is a protected user, skip...')


def main(rate=15):
    with ThreadPoolExecutor(max_workers=rate * len(utils.credential)) as executor:
        for n, credential in enumerate(utils.credential, start=1):
            for i in range(rate):
                executor.submit(expand, credential.api(wait_on_rate_limit=False, wait_on_rate_limit_notify=False), n, i + 1)
                time.sleep(0.05)


if __name__ == "__main__":
    db = utils.db()
    # main()
    add_root()