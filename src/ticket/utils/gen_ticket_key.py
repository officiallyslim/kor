import string
import random

def gen_key(length):
    characters = string.ascii_lowercase + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key
