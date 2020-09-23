from models.taxonomy import Taxonomy, verb_cat_list_to_dict, dump_verb_dict

""" Script which builds a learning outcome taxonomy for the user from an
input verb .txt file and dumps it to a pickle file.
A human-readable version is dumped to a json file, in the form of a dictionary """

# Instantiates a taxonomy object
tax = Taxonomy()
# User inputs name of the taxonomy e.g. 'bloom'
tax.user_input_tax_name()
# User inputs name of the .txt verb list file
tax.user_input_filename_verbs()
# Sets number of verb category objects to create equal to number of new lines in verb file
tax.set_num_verb_cats_from_file()
# Confirms detected number of verb categories with user
tax.user_check_num_verb_cats()
# User inputs the name of the verb categories
tax.user_input_verb_cat_names()
# Instantiates the verb categories and attaches a list of these to the taxonomy
tax.initialise_verb_cats()
# Loads the .txt file verbs into each verb category
tax.load_verbs_from_file()
# Writes a pickle object representation of the taxonomy to file
tax.dump_taxonomy(f"{tax.name}.tax.pickle")
# Converts the verb categories to dictionary form
verb_dict = verb_cat_list_to_dict(tax.verb_cats)
# Writes a json verb dictionary to file
dump_verb_dict(verb_dict, f"{tax.name}.verb_dict.json")
