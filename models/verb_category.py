import os
import sys
import json
import math
from utils.files import file_not_found_msg

class VerbCategory:
    """ A class to manage each verb category of a given taxonomy """

    #######################
    ### Class Variables ###
    #######################

    filename_verbs_txt = "" # Input verb list text filename
    filename_verbs_json = "" # Output verb dictionary json filename
    num_of_categories = 0 # Total number of verb categories
    category_names = [] # Verb category names

    #########################
    ###   Magic Methods   ###
    #########################

    def __init__(self, name="", verbs=[]):
        self.name = name.upper() # Verb category name
        self.verbs = list(set([verb.lower() for verb in verbs])) # Verbs associated with the category / duplicates removed
        self.num_of_verbs = len(self.verbs) # Total number of verbs in the category

        VerbCategory.num_of_categories += 1


    def __str__(self):
        return self.name + ": " + ', '.join([verb for verb in self.verbs])


    def __len__(self):
        """ Make the length of a category equal to the number of verbs """
        return self.num_of_verbs

    def __eq__(self, other):
        """2 categories are equal if their verbs are the same"""
        return set(self.verbs) == set(other.verbs)


    def __add__(self, other):
        """Adding 2 categories a and b returns a new category c, whose verbs are the union of a and b"""
        return VerbCategory(verbs=list(set(self.verbs + other.verbs)))

    def __sub__(self, other):
        """ Subtracting 2 categories a and b removes all verbs from a which appear in b, returns new category """
        return VerbCategory(verbs=[verb for verb in self.verbs if verb not in other.verbs])


    def __mul__(self, other):
        """ Multiplying 2 categories a and b returns a new category c, whose verbs are the intersection/overlap of a and b"""
        return VerbCategory(verbs=list(set(self.verbs) & set(other.verbs)))


    ########################
    ### Instance Methods ###
    ########################

    def add_verb(self, verb):
        """ Adds a verb to the verb category if not already in the category"""
        if verb.lower() not in self.verbs:
            self.verbs.append(verb.lower())
            self.num_of_verbs += 1

    def add_verbs(self, verbs):
        """ Adds a list of verbs to the verb category """
        for verb in verbs:
            self.add_verb(verb)

    def add_verbs_from_file(self, filename, line_number):
        """ Adds a list of verbs to the verb category, given a line index number (file lines numbered from 0) of a file """
        try:
            with open(filename, 'r') as f:
                for index, line in enumerate(f):
                    if index == line_number:
                        self.add_verbs(line.lower().replace(' ', '').strip().split(','))
        except FileNotFoundError:
            print (f"File '{filename}' not found! Please check the filename and file directory.")

    def set_verb_number(self):
        """ Re-evaluates the number of verbs of the verb category """
        self.num_of_verbs = len(self.verbs)


    def remove_verb(self, verb):
        """ Removes a verb from the verb category """
        while verb in self.verbs:
            self.verbs.remove(verb)
            self.num_of_verbs -= 1

    def remove_verbs(self, verbs):
        """ Removes a list of verbs from the verb category. """
        if verbs is self.verbs: # Need to call remove_all_verbs, else would be removing items while iterating
            self.remove_verbs_all()
        else:
            for verb in verbs:
                self.remove_verb(verb)

    def remove_verbs_all(self):
        """ Removes all verbs from the verb category """
        self.remove_verbs([verb for verb in self.verbs])

    def dot_product(self, other):
        """ Returns the number of verbs appearing simultaneously in 2 different categories """
        return len(self * other)

    def angle(self, other):
        """ Returns the angle of the dot product between 2 different categories """
        return math.acos(self.dot_product(other)/math.sqrt((len(self) * len(other))))

    def add_to_dictionary(self):
        pass


