import hashlib
from typing import Union

from .. settings import settings


def encode(num: int, alphabet: str) -> str:
    _divmod = divmod
    base = len(alphabet)
    answer = []
    if num == 0:
        return alphabet[0]
    while num:
        num, remainder = _divmod(num, base)
        answer.append(alphabet[remainder])
    answer.append(settings.url_prefix)
    answer.reverse()
    return ''.join(answer)


def decode(s: str, alphabet: str) -> Union[int, None]:
    s = s[1:]
    for char in s:
        if char not in set(alphabet):
            return None
    base = len(alphabet)
    base_dict = {char: position for position, char in enumerate(alphabet)}
    num = 0
    for char in s:
        num = num * base + base_dict[char]
    return num


def get_hash(link: str) -> str:
    return hashlib.md5(link.encode(encoding='utf-8')).hexdigest()
