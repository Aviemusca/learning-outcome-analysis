import os
import sys
import json
import spacy
import math

from verb_category_class import VerbCategory
from functions import get_lines, file_not_found_msg

class Strand(VerbCategory):
    """ A class to manage each strand of learning outcomes from a curriculum """

    # Class variables
    num_of_strands = 0 # Total number of learning outcome strands in the class
    num_of_LOs_per_strand = [0] # Stores number of LOs in each strand, given an input file
    strand_names = [] # Names of the learning outcome strands
    verb_categories = VerbCategory.category_names # The verb category names to be used in LO categorisation
    LO_dictionary = {} # Stores strands and respective LOs as key-value pairs
    filename_text_LO = "" # Input LO text document filename
    filename_json_LO = "" # Output LO_dictionary json document filename

    def __init__(self, name):
        self.name = name.upper()
        self.LOs = []
        self.num_of_LOS = 0

        Strand.num_of_strands += 1

    def __repr__(self):
        output = f"{self.name}:\n"
        for index, LO in enumerate(self.LOs):
            output += f"\t{index+1}) {LO.text}.\n"
        return output


    def __len__(self):
        """ The length of a strand is equal to the total number of learning outcomes in the strand """
        return self.num_of_LOS

    @classmethod
    def set_verb_categories(cls, categories):
        cls.verb_categories = [category.upper() for category in categories]

    @classmethod
    def get_filename_text_LO(cls):
        """ Prompts the user for the name of the input text file containing the learning outcomes """
        while True:
            filename = input("Enter the file name of your learning outcome text file: ")
            try:
                with open(filename, 'r') as f:
                    pass
            except FileNotFoundError:
                print (file_not_found_msg(filename))
            else:
                break
        cls.filename_text_LO = filename

    @classmethod
    def set_filename_json_LO(cls):
        """ Strips '.txt' from the LO text filename and appends '.json' """
        cls.filename_json_LO = os.path.splitext(cls.filename_text_LO)[0] + '.json'

    @classmethod
    def set_number_of_strands_from_file(cls, filename=""):
        """ Detects and sets the number of strands number of learning outcomes in each strand from the number of blank lines in the LO text file """
        if filename == "": # Use class variable as default filename
            filename = cls.filename_text_LO
        try:
            with open(filename, 'r') as f:
                cls.num_of_strands = 1 # Default i.e. no blank lines
                for line in f:
                    if line == '\n':
                        cls.num_of_strands += 1
                        cls.num_of_LOs_per_strand.append(0)
                    else:
                        cls.num_of_LOs_per_strand[cls.num_of_strands - 1] += 1
        except FileNotFoundError:
            print (file_not_found_msg(filename))

    @classmethod
    def confirm_number_of_strands(cls):
        """ Confirm detected number of LO strands with user """
        print(f"\nTotal number of learning outcome strands detected: {cls.num_of_strands}.")
        get_character = input ("\nIf this is correct, just hit enter. If this is incorrect, enter 'q': ")
        while True:
            if get_character == '':
                break
            elif get_character == 'q':
                print ("\nPlease correct your file '{cls.filename_text_LO}' and separate learning outcome strands by a blank line, then restart. Bye!\n")
                sys.exit ()
            else:
                get_character = input ("\nYou have entered an invalid key!\nPlease enter 'q' or hit enter: ")

    @classmethod
    def get_strand_names(cls):
        for index in range(cls.num_of_strands):
            strand = input (f"Enter the name of the learning outcome strand associated with block {index+1} of lines in the file '{cls.filename_text_LO}': ")
            cls.strand_names.append(strand.upper())


    @classmethod
    def make_LO_dictionary(cls, strands):
        """Merges the strands and the LOs into a dictionary. Each key is a strand name, each value is a LO list of the respective strand"""
        LO_dict = {}
        for strand in strand: # Create the dictionary keys and empty lists
            LO_dict[strand.name] = []
            for LO in strand.LOs:
                LO_dict[strand.name].append(LO.text)
        index = 0 # incremented on empty LO in LO_list
        for LO_text in cls.LO_list:
            if LO_text == "":
                index += 1
            else:
                LO = LearningOutcome(strand_names[index], LO_text.lower().strip())
                cls.LO_dictionary[cls.strand_names[index]].append(LO)


    def add_LO(self, text):
        """ Adds a learning outcome to the strand if not already in the strand """
        # may want to add a check if LO text is already in the LOs list
        LO = LearningOutcome(text)
        self.LOs.append(LO)
        self.num_of_LOS += 1


    def add_LOs_from_file(self, filename, start_line, end_line):
        """ Adds a list of learning outcomes to the strand, given a starting line index number and end line index number (file lines numbered from 0 and end_line not included) of a file """
        try:
            with open(filename, 'r') as f:
                for index, line in enumerate(f):
                    if index >= start_line and index < end_line:
                        self.add_LO(line.lower().strip())
        except FileNotFoundError:
            print(f"File {filename} not found! Please check the filename and file directory.")

    def get_complexity(self):
        """ Should return a dict with the number/percentage of LOs appearning in 6 categories, 5 categories etc..  """
        pass

class LearningOutcome(Strand):
    """  A class to manage each learning outcome of a curriculum """

    # Class variables
    num_of_LOs = 0 # Total number of learning outcomes in the class

    def __init__(self, text=""):
        self.category_hits = {} # Keys = verb categories; values = number of verbs in LO from that category
        self.num_of_verbs = 0 # Number of verbs in the learning outcome
        self.text = text # The string/text of a learning outcome
        for category in LearningOutcome.verb_categories:
            self.category_hits[category] = 0

        LearningOutcome.num_of_LOs += 1


    def load_LO(self, strand, index):
        """Loads the LO text into a LO class instance"""
        self.text = self.LO_dictionary[strand][index]

    @classmethod
    def write_json_count_dictionary(cls):
        """ Writes the json count dictionary to file """
        pass

    def attach_category_hits_dictionary(self, categories):
        """ Creates an attribute dictionary whose keys are the verb category names of the taxonomy"""
        for category in categories:
            self.category_hits[category] = 0

    def get_pos(self, verb_dictionary):
        allowed_non_verbs = ["who", "what", "where", "when", "why"]
        non_detected_verbs = ["test", "sort", "analyse", "store"]
        nlp = spacy.load("en_core_web_sm")
        tokenised_LO = nlp(self.text)
        for token in tokenised_LO:
            for category in verb_dictionary:
                if (token.pos_ == "VERB" or token.text in (allowed_non_verbs or non_detected_verbs)) and token.lemma_ in verb_dictionary[category]:
                    self.category_hits[category] += 1

