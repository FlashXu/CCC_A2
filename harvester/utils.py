import requests
import json


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    def __getattr__(*args):
        val = dict.__getitem__(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def parse(line):
    try:
        line = str(line, encoding='utf-8').strip()
        if line.endswith(','):
            line = line[:-1]
        return DotDict(json.loads(line))
    except json.decoder.JSONDecodeError:
        pass


def stream(url, func=requests.get, stream=True):
    with func(url, stream=stream) as r:
        yield from filter(None, map(parse, r.iter_lines()))
