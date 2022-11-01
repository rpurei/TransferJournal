import string
import random


def random_string(string_len):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=string_len))
