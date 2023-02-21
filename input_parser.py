import json
import numpy as np
import re
from pprint import pprint

# NOUN POS TAGGING
import nltk 
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
def NounExtractor(text):
    # nouns = [(noun, word_idx)...]
    nouns = []
    words = text.split()
    tagged = nltk.pos_tag(words)
    for i,(word, tag) in enumerate(tagged):
        if tag == 'NN' or tag == 'NNS' or tag == 'NNPS' or tag == 'NNP': nouns.append((word,i))

    return nouns

# active list is list of all mentions in their unique index format entity_idx%mention_idx that are currently open where mention idx is the number of mentions seen for that entity so far
# global_stack is a dictionary of entity_idx: entity_stack that keeps track of the mentions active by their unique index in a stack as the key value.

def get_conll_input(ip_file, word_annotation_idx, label_idx, verbose=False):
    
    chains = {}
    active_list = []
    global_stack = {}
    word_idx = 0

    # keeping track of number of mentions for each entity
    entity_mention_count = {}

    #using a unique index for each mention - chain_idx%entity_mention_count[chain_idx] to keep a global stack of which mentions are open

    with open(ip_file) as f:
        for i,line in enumerate(f):
            
            if line == "\n": continue
            if line.split()[0] == '#begin': continue
            if line.split()[0] == '#end': continue

            word_idx += 1

            line = line.split()

            word = line[word_annotation_idx]
            label = line[label_idx]

            # add words to those in the global stack that are currently active
            if label == "-":                 
                for mention_unq_idx in active_list:
                    # print("mention unique idx: ", mention_unq_idx)
                    # print(mention_unq_idx)
                    chain_idx = mention_unq_idx.split("%")[0]
                    mention_idx = mention_unq_idx.split("%")[1]
                    linguistic_head = ""
                    linguistic_head_idx = ""
                        
                    # multi word mentions - edit already created object
                    # print("chain idx ",chain_idx," mention idx ",mention_idx)
                    # print("chains[chain_idx]: " , vars(chains[chain_idx][0]))

                    # return chains

                    mention = next((mention for mention in chains[str(chain_idx)] if mention.mention_idx == int(mention_idx)), None)
                    # print("mention: ",mention)
                    # pprint(vars(mention))
                    mention.multi_word_mention = True
                    mention.words.append(word)
                    if mention.linguistic_head == "":
                        mention.linguistic_head = linguistic_head
                        mention.linguistic_head_idx = linguistic_head_idx
            
                continue
            
            if verbose:
                print("LINE NUMBER ", i+1)
                print("label: ", label)

            # ---------------- SINGLE WORD MENTIONS -------------------
            # STEP 1: look for (0-9) exact matches for single word mentions and remove that string
            # 1a: getting numbers between parantheses - single word mentions
            single_word_entity_idxs = re.findall(r'\(\d+\)', label)
            single_word_entity_idxs = sorted(single_word_entity_idxs, key=len,reverse=True)
            for r in single_word_entity_idxs:
                label = label.replace(r,"")
            for r_idx in range(len(single_word_entity_idxs)):
                single_word_entity_idxs[r_idx] = single_word_entity_idxs[r_idx].replace("(","")
                single_word_entity_idxs[r_idx] = single_word_entity_idxs[r_idx].replace(")","")
            # print("single word entity idxs: ",single_word_entity_idxs)
            # print("label: ", label)

            # 1b: creating new mentions for single word mentions
            for entity_idx in single_word_entity_idxs:
                # print(mention_unq_idx)
                chain_idx = entity_idx

                if entity_idx in entity_mention_count.keys(): entity_mention_count[entity_idx] += 1
                else: entity_mention_count[entity_idx] = 0
                mention_idx = entity_mention_count[entity_idx]

                linguistic_head = ""
                linguistic_head_idx = ""
                # first time encountering a chain - (chain and entity used replacably)
                if chain_idx not in chains.keys():
                    chains[chain_idx] = []
                # print("CREATED MENTION ",chain_idx + "%" + str(mention_idx))
                mention = Mention(chain_idx, mention_idx,  0, word_idx, [word], linguistic_head, linguistic_head_idx, multi_word_mention=False)
                chains[chain_idx].append(mention)
            
            # ------------------ MENTIONS STARTING AT THIS WORD ------------
            # STEP 2: look for (0-9 exact matches and remove, push number into live stack
            # 2a: multi word mentions starting at this word
            start_entity_idxs = re.findall(r'\(\d+', label)
            start_entity_idxs = sorted(start_entity_idxs, key=len,reverse=True)
            for r in start_entity_idxs:
                label = label.replace(r,"")
            for r_idx in range(len(start_entity_idxs)):
                start_entity_idxs[r_idx] = start_entity_idxs[r_idx].replace("(","")
                start_entity_idxs[r_idx] = start_entity_idxs[r_idx].replace(")","")
            # print("start entity idxs: ",start_entity_idxs)
            # print("label: ", label)

            # 2b: adding to existing mentions in active list for multi word mentions - currently active mentions, all these mentions have already been created
            for mention_unq_idx in active_list:
                # print("mention unique idx: ", mention_unq_idx)
                # print(mention_unq_idx)
                chain_idx = mention_unq_idx.split("%")[0]
                mention_idx = mention_unq_idx.split("%")[1]
                linguistic_head = ""
                linguistic_head_idx = ""
                    
                # multi word mentions - edit already created object
                # print("chain idx ",chain_idx," mention idx ",mention_idx)
                # print("chains[chain_idx]: " , vars(chains[chain_idx][0]))

                # return chains

                mention = next((mention for mention in chains[str(chain_idx)] if mention.mention_idx == int(mention_idx)), None)
                # print("mention: ",mention)
                # pprint(vars(mention))
                mention.multi_word_mention = True
                mention.words.append(word)
                if mention.linguistic_head == "":
                    mention.linguistic_head = linguistic_head
                    mention.linguistic_head_idx = linguistic_head_idx
            
            # 2c: adding starting exist to a list of currently active mentions and creating those mentions
            for entity_idx in start_entity_idxs:
                # print(mention_unq_idx)
                chain_idx = entity_idx

                if entity_idx in entity_mention_count.keys(): entity_mention_count[entity_idx] += 1
                else: entity_mention_count[entity_idx] = 0
                mention_idx = entity_mention_count[entity_idx]

                linguistic_head = ""
                linguistic_head_idx = ""
                # first time encountering a chain - (chain and entity used replacably)
                if chain_idx not in chains.keys():
                    chains[chain_idx] = []
                # print("CREATED MENTION ",chain_idx + "%" + str(mention_idx))
                mention = Mention(chain_idx, mention_idx,  0, word_idx, [word], linguistic_head, linguistic_head_idx, multi_word_mention=False)
                chains[chain_idx].append(mention)

                active_list.append(entity_idx + "%" + str(entity_mention_count[entity_idx]))
                
                if entity_idx not in global_stack.keys(): global_stack[entity_idx] = []
                global_stack[entity_idx].append(entity_idx + "%" + str(entity_mention_count[entity_idx]))


            # ---------------- MENTIONS ENDING AT THIS WORD ----------------------
            # STEP 3: look for 0-9) exact matches and remove, remove from live stack list
            # 3a: get multi word mentions idxs ending at this word
            end_entity_idxs = re.findall(r'\d+\)', label)
            end_entity_idxs = sorted(end_entity_idxs, key=len,reverse=True)
            for r in end_entity_idxs:
                label = label.replace(r,"")
            for r_idx in range(len(end_entity_idxs)):
                end_entity_idxs[r_idx] = end_entity_idxs[r_idx].replace("(","")
                end_entity_idxs[r_idx] = end_entity_idxs[r_idx].replace(")","")
            # print("end entity idxs: ",end_entity_idxs)
            # print("label: ", label)
            

            # 3b: removing idxs from end idx from currently active mentions and updating the global stack
            for entity_idx in end_entity_idxs:
                mention_idx_being_removed = global_stack[entity_idx].pop()
                active_list.remove(mention_idx_being_removed)

            # print("entity_mention_count ", entity_mention_count.items())
            # print("global stack ", global_stack.items())
            # print("active list ", *active_list)    
            # print("\n\n")
    # print(len(chains))
    return chains