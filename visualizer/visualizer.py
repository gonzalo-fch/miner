import redis
import streamlit as st
from collections import Counter
import time

redis_client = redis.Redis(host="localhost", port=6379)

st.title("Most Used Words in Method Names")

top_n = st.slider("Top N words", 5, 50, 10)

placeholder = st.empty()

while True:

    words = redis_client.lrange("words", 0, -1)
    words = [w.decode("utf-8") for w in words]

    counts = Counter(words)
    most_common = counts.most_common(top_n)

    data = dict(most_common)

    placeholder.bar_chart(data)

    time.sleep(2)