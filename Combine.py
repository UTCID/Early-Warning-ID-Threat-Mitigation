from ITAP_Parser import parse_csv
from test import send_dictionary
from pyattck import Attck
import operator
attack = Attck()
import numpy as np
final_dictionary = {}
tactic_to_technique_dictionary, mitigation_to_technique_dictionary = {}, {}
stories_dictionary = {}
def find_top_tactic(current_score):
    final_list = []
    if(len(current_score) == 0):
        return None
    if(len(current_score) == 1 or len(current_score)  == 2):
        for k in current_score:
            final_list.append(k)
        return final_list
    max_value_1 = max(current_score, key = lambda x: current_score[x])
    if(current_score[max_value_1] == 1):
        #too vague
        index = 1
        for key in current_score:
            final_list.append(key)
            index += 1
            if(index == 2):
                break
        return final_list
    while(current_score[max_value_1] > 1 or len(final_list)<= 2):
        final_list.append(max_value_1)
        current_score.pop(max_value_1, None)
        if(len(current_score) == 0):
            break
        max_value_1 = max(current_score, key = lambda x: current_score[x])
    return final_list


def find_mitigations(max_tactic,  tactic_to_technique_dictionary, mitigation_to_technique_dictionary):
    result_dict = {}
    for tac in max_tactic:
        result_dict[tac] = []
        for iter_tactic in attack.tactics:
            if(tac == iter_tactic.name):
                result_dict[tac].append(iter_tactic.description)
        mitigation = []
        list_technique = tactic_to_technique_dictionary[tac]
        #print(list_technique)
        for key in mitigation_to_technique_dictionary:
            if(np.in1d(list_technique,mitigation_to_technique_dictionary[key]).any()): #any technique is in the mitigation to technique list
                if(key not in mitigation):
                    mitigation.append(key)
        result_dict[tac].append(mitigation)
    return result_dict

def combine_dictionary():

    stories_dictionary = parse_csv()
    #print(tactic_to_technique_dictionary)
    tactic_to_technique_dictionary, mitigation_to_technique_dictionary = send_dictionary()

    for key in stories_dictionary:
        current_story = stories_dictionary[key]
        try:
            current_score = current_story[0]
        except:
            current_score = []
        current_org = current_story[1]

        sorted_tuples = sorted(current_score.items(), key=lambda item: item[1])
        current_score = {k: v for k, v in sorted_tuples}
        #print(current_score)
        #print("for KEY: " + str(key))
        final_dictionary[key] = []
        #print(current_score)
        max_tactic = find_top_tactic(current_score)
        final_dictionary[key].append(max_tactic)
        #print(max_tactic)
        if(max_tactic == None):
            #print("UNKNOWN")
            continue
        #print(max_tactic)
        mitigations = find_mitigations(max_tactic,tactic_to_technique_dictionary, mitigation_to_technique_dictionary)
        final_dictionary[key].append(mitigations)
        final_dictionary[key].append(current_org)

def get_dictionary():
    print("Processing...")
    combine_dictionary()
    top_mitigation_story = {}
    for k in final_dictionary:
        top_mit = {}
        #print("FINAL DICTION\n\n")
        #print(final_dictionary[k])
        try:
            for tac in final_dictionary[k][1]:
                #dictionary of tactic and description and mitigation
                for mits in final_dictionary[k][1][tac][1]:
                    #list of mitigations per tactic
                    if(mits in top_mit):
                        top_mit[mits] += 1
                    else:
                        top_mit[mits] = 1
            top_mitigation_story[k] = max(top_mit.items(), key=operator.itemgetter(1))[0]
            #print("\n\n")
        except:
            continue
    print("Done")
    #print(top_mitigation_story)
    return final_dictionary, top_mitigation_story
