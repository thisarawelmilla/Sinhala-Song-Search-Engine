def remove_stopword(tokens, stopwords):
    stopwords_removed = []
    for i in tokens:
       if i not in stopwords:
           stopwords_removed.append(i)
    return stopwords_removed
