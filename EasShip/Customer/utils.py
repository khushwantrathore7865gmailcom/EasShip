import random
import string


def generate_id(length=50):
    key = ''
    for l in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)

    return key
