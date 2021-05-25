from ITAP_Parser import parse_csv
from test import send_dictionary
from pyattck import Attck
attack = Attck()
import numpy as np
from Combine import get_dictionary
stories_dictionary = parse_csv()
final_dictionary = get_dictionary()

while(1):
    story_number = str(input("Enter Story Number "))
    story = "Story"+story_number
    print(story)
    #print(stories_dictionary[story])
    print("\tScores:")
    print("\t\t"+str(stories_dictionary[story][0]))
    print("\tIndustry:")
    print("\t\t" + str(stories_dictionary[story][1]))
    print("\tTop Tactics used in Story")
    print("\t\t" + str(final_dictionary[story][0]))
    print("\tTactic Descriptions:")
    for m in final_dictionary[story][1]:
        print("\t\t" + str(m)+":  "+ str(final_dictionary[story][1][m][0]))
        print("\n")
    print("\tMitigations from top Tactic:")
    tac = list(final_dictionary[story][1].keys())[0]
    print("\t\t" + str(tac)+":  "+ str(final_dictionary[story][1][tac][1]))
