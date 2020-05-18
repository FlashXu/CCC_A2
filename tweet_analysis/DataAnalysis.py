
def lemmatize_sentence(tokens):
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk.tag import pos_tag
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def remove_noise(tweet_tokens, stop_words = ()):
    import re, string
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk.tag import pos_tag
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def liu_hu_lexicon(sentence):

    from nltk.corpus import opinion_lexicon
    from nltk.tokenize import TweetTokenizer
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')

    tokenizer = TweetTokenizer(preserve_case=False)
    pos_words = 0
    neg_words = 0
    # Tokenize the sentence
    tokens = tokenizer.tokenize(sentence)
    # Remove noise and change words' form
    tokens = lemmatize_sentence(remove_noise(tokens, stop_words))
    tokenized_sent = [word.lower() for word in tokens]

    for word in tokenized_sent:
        if word in opinion_lexicon.positive():
            pos_words += 1
        elif word in opinion_lexicon.negative():
            neg_words += 1

    if pos_words > neg_words:
        return "Positive"
    elif pos_words < neg_words:
        return "Negative"
    elif pos_words == neg_words:
        return "Neutral"
