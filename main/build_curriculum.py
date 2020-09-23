from models.curriculum import (
        Curriculum,
        LO_list_to_dict,
        dict_to_LO_list,
        dump_LO_dict
        )

""" Scripts which builds a curriculum for the user from an input
learning outcome .txt file and dumps it to a pickle file.
A human-readable version is dumped to a json file, as a dictionary """

# Instantiates a curriculum object
curr = Curriculum()
# User inputs name of the curriculum e.g. 'computer_science'
curr.user_input_name()
# User inputs name of the .txt file containing the learning outcomes
curr.user_input_filename_LOs()
# Sets the number of learning outcome strands from blank lines in file
curr.set_num_strands_from_file()
# Checks with user whether number of strands is correct
curr.user_check_num_strands()
# User inputs names of the strands
curr.user_input_strand_names()
# Loads the LOs into the curriculum, as a list of lists of LearningOutcome objects
curr.load_LOs_from_file(curr.filename_LOs_txt)
# Writes a pickle object representation of the curriculum to file
curr.dump_curriculum(f"{curr.name}.curriculum.pickle")
# Converts the LO lists to dictionary form
LO_dict = LO_list_to_dict(curr.LOs, curr.strand_names)
dump_LO_dict(LO_dict, f"{curr.name}.LO_dict.json")
