from collections import Counter

counter = Counter()

def add_word(word):
    counter[word] += 1

def get_top(n):
    return counter.most_common(n)