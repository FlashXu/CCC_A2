import utils
from tweepy.error import TweepError
from concurrent.futures import ThreadPoolExecutor
import asyncio
from asgiref.sync import sync_to_async
import time


# add all existing user into search tree as level 0
def add_root(api):
    users = [r.key for r in db.view('90024/user', group=True)]
    for names in utils.break_to_chunk(users):
        parsed_user = utils.bulk_parse_user(
            api.lookup_users(screen_names=names), 0)
        if parsed_user:
            result = db.update(parsed_user)
            print(f'{sum([r[0] for r in result])} user uploaded')


@sync_to_async
def lookup_by_ids(api, ids, level):
    for sub_ids in utils.break_to_chunk(ids):
        users = api.lookup_users(user_ids=sub_ids)
        parsed_user = utils.bulk_parse_user(users, level)
        if parsed_user:
            result = db.update(parsed_user)
            print(
                f'Uploading {sum([r[0] for r in result]):2} level {level} user.')


# acquire next user to expand, the purpose of while loop is handle race condition
@sync_to_async
def acquire_next_user():
    while True:
        user = db.view('user_tree/expand', limit=1, reduce=False,
                       startkey=[False], endkey=[False, {}], include_docs=True).rows[0].doc
        try:
            user['expanded'] = True
            db.save(user)
            return user
        except:
            # 'Update Conflict' race condition... Skip to next available user.
            pass

# get the union of followers and friends ids for the given user
@sync_to_async
def ff_ids(api, name):
    follower_ids = api.followers_ids(screen_name=name, count=5000)
    friend_ids = api.friends_ids(screen_name=name, count=5000)
    return list(set(follower_ids) | set(friend_ids))


async def expand(api):
    user = await acquire_next_user()

    # start the expansion on followers and friends
    try:
        level = user['level'] + 1
        name = user['name']
        print(f'Expanding {name} to level {level} ...')
        ids = await ff_ids(api, name)
        tasks = [lookup_by_ids(api, ids, level)
                 for ids in utils.break_to_chunk(ids, 500)]
        await asyncio.wait(tasks)
    except TweepError:
        print(f'{name} is a protected user, skip...')


async def main(rate=15):
    start = time.time()

    token_size = len(utils.credential)
    tasks = []
    for n in range(token_size):
        for i in range(rate):
            tasks.append(expand(utils.api(n, False, False)))
    await asyncio.wait(tasks)

    print(time.time() - start)


if __name__ == "__main__":
    db = utils.db(url='115.146.95.16:9001')
    asyncio.run(main(5))
