# TODO: convert to a class
DATASET = "conll"


def get_required_format(entity, method="binary match"):

    if DATASET == "conll": return get_required_format_conll(entity, method)
    if DATASET == "mujadia": return get_required_format_mujadia(entity, method)

def intersection(key_entity, resp_entity, method="binary match", metric="muc"):

    key_entity = get_required_format(key_entity, method)
    resp_entity = get_required_format(resp_entity, method)
    
    return list(set(key_entity) & set(resp_entity))

# entities -> list of entities where each entity is a list of mentions
def b_cubed(key_entities, resp_entities, score = "recall", method="binary match"):

    entities1 = key_entities
    entities2 = resp_entities

    if score == "precision":
        entities1 = resp_entities
        entities2 = key_entities

    numerator = 0
    denominator = 0

    for entity1 in entities1:

        # differs based on method used
        entity1_size = 0

        if method == "binary match": 
            entity1_size = len(entity1)
        if method == "word": 
            for mention in entity1: entity1_size += len(mention.words)

        denominator += entity1_size

        for entity2 in entities2:
            numerator += ( pow(len(intersection(entity1,entity2,method=method)),2) / entity1_size )

    try:
        recall = numerator / denominator
    except:
        # print("denominator=0")
        return -1

    # print(recall)

    if recall > 1: print("GREATER THAN 1")
    # else: print(recall)
    
    return recall

def partition(entity1, entities2, method="binary match"):
    # only required to calculate what mentions dont intersect with any in required format 
    entity1_f = get_required_format(entity1,method=method)

    # list of mentions found in response entites ("opposite sets")
    # used to find the mentions that are not present in even one "opposite set"
    intersect = []
    
    # number of resp sets that have at least one mention in common
    num_common = 0
    for entity2 in entities2:

        # intersection done on required format in function
        common = intersection(entity1, entity2, metric="muc", method=method)
        # print("common: ",common)

        # flag to check if mention has been included in a partition from a previous chain
        flag = 0
        for c in common:
            if c in intersect: flag = 1

        if flag == 0:
            # add to partition size only if partition created is made up of mentions not seen before
            if len(common) != 0: 
                num_common += 1
                # print("num_common: ",num_common)

        for c in common: 
            intersect.append(c)
        # print("intersect: ",intersect)

    num_not_common = [x for x in entity1_f if x not in intersect]
        # print("num_not_commmon: ",num_not_common)

    # returning partition size
    return (num_common + len(num_not_common))

    # condition: a mention belongs only to one entity (or else using variable common to count common mentions across sets won't be useful)

'''
algorithm - 

given an entity set (eg key) for which partition is created wrt to opposite set (eg response) -> # of partitions - 
= number of opposite sets it has at least one element in common with + number of mentions which are not in common with any opp sets                  

'''

# TODO: add case where # of key entities = 0
def muc(key_entities, resp_entities, score = "recall", method="binary match"):

    numerator = 0
    denominator = 0

    entities1 = key_entities
    entities2 = resp_entities

    if score == "precision":
        entities1 = resp_entities
        entities2 = key_entities

    for entity1 in entities1:

        # differs based on method used
        entity1_size = 0

        if method == "binary match": 
            entity1_size = len(entity1)
        if method == "word": 
            for mention in entity1: entity1_size += len(mention.words)
        
        numerator += (entity1_size - partition(entity1, entities2, method=method))
        
        denominator += (entity1_size - 1)
    
    # print (numerator / denominator)
    if denominator == 0: return 0
    return numerator / denominator

def phi(entity1, entity2, method="binary match"):

    entity1_f = get_required_format(entity1, method=method)
    entity2_f = get_required_format(entity2, method=method)

    return (2 * len(intersection(entity1,entity2, method=method)) ) / ( len(entity1_f) + len(entity2_f) )

def ceafe(key_entities, resp_entities, score = "recall", method="binary match"):

    numerator = 0
    denominator = 0

    # num of elts common across two entity sets
    alignment_score = 0
    phi_val = 0

    entities1 = key_entities
    entities2 = resp_entities

    if score == "precision":
        entities1 = resp_entities
        entities2 = key_entities
    
    for entity1 in entities1:

        for entity2 in entities2:

            if alignment_score < len(intersection(entity1, entity2, method=method)):
                alignment_score = len(intersection(entity1, entity2, method=method))
                phi_val = phi(entity1,entity2,method=method)
        
        numerator += phi_val
        denominator += 1

    # print(numerator/denominator)
    return numerator/denominator


def link(n):
    return n*(n-1)/2

# assuming key_entities is list of mentions
# recall -> entities1 : key_entities, entities1 : resp_entities
# precision -> entities1 : resp_entities, entities1 : key_entities
def lea(entities1, entities2, method="binary match"):

    numerator = 0 
    denominator = 0
    
    for entity1 in entities1:
        # importance -> size of entity (number of mentions)
        importance = len(entity1)
        resolution_score = 0
        for entity2 in entities2:
            # link based, therefore they intersect only if there are at least two mentions in common (a link is present)
            common_mentions = intersection(entity1, entity2, method=method)

            # for singleton mentions, link(ki intersection ri) = 1 only when ki = ri = 1
            if len(common_mentions) == 1:
                if ((len(entity1) == 1) and (len(entity2) == 1)): resolution_score += 1
            
            # at least 2 common mentions means there is at least one link
            if len(common_mentions) >= 2:
                # denominator will never be 0 since len(entity1) >= 2 if len(common_mentions) >= 2
                val = (link(len(common_mentions)))/link(len(entity1))
                if(val > 1): print("oh no")
                resolution_score += (link(len(common_mentions)))/link(len(entity1))
        
        numerator += (importance * resolution_score)
        denominator += len(entity1)

        if numerator/denominator > 1: 
            pprint(vars(entity1))
            print("oh no")
    
    if denominator == 0: return 0
    return (numerator/denominator)