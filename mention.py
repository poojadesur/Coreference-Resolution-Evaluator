# is storing this much a waste of space?
# an object can be edited - all multi word mentions, appended to list self.mention
# while reading input file maintain dict {chain idx:{mentionid:Mention}}
class Mention:
    def __init__(self, chain_idx, mention_idx, sentence_idx, word_idx, word, linguistic_head, linguistic_head_idx, multi_word_mention=False):
        
        # comes from annotated data
        self.chain_idx = chain_idx
        self.mention_idx = mention_idx 

        # calculated when reading data input - required to indentify words uniquely
        # word_idx for multi word mentions is the idx of the first word
        self.sentence_idx = sentence_idx
        self.word_idx = word_idx
        
        #list of multiword mentions as separate words,
        self.words = word
        # toggle when object is edited 
        self.multi_word_mention = multi_word_mention

        # should this be calculated during input or during creation of required format list?
        # what i did -> saved linguistic head, calculate nouns when requied
        # self.nouns = nouns # [(word,idx)]
        self.linguistic_head = linguistic_head
        self.linguistic_head_idx = linguistic_head_idx
        