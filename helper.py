# returns an entity which is represented as a list of "sentidx%wordidx" each of which represents a mention
# multiword mentions: "sentidx%word1idx-word2idx-word3-idx" -> update: wrong
# treat multiword mentions all as normal single word mentions by splitting them apart - eg  "sentidx%word1idx-word2idx-word3-idx" ->  ["sentidx%word1idx" "sentidx%-word2idx" "sentidx%-word3idx"]

def get_words(entity):
    entity_f = []
    for mention in entity:
        for i,word in enumerate(mention.words): 
            entity_f.append(str(mention.sentence_idx) + "%" + str(i+mention.word_idx))
    return entity_f

# have to calculate nouns outside bc length of text can affect how it is calculated
def get_nouns(entity):
    entity_f = []

    for mention in entity:
        if mention.multi_word_mention:
            for (word,idx) in mention.nouns: entity_f.append(mention.sentence_idx + "%" + str(idx + self.word_idx))
        else: entity_f.append(mention.sentence_idx + "%" + str(self.word_idx))

    return entity_f

def get_linguistic_head(entity):
    entity_f = []
    for mention in entity:
        entity_f.append(mention.sentence_idx + "%" + mention.linguistic_head_idx)
    return entity_f

# TODO CLARIFY BIG ASSUMPTION - multi word mentions are all one after the other
def get_binary_match(entity):
    entity_f = []
    for mention in entity:
        if mention.multi_word_mention:
            word_idx = str(mention.word_idx)
            for i,word in enumerate(mention.words): word_idx += str("-" + str(mention.word_idx + i + 1))
            entity_f.append(str(mention.sentence_idx) + "%" + word_idx)
        else: entity_f.append(str(mention.sentence_idx) + "%" + str(mention.word_idx))
    return entity_f



def get_required_format_conll(entity, method='binary match'):
    if method == "word": return get_words(entity)

    if method == "nouns": return get_nouns(entity)

    if method == "linguistic head": return get_linguistic_head(entity)

    if method == "binary match": return get_binary_match(entity)