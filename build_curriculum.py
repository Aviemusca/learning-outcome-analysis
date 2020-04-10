from curriculum_class import Curriculum, LO_list_to_dict, dict_to_LO_list, dump_LO_dict

""" Scripts which builds a curriculum for the user from an input learning outcome .txt file and dumps it to a pickle file. A human-readable version is dumped to a json file, in the form of a dictionary """
curr = Curriculum() # Instantiates a curriculum object
curr.user_input_name() # User inputs name of the curriculum e.g. 'computer_science'
curr.user_input_filename_LOs() # User inputs name of the .txt file containing the learning outcomes
curr.set_num_strands_from_file() # Sets the number of learning outcome strands from blank lines in file
curr.user_check_num_strands() # Checks with user whether number of strands is correct
curr.user_input_strand_names() # User inputs names of the strands
curr.load_LOs_from_file(curr.filename_LOs_txt) # Loads the LOs into the curriculum, as a list of lists of LearningOutcome objects
curr.dump_curriculum(f"{curr.name}.curriculum.pickle") # Writes a pickle object representation of the curriculum to file
LO_dict = LO_list_to_dict(curr.LOs, curr.strand_names) # Converts the LO lists to dictionary form
dump_LO_dict(LO_dict, f"{curr.name}.LO_dict.json")
