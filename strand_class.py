import os
import sys
import json
import spacy
import math

from verb_category_class import VerbCategory
from learning_outcome_class import LearningOutcome
from functions import get_lines, file_not_found_msg

class Strand:
    """ A class to manage each strand of learning outcomes from a curriculum """

    #######################
    ### Special Methods ###
    #######################

    def __init__(self, name, num_of_LOs=0, LOs=[]):
        self.name = name.upper()
        self.num_of_LOs = num_of_LOs
        self.LOs = LOs


    def __repr__(self):
        output = f"Strand(name='{self.name}', num_of_LOs={self.num_of_LOs},"
        output += "[" + ', '.join(["LearningOutcome()" for LO in self]) + "])"
        return output

    def __str__(self):
        output = f"{self.name}:\n"
        for index, LO in enumerate(self.LOs):
            output += f"\t{index+1}) {LO.text}.\n"
        return output

    def __len__(self):
        """ The length of a strand is equal to the total number of learning outcomes in the strand """
        return len(self.LOs)

    #def __getitem__(self, index):
     #   return self.LOs[index]

#    @classmethod
#    def make_LO_dictionary(cls, strands):
#        """Merges the strands and the LOs into a dictionary. Each key is a strand name, each value is a LO list of the respective strand"""
#        LO_dict = {}
#        for strand in strand: # Create the dictionary keys and empty lists
#            LO_dict[strand.name] = []
#            for LO in strand.LOs:
#                LO_dict[strand.name].append(LO.text)
#        index = 0 # incremented on empty LO in LO_list
#        for LO_text in cls.LO_list:
#            if LO_text == "":
#                index += 1
#            else:
#                LO = LearningOutcome(strand_names[index], LO_text.lower().strip())
#                cls.LO_dictionary[cls.strand_names[index]].append(LO)

#
#       def add_LO(self, text):
#           """ Adds a learning outcome to the strand if not already in the strand """
#           # may want to add a check if LO text is already in the LOs list
#           LO = LearningOutcome(text)
#           self.LOs.append(LO)
#           self.num_of_LOs += 1
#
#

    def load_LOs(self, filename, start_line, end_line):
        """ Adds a list of learning outcomes to the strand, given a starting line index number and end line index number (file lines numbered from 0 and end_line not included) of a file """
        try:
            print("pass")
            with open(filename, 'r') as f:
                for index, line in enumerate(f):
                    if index >= start_line and index < end_line:
                        print(line)
                        LO = LearningOutcome(line.lower().strip())
                        self.LOs.append(LO)
        except FileNotFoundError:
            print(file_not_found_msg(filename))

    def get_complexity(self):
        """ Should return a dict with the number/percentage of LOs appearing in 6 categories, 5 categories etc..  """
        pass


