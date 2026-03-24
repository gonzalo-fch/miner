import re


def split_words(name):

    words = []

    snake = name.split("_")

    for part in snake:

        camel = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', part)

        if camel:
            words.extend(camel)
        else:
            words.append(part)

    return [w.lower() for w in words if len(w) > 1]