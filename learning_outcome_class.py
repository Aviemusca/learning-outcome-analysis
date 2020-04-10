import os
import sys
import json
import spacy

from verb_category_class import VerbCategory
from functions import get_lines, file_not_found_msg

class LearningOutcome:
    """  A class to manage each learning outcome of a curriculum """


    #######################
    ### Class variables ###
    #######################


    num_of_LOs = 0 # Total number of learning outcomes in the class


    #######################
    ### Special Methods ###
    #######################

    def __init__(self, text=""):
        self.strand = "" # The strand name of a LO instance
        self.category_hits = {} # Keys = verb categories; values = number of verbs in LO from that category
        self.num_of_hits = 0 # Total number of hits in the learning outcome
        self.text = text # The string/text of a learning outcome

        LearningOutcome.num_of_LOs += 1


    def __repr__(self):
        return f"LearningOutcome(text={self.text})"

    def __str__(self):
        return self.text

    def set_text(self, text):
        """ Loads the LO text """
        self.text = text.lower().strip()
        return self.text

    @classmethod
    def write_json_count_dictionary(cls):
        """ Writes the json count dictionary to file """
        pass

    def attach_cat_hits_dict(self, categories):
        """ Creates an attribute dictionary whose keys are the verb category names of the taxonomy"""
        self.category_hits = {category : 0 for category in categories}
        #for category in categories:
        #    self.category_hits[category] = 0

    def get_category_hits(self, verb_dictionary):
        allowed_non_verbs = ["who", "what", "where", "when", "why"]
        non_detected_verbs = []
        self.category_hits = {category : 0 for category in verb_dictionary} # initialise the category hits
        nlp = spacy.load("en_core_web_sm")
        tokenised_LO = nlp(self.text)
        for token in tokenised_LO:
            for category in verb_dictionary:
                if (token.pos_ == "VERB" or token.text in (allowed_non_verbs or non_detected_verbs)) and token.lemma_ in verb_dictionary[category]:
                    self.category_hits[category] += 1
                    self.num_of_hits += 1

    def display_category_hits(self):
        pass


