
def evaluate_metric(metric, entities1, entities2, method="binary match"):
    if metric == "muc":
        return muc(entities1, entities2, method=method)
    if metric == "bcub":
        return b_cubed(entities1, entities2, method=method)
    if metric == "ceafe":
        return ceafe(entities1, entities2, method=method)
    if metric == "lea":
        return lea(entities1, entities2, method=method)

def get_scores(entities1, entities2, metric,method):
    print("**********",metric,"**********")
    try: 
        recall = round(evaluate_metric(metric, entities1, entities2, method=method),2)
        print("recall: ",recall)
    except: print("ERROR IN RECALL")
    try: 
        precision = round(evaluate_metric(metric, entities2, entities1, method=method),2)
        print("precision: ",precision)
    except: print("ERROR IN PRECISION")
    try: 
        f1 = round((2 * recall * precision) / (recall + precision),2)
        print("f1: ",f1)
    except: f1 = 0

    return {'recall':recall, 'precision':precision, 'f1':f1}


def calculate_metrics(key_chains, response_chains, score="recall", metric='all', method="binary match",verbose=False):

    key_entities = [key_chains[key] for key in key_chains.keys()]
    response_entities = [response_chains[key] for key in response_chains.keys()]

    scores = {}

    if verbose:
        print("KEYS:")
        for entity in key_entities:
            print(vars(entity[0]),"\n")

        print("\n\nRESPONSE:")
        for entity in response_entities:
            print(vars(entity[0]),"\n")

    if metric == "all":

        scores['muc'] = get_scores(key_entities, response_entities, "muc",method=method)
        scores['bcubed'] = get_scores(key_entities, response_entities, "bcub",method=method)
        scores['ceafe'] = get_scores(key_entities, response_entities, "ceafe",method=method)
        scores['lea'] = get_scores(key_entities, response_entities, "lea",method=method)

    else: 
        if metric == 'b_cubed': scores["bcubed"] = get_scores(key_entities, response_entities, "bcub",method=method)
        if metric == 'muc': scores["muc"] = get_scores(key_entities, response_entities, "muc",method=method)
        if metric == 'ceafe': scores["ceafe"] = get_scores(key_entities, response_entities, "ceafe",method=method)
        if metric == 'lea': scores["lea"] = get_scores(key_entities, response_entities, "lea",method=method)

    return scores