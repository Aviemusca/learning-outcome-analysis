import os
import sys
import json
import pickle
import math
from utils.files import file_not_found_msg
from models.verb_category import VerbCategory

class Taxonomy:
    """ A class to manage a learning outcome taxonomy """

    #######################
    ### Class Variables ###
    #######################

    num_of_taxs = 0 # Number of taxonomy instances created from the class

    #########################
    ###   Magic Methods   ###
    #########################

    def __init__(self, name="", num_of_verb_cats=0, verb_cat_names=[], filename_verbs_txt="", filename_verb_dict=""):
        self.name = name.upper() # Taxonomy name e.g. Bloom, SOLO etc..
        self.num_of_verb_cats = num_of_verb_cats # Number of verb categories in the taxonomy
        self.verb_cat_names = [name.upper() for name in verb_cat_names]
        self.verb_cats = [VerbCategory(name=name) for name in verb_cat_names] # List of verb category objects of the taxonomy
        self.filename_verbs_txt = filename_verbs_txt # Name of the input verb .txt file (File not required, but its inclusion allows for near fully-automated taxonomy object construction)
        self.verb_frequencies = {} # Number of times each verb appears in the taxonomy

        Taxonomy.num_of_taxs += 1

    def __str__(self):
        return f"\n{self.name}\n\n" + '\n\n'.join([str(VC) for VC in self.verb_cats])

    def __getitem__(self, index):
        return self.verb_cats[index]

    def __len__(self):
        return len(self.verb_cats)

    ########################
    ### Instance Methods ###
    ########################


    def user_input_tax_name(self):
        """ Asks the user for the name of the taxonomy """
        self.name = input("Choose a name for the taxonomy: ").upper()

    def user_input_filename_verbs(self):
        """ Asks user for the name of the input text file containing the verbs"""
        while True:
            filename = input("Enter the file name of your verb list text file: ")
            try:
                with open(filename, 'r') as f:
                    pass
            except FileNotFoundError:
                print(file_not_found_msg(filename))
            else:
                self.filename_verbs_txt = filename # Also returned below if needed
                break
        return filename


    def set_num_verb_cats(self, number):
        """ Sets the number of verb categories in the taxonomy """
        if not isinstance(number, int):
            raise TypeError("The number of verb categories must be an interger!")
        self.num_of_verb_cats = number

    def user_input_num_verb_cats(self):
        """ Asks the user to set the number of verb categories in the taxonomy """
        self.set_num_verb_cats(int(input(f"How many verb categories do you want to include in the taxonomy '{self.name}'?: ")))

    def set_num_verb_cats_from_file(self, filename=""):
        """ Sets the number of verb categories from the number of lines in a file """
        if filename == "": # Default to self attribute if no filename provided
            filename = self.filename_verbs_txt
        tmp, self.num_of_verb_cats = self.num_of_verb_cats, 0
        try:
            with open (filename, 'r') as f:
                self.num_of_verb_cats = sum(1 for line in f)
        except FileNotFoundError:
            print(file_not_found_msg(filename))
            self.num_of_verb_cats = tmp
        else:
            return self.num_of_verb_cats

    def user_check_num_verb_cats(self):
        """ Checks whether the user is happy with the number of (detected) verb categories """
        print(f"\nNumber of detected verb categories: {self.num_of_verb_cats}.")
        get_character = input ("If this seems correct, just hit enter. Else, enter 'q': ")
        while True:
            if get_character == '':
                break
            elif get_character == 'q':
                print (f"Please correct file '{self.filename_verbs_txt}' and ensure verbs from a given category are on their own line, then restart. Bye!")
                sys.exit ()
            else:
                get_character = input ("\nYou have entered an invalid key!\nPlease enter 'q' or hit enter: ")

    def add_verb_cat_name(self, cat_name):
        """ Adds a category name to the verb category name list """
        if cat_name.upper() not in self.verb_cat_names:
            self.verb_cat_names.append(cat_name.upper())
            return True
        else:
            print(f"'{cat_name.upper()}' already in the '{self.name}' taxonomy verb category names.")
            return False

    def add_verb_cat_names(self, cat_names):
        """ Adds a list of category names to the verb category name list """
        for cat_name in cat_names:
            self.add_verb_cat_name(cat_name)

    def user_input_verb_cat_names(self, filename=""):
        """ Asks user for the names of the verb categories of the taxonomy """
        if self.num_of_verb_cats == 0:
            print(f"The number of verb categories is currently 0.")
        if filename == "": # Default to self attribute if no filename provided
            filename = self.filename_verbs_txt
        index = 0
        while index < self.num_of_verb_cats: # A for loop would increment index after each iteration
            cat_name = input (f"Enter the category name of verbs associated with line {index+1} in the file '{filename}': ")
            if self.add_verb_cat_name(cat_name):
                index += 1

    def add_verb_cat(self, cat_name="", verbs=[]):
        """ Instantiates a verb category object and appends it to the verb category list of the taxonomy """
        if cat_name.upper() not in [category.name for category in self.verb_cats]:
            VC = VerbCategory(name=cat_name.upper(), verbs=verbs)
            self.verb_cats.append(VC)
            self.num_of_verb_cats += 1
            return True
        else:
            print(f"'{cat_name.upper()}' object is already in the '{self.name}' taxonomy verb category object list.")
            return False

    def remove_verb_cat(self, cat_name=""):
        """ Removes a verb category from the verb category object list of the taxonomy """
        while cat_name.upper() in [verb_cat.name for verb_cat in self.verb_cats]:
            for cat in self.verb_cats:
                if cat.name == cat_name.upper():
                    self.verb_cats.remove(cat)
                    self.num_of_verb_cats -= 1


    def remove_verb_cats(self):
        """ Removes all verb categories from the verb category list """
        for cat in self.verb_cats:
            self.remove_verb_cat(cat.name)

    def initialise_verb_cats(self):
        """ Initialises a list of verb categories of appropriate name and attaches it to the taxonomy """
        self.remove_verb_cats() # Remove any existing verb categories
        for cat_name in self.verb_cat_names:
            self.add_verb_cat(cat_name=cat_name)

    def load_verbs_from_file(self, filename=""):
        """ Loads the .txt file verbs into the verb category object list """
        if filename == "":
            filename = self.filename_verbs_txt
        for index, VC in enumerate(self.verb_cats):
            VC.add_verbs_from_file(filename, index)


    def dump_taxonomy(self, filename):
        """  Writes a taxonomy object to a pickle file """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


    def overlap(self):
        """ Returns the number of verbs appearing simultaneously in 2 different categories across all categories"""
        return sum([VC_i.dot_product(VC_j) for i, VC_i in enumerate(self.verb_cats) for j, VC_j in enumerate(self.verb_cats) if j > i])

    def verb_frequency_count(self):
        """ Returns a frequency count dictionary of all the verbs of the taxonomy. Key -> verb; Value -> number of occurrances in the verb categories"""
        freqs = {}
        for VC in self.verb_cats:
            for verb in VC.verbs:
                freqs[verb] = freqs[verb] + 1 if verb in freqs else 1
        # sort dict by values
        self.verb_frequencies = {k : v for k, v in sorted(freqs.items(), key=lambda item: item[1])}


    #################
    ### Functions ###
    #################


def verb_cat_list_to_dict(VCs):
    """ Returns a verb dictionary from a list of verb category objects. Key -> category name; Value -> list of verbs """
    return {VC.name : VC.verbs for VC in VCs}

def dict_to_verb_cat_list(verb_dict):
    """ Returns a list of verb categories from an input verb dictionary """
    return [VerbCategory(category, verbs) for category, verbs in verb_dict.items()]

def dump_verb_dict(verb_dict, filename):
    """ Writes the verb dictionary to a json file """
    with open(filename, 'w') as f:
        json.dump(verb_dict, f)

def load_verb_dict(filename):
    """ Loads a verb dictionary from a json file """
    try:
        with open(filename, 'r') as f:
            verb_dict = json.load(f)
    except FileNotFoundError:
        print(file_not_found_msg(filename))
    else:
        return verb_dict

def load_taxonomy(filename):
    """ Loads a taxonomy object from a pickle file """
    try:
        with open(filename, 'rb') as f:
            taxonomy = pickle.load(f)
    except FileNotFoundError:
        print(file_not_found_msg(filename))
    else:
        return taxonomy

