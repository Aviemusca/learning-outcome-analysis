from models.taxonomy import Taxonomy, verb_cat_list_to_dict, dump_verb_dict

""" Script which builds a learning outcome taxonomy for the user from an input verb .txt file and dumps it to a pickle file. A human-readable version is dumped to a json file, in the form of a dictionary """

tax = Taxonomy() # Instantiates a taxonomy object
tax.user_input_tax_name() # User inputs name of the taxonomy e.g. 'bloom'
tax.user_input_filename_verbs() # User inputs name of the .txt verb list file
tax.set_num_verb_cats_from_file() # Sets number of verb category objects to create equal to number of new lines in verb file
tax.user_check_num_verb_cats() # Confirms detected number of verb categories with user
tax.user_input_verb_cat_names() # User inputs the name of the verb categories
tax.initialise_verb_cats() # Instantiates the verb categories and attaches a list of these to the taxonomy
tax.load_verbs_from_file() # Loads the .txt file verbs into each verb category
tax.dump_taxonomy(f"{tax.name}.tax.pickle") # Writes a pickle object representation of the taxonomy to file
verb_dict = verb_cat_list_to_dict(tax.verb_cats) # Converts the verb categories to dictionary form
dump_verb_dict(verb_dict, f"{tax.name}.verb_dict.json") # Writes a json verb dictionary to file
