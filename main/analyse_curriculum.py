import argparse
import json
from models.curriculum import Curriculum, load_curriculum
from models.taxonomy import Taxonomy, load_taxonomy, verb_cat_list_to_dict
from models.learning_outcome import LearningOutcome


# Argument Parser
parser = argparse.ArgumentParser(description="Both a taxonomy object and a curriculum object are required for running this script.")
parser.add_argument("-T", help="This is the taxonomy object (pickle) filename")
parser.add_argument("-C", help="This is the curriculum object (pickle) filename")
args = parser.parse_args()


# Load Taxonomy and Curriculum Objects
tax = load_taxonomy(args.T)
curr = load_curriculum(args.C)

# Convert taxonomy object to dict
verb_dict = verb_cat_list_to_dict(tax.verb_cats)

# Parse the learning outcomes of the curriculum using spaCy nlp
# and get the verb dict category hits for each learning outcome
curr.LO_category_hits_spacy(verb_dict)

# Format learning outcome category hit counts as a count dict
count = curr.get_count_dict()

# Write to file
with open(f"{curr.name}-{tax.name}.count.json", 'w') as f:
    json.dump(count, f)
