import argparse
from curriculum_class import Curriculum, load_curriculum
from taxonomy_class import Taxonomy, load_taxonomy, verb_cat_list_to_dict
from learning_outcome_class import LearningOutcome


### Argument Parser ###

parser = argparse.ArgumentParser(description="Both a taxonomy object and a curriculum object are required for running this script.")
parser.add_argument("-T", help="This is the taxonomy object (pickle) filename")
parser.add_argument("-C", help="This is the curriculum object (pickle) filename")
args = parser.parse_args()


### Load Taxonomy and Curriculum Objects ###

tax = load_taxonomy(args.T)
curr = load_curriculum(args.C)

verb_dict = verb_cat_list_to_dict(tax.verb_cats)
curr.LO_category_hits_spacy(verb_dict)

for LO in curr:
    print(LO.category_hits)
