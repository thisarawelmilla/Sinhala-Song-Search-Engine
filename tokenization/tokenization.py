def tokenization(search_term):
    # tokenized the words by sysmbols
    chars = re.escape(string.punctuation)
    remove = re.sub(r'['+chars+']',' ', search_term)
    tokens = remove.split()

    return tokens
       
