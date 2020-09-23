import os
import sys
import json
import pickle

from models.learning_outcome import LearningOutcome
from utils.files import file_not_found_msg


class Curriculum:
    """ A class to manage the collection of learning outcome strands of a curriculum """

    #######################
    ### Class Variables ###
    #######################

    num_of_curr = 0

    #######################
    ### Special Methods ###
    #######################

    def __init__(self, name="", country="", ID="", num_of_strands=0, strand_names=[], filename_LOs_txt=""):
        self.name = self.set_name(name)                                 # Name of the curriculum e.g. CS, Math
        self.country = self.set_country(country)                        # Origin country of the curriculum
        self.ID = self.set_ID(ID)                                       # ID of the curriculum
        self.num_of_strand = self.set_num_of_strands(num_of_strands)    # Number of learning outcome strands in the curriculum
        self.strand_names = self.set_strand_names(strand_names)          # Names of the learning outcome strands
        self.filename_LOs_txt = self.set_filename_LOs(filename_LOs_txt) # Sets the input LO .txt file name
        self.LOs = [[]]                                                 # The learning outcome objects of the curriculum, each inner list is a strand of LOs


    def __getitem__(self, position):
        """ Sets the position in the curriculum equal to the position in a flattened list of lists (2-level), e.g. looping through a curriculum loops over the LOs of the first strand, then the LOs of the second strand etc.. """
        strand_idx = 0
        while position > len(self.LOs[strand_idx]) - 1:
            position -= len(self.LOs[strand_idx])
            strand_idx += 1
        return self.LOs[strand_idx][position]


    ########################
    ### Instance methods ###
    ########################


    def set_name(self, name):
        """ Sets the name of the curriculum """
        self.name = name.upper()
        return self.name


    def user_input_name(self):
        """ Asks the user for the name of the curriculum """
        self.name = self.set_name(input("Enter the name of the curriculum: "))


    def set_country(self, country):
        """ Sets the country of the curriculum """
        self.country = country.title()
        return self.country


    def user_input_counry(self):
        """ Asks the user for the country of the curriculum """
        self.country = self.set_country(input("Enter the origin country of the curriculum: "))


    def set_ID(self, ID):
        """ Sets the id of the curriculum """
        self.ID = ID
        return self.ID


    def set_filename_LOs(self, filename):
        """ Sets the name of the file containing the learning outcomes """
        if filename == "": return
        try:
            with open(filename, 'r') as f:
                pass
        except FileNotFoundError:
            print(file_not_found_msg(filename))
        else:
            self.filename_LOs_txt = filename
            return self.filename_LOs_txt


    def user_input_filename_LOs(self):
        """ Asks the user for the name of the input text file containing the learning outcomes """
        while True:
            filename = input("Enter the file name of the learning outcome text file: ")
            try:
                with open(filename, 'r') as f:
                    pass
            except FileNotFoundError:
                print (file_not_found_msg(filename))
            else:
                self.filename_LOs_txt = filename
                break


    def set_num_of_strands(self, number):
        """ Sets the number of learning outcome strands in the curriculum """
        if not isinstance(number, int):
            raise TypeError("The number of learning outcome strands must be an integer!")
        self.num_of_strands = number
        return self.num_of_strands


    def set_strand_names(self, names):
        """ Sets the names of the learning outcome strands """
        self.strand_names = [name.upper() for name in names]
        return self.strand_names


    def user_input_num_strands(self):
        """ Asks the user to set the number of learning outcome strands """
        self.num_of_strands(int(input(f"How many learning outcome strands do you want to include in the curriculum '{self.name}'?: ")))


    def set_num_strands_from_file(self, filename=""):
        """ Sets the number of strands from the number of blank lines in a file """
        if filename == "": # Default to self attribute if no filename provided
            filename = self.filename_LOs_txt
        tmp, self.num_of_strands = self.num_of_strands, 0
        try:
            with open (filename, 'r') as f:
                self.num_of_strands = 1 + sum(1 if line == '\n' else 0 for line in f)
        except FileNotFoundError:
            print (file_not_found_msg(filename))
            self.num_of_strands = tmp


    def user_check_num_strands(self):
        """ Checks whether the user is happy with the number of (detected) strands """
        print(f"\nNumber of detected strands: {self.num_of_strands}.")
        get_character = input ("If this seems correct, just hit enter. Else, enter 'q': ")
        while True:
            if get_character == '':
                break
            elif get_character == 'q':
                print (f"Please correct file '{self.filename_LOs_txt}' and ensure learning outcome strands are separated by a blank line, then restart. Bye!")
                sys.exit ()
            else:
                get_character = input ("\nYou have entered an invalid key!\nPlease enter 'q' or hit enter: ")


    def add_strand_name(self, name):
        """ Adds a strand name to the strand name list """
        if name.upper() not in self.strand_names:
            self.strand_names.append(name.upper())
            return True
        else:
            print(f"'{name.upper()}' already in the '{self.name}' curriculum strand names.")
            return False


    def add_strand_names(self, names):
        """ Adds a list of strand names to the strand name list """
        for name in names:
            self.add_strand_name(name)


    def user_input_strand_names(self, filename=""):
        """ Asks user for the names of the learning outcome strands """
        if self.num_of_strands == 0:
            print(f"The number of strands is currently 0.")
        if filename == "": # Default to self attribute if no filename provided
            filename = self.filename_LOs_txt
        index = 0
        while index < self.num_of_strands: # A for loop would increment index after each iteration
            strand_name = input (f"Enter the name of the strand associated with block {index+1} of learning outcomes in the file '{filename}': ")
            if self.add_strand_name(strand_name):
                index += 1


    def load_LOs_from_file(self, filename=""):
        """ Creates a list of lists of learning outcome objects and loads their text from a file. Each inner list is a list of learning outcome objects pertaining to a perticular strand """
        if filename == "":
            filename = self.filename_LOs_txt
        strand_idx = 0
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line == '\n': # strands are blank line separated
                        strand_idx += 1
                        self.LOs.append([]) # Create new list for the next strand
                    else:
                        LO = LearningOutcome(line.lower().strip())
                        self.LOs[strand_idx].append(LO)
        except FileNotFoundError:
            print(file_not_found_msg(filename))


    def dump_curriculum(self, filename):
        """  Writes a Curriculum object to a pickle file """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def LO_category_hits_spacy(self, verb_dict):
        for strand in self.LOs:
            for LO in strand:
                LO.get_category_hits(verb_dict)


    def get_count_dict(self):
        """ Return the hit count dictionary of the curriculum
        (to be called after nlp parsing) """
        count = {}
        for index, strand in enumerate(self.LOs):
            count[self.strand_names[index]] = [LO.category_hits for LO in strand]
        return count


    #################
    ### Functions ###
    #################


def LO_list_to_dict(LOs, strand_names):
    """ Returns a LO dictionary from a list of lists of LO objects. Key -> strand name; Value -> list of LOs (text) """
    return {strand_name : [LO.text for LO in LOs[idx]] for idx, strand_name in enumerate(strand_names)}

def dict_to_LO_list(LO_dict):
    """ Returns a list of lists of LO objects from an input LO dictionary """
    LO_list = []
    for strand in LO_dict:
        LO_list.append([LearningOutcome(text) for text in LO_dict[strand]])
    return LO_list

def load_curriculum(filename):
    """ Loads a curriculum object from a pickle file """
    try:
        with open(filename, 'rb') as f:
            curriculum = pickle.load(f)
    except FileNotFoundError:
        print(file_not_found_msg(filename))
    else:
        return curriculum

def dump_LO_dict(LO_dict, filename):
    """ Dumps a learning outcome dictionary to a json file """
    with open(filename, 'w') as f:
        json.dump(LO_dict, f)

